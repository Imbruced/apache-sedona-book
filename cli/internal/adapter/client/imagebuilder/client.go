package imagebuilder

import (
	"archive/tar"
	domainerrors "cli/internal/domain/errors"
	"context"
	"embed"
	"fmt"
	"io"
	"io/fs"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/image"
	"github.com/docker/docker/client"
	"github.com/docker/docker/errdefs"
)

//go:embed docker
var sedona embed.FS

type DockerClient interface {
	ImageBuild(ctx context.Context, buildContext io.Reader, options types.ImageBuildOptions) (types.ImageBuildResponse, error)
	ImageInspect(ctx context.Context, imageID string, inspectOpts ...client.ImageInspectOption) (image.InspectResponse, error)
}

type Client struct {
	client DockerClient
}

func NewClient(client DockerClient) *Client {
	return &Client{
		client: client,
	}
}

func (c *Client) BuildImage(ctx context.Context, imageName string, tag string) error {
	archive, err := createAnArchive(fmt.Sprintf("docker/%s", imageName))
	if err != nil {
		return err
	}

	imageBuildResponse, err := c.client.ImageBuild(
		context.Background(),
		archive,
		types.ImageBuildOptions{
			Tags:       []string{fmt.Sprintf("%s:%s", imageName, tag)},
			Dockerfile: "Dockerfile",
		})
	if err != nil {
		return err
	}

	defer imageBuildResponse.Body.Close()
	lines := make([]byte, 1024)
	// Read the response to ensure the image is built
	// You can log or process the response as needed
	for {
		n, err := imageBuildResponse.Body.Read(lines)
		if n == 0 {
			break
		}

		if err != nil && err != io.EOF {
			return err
		}
	}

	return nil
}

func (c *Client) Exists(ctx context.Context, image, tag string) error {
	_, err := c.client.ImageInspect(context.Background(), fmt.Sprintf("%s:%s", image, tag))
	if err != nil {
		_, ok := (err).(errdefs.ErrNotFound)
		if ok {
			return domainerrors.ErrImageNotFound
		}

		return err
	}

	return nil
}

func createAnArchive(path string) (reader io.Reader, err error) {
	pr, pw := io.Pipe()

	tarWriteHandler := func() (subErr error) {
		defer func() {
			err = pw.Close()
		}()

		tw := tar.NewWriter(pw)
		defer func() {
			subErr = tw.Close()
		}()

		sub, err := fs.Sub(sedona, path)
		if err != nil {
			return err
		}

		if subErr = tw.AddFS(sub); err != nil {
			return err
		}

		return nil
	}

	go func() {
		if err = tarWriteHandler(); err != nil {
			_ = pw.CloseWithError(err)
		}
	}()

	return pr, nil
}
