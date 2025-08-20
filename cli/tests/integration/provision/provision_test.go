package provision

import (
	containerClient "cli/internal/adapter/client/container"
	"cli/internal/domain/entity"
	"cli/internal/service/container"
	"cli/internal/service/resolver"
	"context"
	"github.com/docker/docker/client"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestProvision(t *testing.T) {
	dockerClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	assert.NoError(t, err)

	c := containerClient.NewContainer(dockerClient)
	resolverService := resolver.NewService()

	containerService := container.NewService(c, resolverService)

	ctx := context.Background()

	_, err = containerService.StartContainers(ctx, &entity.RunPreRequisiteRequest{
		Chapter:    entity.Chapter6,
		SubChapter: 2,
		CopyData:   true,
	})
	assert.NoError(t, err)
}
