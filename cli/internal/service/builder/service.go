package builder

import (
	"cli/internal/domain/dto"
	domainerrors "cli/internal/domain/errors"
	"context"
	"errors"
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

	go func() {
		errChan := s.buildImages(ctx, request)

		for {
			select {
			case <-ctx.Done():
				return
			case err := <-errChan:
				if err != nil {
					break
				}
			}
		}
	}()
	return nil
}

func (s *Service) buildImages(ctx context.Context, request *dto.StartContainersRequest) chan error {
	errChan := make(chan error, 2)

	for _, img := range request.Images.GetImagesNames() {
		go func() {
			err := s.imageClient.Exists(ctx, img.Name, img.Tag)
			if err != nil && !errors.Is(err, domainerrors.ErrImageNotFound) {
				errChan <- err
				return
			}

			if err == nil {
				request.UpdateBuildImageStatus(img.FullName(), true)
				return
			}

			err = s.imageClient.BuildImage(ctx, img.Name, img.Tag)
			if err != nil {
				errChan <- err
				return
			}

			request.UpdateBuildImageStatus(img.FullName(), true)
		}()
	}

	return errChan
}
