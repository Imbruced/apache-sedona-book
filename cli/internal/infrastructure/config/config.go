package config

type AppConfig struct {
	Data DataConfig
	Env  EnvConfigs
}

type EnvConfigs []EnvConfig

func (e EnvConfigs) ToMap() map[string]string {
	envMap := make(map[string]string, len(e))
	for _, env := range e {
		envMap[env.Name] = env.Value
	}
	return envMap
}

type EnvConfig struct {
	Name  string
	Value string
}

type DataConfig struct {
	Copy bool `yaml:"copy"`
}

type ImagesConfig struct {
	Images map[string]Image
}

type HealthCheckConfig struct {
	Test []string `yaml:"test"`
}

type Image struct {
	Name            string
	Command         []string
	Ports           []string
	MountPath       string            `yaml:"mount-path"`
	Environment     map[string]string `yaml:"environment"`
	HealthCheck     HealthCheckConfig `yaml:"health-check"`
	ShowInBrowser   bool              `yaml:"show-in-browser"`
	BrowserOpenPath string            `yaml:"browser-open-path"`
}

type ImageDependency struct {
	Image           string
	Scripts         []string
	Volumes         []string
	PostInitCommand []string `yaml:"post-init-command"`
	Data            []string
	BrowserPath     string `yaml:"browser-path"`
}
type ChapterStructure struct {
	Title    string
	ID       string
	Sections []ChapterStructure
	Images   []ImageDependency
}

type Config struct {
	ChapterStructure ChapterStructure
	Images           ImagesConfig
	AppConfig        AppConfig
}
