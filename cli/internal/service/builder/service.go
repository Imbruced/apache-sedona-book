package builder

import (
	"cli/internal/domain/dto"
	domainerrors "cli/internal/domain/errors"
	"context"
	"errors"
	"sync"
)

type ImageClient interface {
	BuildImage(ctx context.Context, image, tag string) error
	Exists(ctx context.Context, image, tag string) error
}

type Service struct {
	imageClient ImageClient
}

func NewService() *Service {
	return &Service{}
}

func (s *Service) WithImageClient(imageClient ImageClient) *Service {
	s.imageClient = imageClient
	return s
}

func (s *Service) Build(ctx context.Context, request *dto.StartContainersRequest) error {
	for _, img := range request.Images {
		request.UpdateBuildImageStatus(img.Image, false)
	}

	err := s.buildImages(ctx, request)
	if err != nil {
		return err
	}

	return nil
}

func (s *Service) buildImages(ctx context.Context, request *dto.StartContainersRequest) error {
	var wg sync.WaitGroup

	for _, img := range request.Images.GetImagesNames() {
		wg.Add(1)

		go func() {
			defer wg.Done()
			err := s.imageClient.Exists(ctx, img.Name, img.Tag)
			if err != nil && !errors.Is(err, domainerrors.ErrImageNotFound) {
				return
			}

			if err == nil {
				request.UpdateBuildImageStatus(img.FullName(), true)
				return
			}

			err = s.imageClient.BuildImage(ctx, img.Name, img.Tag)
			if err != nil {
				return
			}

			request.UpdateBuildImageStatus(img.FullName(), true)
		}()
	}

	wg.Wait()

	return nil
}
