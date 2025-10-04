package imagebuilder

import (
	domainerrors "cli/internal/domain/errors"
	"context"
	"github.com/docker/docker/client"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestClient_Images(t *testing.T) {
	dockerClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	assert.NoError(t, err)

	image := "testimage"
	tag := "1.0.0"

	cl := NewClient(dockerClient)
	ctx := context.Background()

	err = cl.BuildImage(ctx, image, tag)
	assert.NoError(t, err)

	assert.Nil(t, cl.Exists(ctx, image, tag))

	assert.ErrorIs(t, cl.Exists(ctx, image, "1.1.0"), domainerrors.ErrImageNotFound)
}
