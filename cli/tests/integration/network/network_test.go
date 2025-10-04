package network

import (
	"cli/internal/adapter/client/container"
	"cli/internal/service/network"
	"context"
	"github.com/docker/docker/client"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestNetwork(t *testing.T) {
	ctx := context.Background()
	networkName := uuid.NewString()

	dockerClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	assert.NoError(t, err)

	containerClient := container.NewClient(dockerClient)
	networkService := network.NewService(containerClient)

	createdNetwork, err := networkService.CreateOrGetNetwork(context.Background(), networkName)
	assert.NoError(t, err)
	assert.NotNil(t, createdNetwork)

	err = networkService.RemoveNetwork(ctx, createdNetwork.ID)
	assert.NoError(t, err)
}
