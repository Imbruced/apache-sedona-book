package config

type ImagesConfig struct {
	Images map[string]Image
}

type HealthCheckConfig struct {
	Test []string `yaml:"test"`
}

type Image struct {
	Name        string
	Command     []string
	Ports       []string
	MountPath   string            `yaml:"mount-path"`
	Environment map[string]string `yaml:"environment"`
	HealthCheck HealthCheckConfig `yaml:"health-check"`
}

type ImageDependency struct {
	Image           string
	Scripts         []string
	Volumes         []string
	PostInitCommand []string `yaml:"post-init-command"`
	Data            []string
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
}
