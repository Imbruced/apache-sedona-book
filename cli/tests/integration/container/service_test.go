package container

import (
	containerClient "cli/internal/adapter/client/container"
	"cli/internal/domain/dto"
	"cli/internal/domain/entity"
	"cli/internal/service/network"
	"cli/internal/service/resolver"
	"cli/internal/service/run"
	"context"
	"fmt"
	"github.com/docker/docker/client"
	"github.com/stretchr/testify/assert"
	"net/http"
	"os"
	"testing"
	"time"
)

func TestContainerService(t *testing.T) {
	startChapter(t, entity.Chapter3, entity.SubChapter2, func(request *dto.StartContainersRequest) {
		assert.Equal(t, "http://localhost:8888/lab/workspaces/auto-R/tree/LoadingRasterData.ipynb", *request.OpenUrl)

		resp, err := http.Get("http://localhost:8888")
		if err != nil {
			fmt.Println("Error:", err)
			return
		}
		defer resp.Body.Close()

		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, resp.StatusCode)
	})
	startChapter(t, entity.Chapter3, entity.SubChapter3, func(request *dto.StartContainersRequest) {
		assert.Equal(t, "http://localhost:8888/lab/workspaces/auto-R/tree/ReadingFromPostgreSQL.ipynb", *request.OpenUrl)

		resp, err := http.Get("http://localhost:8888")
		if err != nil {
			fmt.Println("Error:", err)
			return
		}
		defer resp.Body.Close()

		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, resp.StatusCode)
	})
}

func startChapter(t *testing.T, chapter entity.Chapter, subChapter entity.SubChapter, verifyState func(request *dto.StartContainersRequest)) {
	ctx := context.Background()
	os.Setenv("SEDONA_DATA_HOME", "/Users/pawelkocinski/Desktop/projects/sedona-book/apache-sedona-book/book")
	imageResolver := resolver.NewService()

	images, err := imageResolver.Resolve(ctx, &entity.ResolveRequest{
		Chapter:    chapter,
		SubChapter: subChapter,
	})

	assert.NoError(t, err)
	assert.NotEmpty(t, images)

	dockerClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	assert.NoError(t, err)

	c := containerClient.NewContainer(dockerClient)

	containerProvisioner := run.NewService(c)

	networkService := network.NewService(c)

	n, err := networkService.CreateOrGetNetwork(ctx, "test-network")
	assert.NoError(t, err)
	assert.NotNil(t, n)

	request := &dto.StartContainersRequest{
		BuildingImages: make(map[string]bool),
		StartingImages: make(map[string]bool),
		NetworkID:      n.ID,
		Images:         images,
	}

	err = containerProvisioner.RunContainers(ctx, request)
	numberOfImages := len(request.Images)
	time.Sleep(time.Millisecond * 200)
	assert.Equal(t, numberOfImages, len(request.StartingImages))
	assert.NoError(t, err)

	for {
		numberOfStarted := 0
		for imageName, isReady := range request.StartingImages {
			println(fmt.Sprintf("Image: %s, isReady: %t", imageName, isReady))
			if isReady {
				numberOfStarted++
			}
		}

		time.Sleep(time.Second * 2)

		if numberOfStarted == numberOfImages {
			break
		}
	}

	verifyState(request)

	err = containerProvisioner.Clear(ctx)
	assert.NoError(t, err)
}
