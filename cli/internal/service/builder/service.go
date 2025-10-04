package builder

import (
	"cli/internal/domain/dto"
	"cli/internal/domain/entity"
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
	imageBuildChannel := make(map[string]bool)

	for _, img := range request.Images {
		imageBuildChannel[img.Image] = false
	}

	go func() {
		errChan := s.buildImages(ctx, request.Images.GetImagesNames(), imageBuildChannel)

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

func (s *Service) buildImages(ctx context.Context, images []*entity.ImageMeta, signals map[string]bool) chan error {
	errChan := make(chan error, 2)

	for _, img := range images {
		go func() {
			err := s.imageClient.Exists(ctx, img.Name, img.Tag)
			if err != nil && !errors.Is(err, domainerrors.ErrImageNotFound) {
				errChan <- err
				return
			}

			if err == nil {
				signals[img.FullName()] = true
				return
			}

			err = s.imageClient.BuildImage(ctx, img.Name, img.Tag)
			if err != nil {
				errChan <- err
				return
			}

			signals[img.FullName()] = true
		}()
	}

	return errChan
}
