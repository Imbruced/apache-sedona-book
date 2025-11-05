package entity

import (
	"sort"
	"strings"
)

type ContainerMetadata struct {
	ID    string
	Name  string
	State string
}

type EnvVariables map[string]string

func (e EnvVariables) ToEnvList() []string {
	envList := make([]string, 0, len(e))
	for key, value := range e {
		envList = append(envList, key+"="+value)
	}
	return envList
}

type HealthCheck struct {
	Test []string
}

type ImageMeta struct {
	Name string
	Tag  string
}

func (img *ImageMeta) FullName() string {
	return img.Name + ":" + img.Tag
}

type ContainerRunRequest struct {
	Image              string
	ContainerName      string
	Command            []string
	ExposedPorts       map[string]string
	MountPathHost      string
	MountPathContainer string
	MountFiles         []string
	EnvVariables       EnvVariables
	HealthCheck        HealthCheck
	NetworkID          string
	ShowInBrowser      bool
	BrowserOpenPath    string
	OpenTerminal       bool
	OpenWebUI          *OpenWebUIConfig
}

type ContainerRunRequests []*ContainerRunRequest

func (c ContainerRunRequests) GetImagesNames() []*ImageMeta {
	result := make([]*ImageMeta, 0, len(c))

	for _, req := range c {
		parts := strings.Split(req.Image, ":")
		if len(parts) != 2 {
			continue
		}

		imageName := parts[0]
		imageTag := parts[1]

		result = append(result, &ImageMeta{
			Name: imageName,
			Tag:  imageTag,
		})
	}

	return result
}

func (c ContainerRunRequests) ResolveURL() *string {
	for _, req := range c {
		if req.OpenWebUI != nil && req.OpenWebUI.Path != "" {
			return &req.OpenWebUI.Path
		}
	}

	return nil
}

type OpenWebUIConfig struct {
	Path string
}

type CreateContainerResponse struct {
	ID string
}

type RunPreRequisiteRequest struct {
	Chapter    Chapter
	SubChapter SubChapter
	CopyData   bool
}

type CreateNetworkRequest struct {
	Name string
}

type CreateNetworkResponse struct {
	ID string
}

type Network struct {
	ID string
}

type StartContainerResponse struct {
	OpenUrl        *string
	OpenTerminal   func() error
	BuildingImages map[string]bool
	StartingImages map[string]bool
	StartedImages  bool
}

type ImageReady struct {
	Image string
	Ready bool
}

func (s *StartContainerResponse) GetAllImages() []*ImageReady {
	result := make([]*ImageReady, 0, len(s.BuildingImages))
	for image, ready := range s.BuildingImages {
		result = append(result, &ImageReady{
			Image: image,
			Ready: ready,
		})
	}

	sort.Slice(result, func(i, j int) bool {
		return result[i].Image < result[j].Image
	})

	return result
}
