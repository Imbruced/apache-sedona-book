package entity

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
	PostInitCommand    []string
	NetworkID          string
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
	OpenUrl *string
}
