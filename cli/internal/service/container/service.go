package container

import (
	"cli/internal/domain/entity"
	domainerrors "cli/internal/domain/errors"
	"context"
	"errors"
	"github.com/docker/docker/api/types/container"
	"sync"
	"time"
)

type Client interface {
	ListContainers(ctx context.Context) ([]*entity.ContainerMetadata, error)
	Clear(ctx context.Context, metadata *entity.ContainerMetadata) error
	Run(ctx context.Context, arg *entity.ContainerRunRequest) (*entity.CreateContainerResponse, error)
	ReadLogs(ctx context.Context, containerID string) (string, error)
	Wait(ctx context.Context, containerID string) (<-chan container.WaitResponse, <-chan error)
	IsHealthy(ctx context.Context, containerID string) (bool, error)
	RunScript(ctx context.Context, containerID string, command []string) error
	CreateNetwork(ctx context.Context, request *entity.CreateNetworkRequest) (*entity.CreateNetworkResponse, error)
	GetNetworkID(ctx context.Context, app string) (*entity.Network, error)
	RemoveNetwork(ctx context.Context, networkID string) error
}

type Resolver interface {
	Resolve(ctx context.Context, request *entity.ResolveRequest) ([]*entity.ContainerRunRequest, error)
}

type Service struct {
	client   Client
	resolver Resolver
}

func NewService(client Client, resolver Resolver) *Service {
	return &Service{
		client:   client,
		resolver: resolver,
	}
}

func (s *Service) ListContainers(ctx context.Context) ([]*entity.ContainerMetadata, error) {
	containers, err := s.client.ListContainers(ctx)
	if err != nil {
		return nil, err
	}

	return containers, nil
}

func (s *Service) Clear(ctx context.Context) error {
	containers, err := s.ListContainers(ctx)
	if err != nil {
		return err
	}

	for _, container := range containers {
		err = s.client.Clear(ctx, container)
		if err != nil {
			return err
		}
	}

	network, err := s.client.GetNetworkID(ctx, "sedona")
	if err != nil && errors.Is(err, domainerrors.ErrNetworkNotFound) {
		return nil
	}

	if err != nil {
		return err
	}

	err = s.client.RemoveNetwork(ctx, network.ID)
	if err != nil {
		return err
	}

	return nil
}

func (s *Service) StartContainers(ctx context.Context, request *entity.RunPreRequisiteRequest) error {
	images, err := s.resolver.Resolve(ctx, &entity.ResolveRequest{
		Chapter:    request.Chapter,
		LoadData:   request.CopyData,
		SubChapter: request.SubChapter,
	})
	if err != nil {
		return err
	}

	// Create a network for the containers
	networkRequest := &entity.CreateNetworkRequest{
		Name: "sedona",
	}

	networkResponse, err := s.client.CreateNetwork(ctx, networkRequest)
	if err != nil {
		return nil
	}

	wg := &sync.WaitGroup{}
	wg.Add(len(images))

	for _, image := range images {
		go func() {
			defer wg.Done()
			image.NetworkID = networkResponse.ID
			containerInfo, err := s.client.Run(ctx, image)
			if err != nil {
				println("Error starting container:", err.Error())
				return
			}

			healthy, err := s.WaitUntilHealthy(ctx, containerInfo.ID)
			if err != nil {
				return
			}

			if !healthy {
				return
			}

			println("Container started successfully:", containerInfo.ID)
			if len(image.PostInitCommand) == 0 {
				return
			}

			err = s.client.RunScript(ctx, containerInfo.ID, image.PostInitCommand)
			if err != nil {
				println("Error running script:", err.Error())
				return
			}
		}()
	}

	wg.Wait()

	return nil
}

func (s *Service) WaitUntilHealthy(ctx context.Context, containerID string) (bool, error) {
	ctxWithTimeout, cancel := context.WithTimeout(ctx, time.Second*20)
	defer cancel()

	sleepTicker := time.NewTicker(time.Second * 2)

	for {
		select {
		case <-ctxWithTimeout.Done():
			return false, nil
		case <-sleepTicker.C:
			healthy, err := s.client.IsHealthy(ctxWithTimeout, containerID)
			if err != nil {
				return false, err
			}

			if healthy {
				return true, nil
			}
		}
	}
}
