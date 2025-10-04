package dto

import (
	"cli/internal/domain/entity"
	"sort"
	"sync"
)

type ProvisionRequest struct {
	Chapter    entity.Chapter
	SubChapter entity.SubChapter
}

type StartContainersRequest struct {
	OpenUrl        *string
	OpenTerminal   func() error
	BuildingImages map[string]bool
	StartingImages map[string]bool
	NetworkID      string
	Images         entity.ContainerRunRequests
	Errors         chan error
	lock           sync.Mutex
}

func (s *StartContainersRequest) UpdateBuildImageStatus(image string, ready bool) {
	s.lock.Lock()
	defer s.lock.Unlock()
	s.BuildingImages[image] = ready
}

func (s *StartContainersRequest) UpdateContainerStatus(image string, ready bool) {
	s.lock.Lock()
	defer s.lock.Unlock()
	s.StartingImages[image] = ready
}

func (s *StartContainersRequest) GetAllImages() []*entity.ImageReady {
	result := make([]*entity.ImageReady, 0, len(s.BuildingImages))
	for image, ready := range s.BuildingImages {
		result = append(result, &entity.ImageReady{
			Image: image,
			Ready: ready,
		})
	}

	sort.Slice(result, func(i, j int) bool {
		return result[i].Image < result[j].Image
	})

	return result
}
