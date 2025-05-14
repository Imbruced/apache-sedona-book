package container

import (
	"cli/internal/domain/entity"
	domainerrors "cli/internal/domain/errors"
	"context"
	"fmt"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/filters"
	"github.com/docker/docker/api/types/mount"
	"github.com/docker/docker/api/types/network"
	"github.com/docker/docker/client"
	"github.com/docker/go-connections/nat"
	"io"
	"os"
	"strings"
	"time"
)

const (
	SedonaNetworkName = "sedona"
	SedonaLabelName   = "sedona"
)

var (
	SedonaLabels = map[string]string{
		"app": SedonaLabelName,
	}
)

type Container struct {
	cli *client.Client
}

func (c *Container) RunScript(ctx context.Context, containerID string, command []string) error {
	execID, err := c.cli.ContainerExecCreate(ctx, containerID, container.ExecOptions{
		AttachStdin:  false,
		AttachStdout: true,
		AttachStderr: true,
		Tty:          false,
		Cmd:          command,
	})
	if err != nil {
		return err
	}

	resp, err := c.cli.ContainerExecAttach(ctx, execID.ID, container.ExecAttachOptions{})
	if err != nil {
		return err
	}
	defer resp.Close()

	for {
		_, err = io.Copy(os.Stdout, resp.Reader)
		if err != nil {
			return err
		}

		inspectResp, err := c.cli.ContainerExecInspect(ctx, execID.ID)
		if err != nil {
			return err
		}

		println(inspectResp.ExitCode)

		if inspectResp.Running {
			time.Sleep(1 * time.Second)
			continue
		}

		if inspectResp.ExitCode != 0 {
			return fmt.Errorf("command exited with code %d", inspectResp.ExitCode)
		}

		println("Command executed successfully")

		break
	}
	return nil
}

func (c *Container) getFilterArgs() filters.Args {
	filterArgs := filters.NewArgs()
	filterArgs.Add("label", fmt.Sprintf("app=%s", SedonaLabelName))
	return filterArgs
}

func (c *Container) GetNetworkID(ctx context.Context) (*entity.Network, error) {
	networks, err := c.cli.NetworkList(ctx, network.ListOptions{
		Filters: c.getFilterArgs(),
	})
	if err != nil {
		return nil, err
	}

	if len(networks) == 0 {
		return nil, domainerrors.ErrNetworkNotFound
	}

	if len(networks) > 1 {
		return nil, fmt.Errorf("multiple networks found")
	}

	networkInfo := networks[0]

	return &entity.Network{
		ID: networkInfo.ID,
	}, nil
}

func (c *Container) RemoveNetwork(ctx context.Context, networkID string) error {
	err := c.cli.NetworkRemove(ctx, networkID)
	if err != nil {
		return err
	}

	return nil
}

func (c *Container) CreateNetwork(ctx context.Context, request *entity.CreateNetworkRequest) (*entity.CreateNetworkResponse, error) {
	n, err := c.cli.NetworkCreate(ctx, "sedona", network.CreateOptions{
		Driver:     "bridge",
		Internal:   false,
		Attachable: true,
		Labels:     SedonaLabels,
	})
	if err != nil {
		return nil, err
	}

	return &entity.CreateNetworkResponse{
		ID: n.ID,
	}, nil
}

func (c *Container) Run(ctx context.Context, request *entity.ContainerRunRequest) (*entity.CreateContainerResponse, error) {
	portMap := make(nat.PortMap, len(request.ExposedPorts))
	exposedPorts := make(nat.PortSet, len(request.ExposedPorts))
	imageName := strings.Split(request.Image, ":")[0]
	parts := strings.Split(imageName, "/")

	imageName = parts[len(parts)-1]

	for _, containerPort := range request.ExposedPorts {
		exposedPorts[nat.Port(containerPort)] = struct{}{}
	}

	for hostPort, containerPort := range request.ExposedPorts {
		portMap[nat.Port(containerPort)] = []nat.PortBinding{
			{
				HostIP:   "0.0.0.0",
				HostPort: hostPort,
			},
		}
	}

	resp, err := c.cli.ContainerCreate(ctx, &container.Config{
		Env:          request.EnvVariables.ToEnvList(),
		Image:        request.Image,
		ExposedPorts: exposedPorts,
		Labels:       SedonaLabels,
		Cmd:          request.Command,
		Healthcheck: &container.HealthConfig{
			Test:        request.HealthCheck.Test,
			Interval:    5 * time.Second,
			Timeout:     20 * time.Second,
			Retries:     3,
			StartPeriod: 2 * time.Second,
		},
	},
		&container.HostConfig{
			PortBindings: portMap,
			Mounts:       createNewMounts(request.MountPathHost, request.MountPathContainer, request.MountFiles),
		},
		&network.NetworkingConfig{
			EndpointsConfig: map[string]*network.EndpointSettings{
				SedonaNetworkName: {
					Aliases:   []string{imageName},
					NetworkID: request.NetworkID,
				},
			},
		},
		nil,
		request.ContainerName)
	if err != nil {
		return nil, err
	}

	if err = c.cli.ContainerStart(ctx, resp.ID, container.StartOptions{}); err != nil {
		return nil, err
	}

	return &entity.CreateContainerResponse{
		ID: resp.ID,
	}, nil
}

func createNewMounts(mountHostRoot string, mountContainerRoot string, mountFiles []string) []mount.Mount {
	mounts := make([]mount.Mount, 0)

	for _, mountFile := range mountFiles {
		mounts = append(mounts, mount.Mount{
			Type:   mount.TypeBind,
			Source: mountHostRoot + "/" + mountFile,
			Target: mountContainerRoot + "/" + mountFile,
		})
	}

	return mounts
}

func (c *Container) ReadLogs(ctx context.Context, containerID string) (string, error) {
	result, err := c.cli.ContainerLogs(ctx, containerID, container.LogsOptions{
		ShowStdout: true,
		ShowStderr: true,
	})
	if err != nil {
		return "", err
	}

	defer result.Close()
	logs, err := io.ReadAll(result)
	if err != nil {
		return "", err
	}

	return string(logs), nil
}

func (c *Container) Wait(ctx context.Context, containerID string) (<-chan container.WaitResponse, <-chan error) {
	return c.cli.ContainerWait(ctx, containerID, container.WaitConditionNotRunning)
}

func NewContainer(cli *client.Client) *Container {
	return &Container{
		cli: cli,
	}
}

func (c *Container) ListContainers(ctx context.Context) ([]*entity.ContainerMetadata, error) {
	result, err := c.cli.ContainerList(ctx, container.ListOptions{
		Filters: c.getFilterArgs(),
	})
	if err != nil {
		return nil, err
	}

	containers := make([]*entity.ContainerMetadata, 0, len(result))
	for _, cn := range result {
		containers = append(containers, &entity.ContainerMetadata{
			ID:    cn.ID,
			Name:  cn.Names[0],
			State: cn.State,
		})
	}

	return containers, nil
}

func (c *Container) Clear(ctx context.Context, metadata *entity.ContainerMetadata) error {
	err := c.cli.ContainerKill(ctx, metadata.ID, "")
	if err != nil {
		return err
	}

	err = c.cli.ContainerRemove(ctx, metadata.ID, container.RemoveOptions{})
	if err != nil {
		return err
	}

	return nil
}

func (c *Container) IsHealthy(ctx context.Context, containerID string) (bool, error) {
	result, err := c.cli.ContainerInspect(ctx, containerID)
	if err != nil {
		return false, err
	}

	return result.State.Health != nil && result.State.Health.Status == "healthy", nil
}
