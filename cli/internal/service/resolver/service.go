package resolver

import (
	"cli/internal/domain/entity"
	"cli/internal/infrastructure/config"
	"context"
	"fmt"
	"os"
	"strings"
)

const (
	dataDir   = "source_data"
	scriptDir = "scripts"
)

type Service struct {
}

func NewService() *Service {
	return &Service{}
}

func (s *Service) Resolve(ctx context.Context, request *entity.ResolveRequest) ([]*entity.ContainerRunRequest, error) {
	cfg, err := config.NewConfig(request.Chapter)
	if err != nil {
		return nil, err
	}

	requests := make([]*entity.ContainerRunRequest, 0, len(cfg.ChapterStructure.Images))
	structure := cfg.ChapterStructure
	if request.SubChapter != 0 {
		structure = structure.Sections[request.SubChapter-1]
	}

	images := s.resolveImages(structure)
	aggImages := s.aggregateImages(request.LoadData, images)

	for _, image := range aggImages {
		imageLocation := cfg.Images.Images[image.Image]

		exposedPorts := make(map[string]string, len(imageLocation.Ports))
		for _, port := range imageLocation.Ports {
			portParts := strings.Split(port, ":")
			if len(portParts) != 2 {
				continue
			}

			hostPort := portParts[0]
			containerPort := portParts[1]
			exposedPorts[hostPort] = containerPort
		}

		println("Image: ", imageLocation.MountPath)
		env := cfg.AppConfig.Env.ToMap()

		for envVar, envVarValue := range imageLocation.Environment {
			env[envVar] = envVarValue
		}

		requests = append(requests, &entity.ContainerRunRequest{
			Image:              imageLocation.Name,
			ContainerName:      "",
			Command:            imageLocation.Command,
			ExposedPorts:       exposedPorts,
			MountPathHost:      os.Getenv("SEDONA_DATA_HOME"),
			MountPathContainer: imageLocation.MountPath,
			MountFiles:         image.Volumes,
			EnvVariables:       env,
			HealthCheck: entity.HealthCheck{
				Test: imageLocation.HealthCheck.Test,
			},
			PostInitCommand: image.PostInitCommand,
		})
	}

	return requests, nil
}

func (s *Service) resolveImages(structure config.ChapterStructure) []config.ImageDependency {
	images := make([]config.ImageDependency, 0, len(structure.Images))

	images = append(images, structure.Images...)

	if len(structure.Sections) == 0 {
		return images
	}

	for _, section := range structure.Sections {
		images = append(images, s.resolveImages(section)...)
	}

	return images
}

func (s *Service) aggregateImages(loadData bool, images []config.ImageDependency) []config.ImageDependency {
	result := make([]config.ImageDependency, 0, len(images))
	seen := make(map[string]config.ImageDependency)
	for _, image := range images {
		currentElement, ok := seen[image.Image]

		if !ok {
			seen[image.Image] = image
			currentElement = image
		}

		currentElement.Volumes = getUniqueElements(append(
			currentElement.Volumes, s.resolveVolumes(loadData, image)...,
		))
		currentElement.PostInitCommand = getUniqueElements(append(currentElement.PostInitCommand, image.PostInitCommand...))
		currentElement.Scripts = getUniqueElements(append(currentElement.Scripts, image.Scripts...))

		seen[image.Image] = currentElement
	}

	for _, image := range seen {
		result = append(result, image)
	}

	return result
}

func (s *Service) resolveVolumes(loadData bool, deps config.ImageDependency) []string {
	volumes := make([]string, 0, len(deps.Volumes))

	for _, volume := range deps.Volumes {
		volumes = append(volumes, volume)
	}

	if loadData {
		for _, data := range deps.Data {
			volumes = append(volumes, fmt.Sprintf("%s/%s", dataDir, data))
		}

		for _, script := range deps.Scripts {
			volumes = append(volumes, fmt.Sprintf("%s/%s", scriptDir, script))
		}
	}

	return volumes
}

func getUniqueElements(elements []string) []string {
	uniqueElements := make(map[string]struct{})
	for _, element := range elements {
		uniqueElements[element] = struct{}{}
	}

	result := make([]string, 0, len(uniqueElements))
	for element := range uniqueElements {
		result = append(result, element)
	}

	return result
}
