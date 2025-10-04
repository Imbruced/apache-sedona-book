package config

import (
	"cli/internal/domain/entity"
	"embed"
	"fmt"
	"github.com/goccy/go-yaml"
	"os"
	"path/filepath"
	"runtime"
)

//go:embed chapters/*.yaml
var configChapters embed.FS

func NewConfig(chapter entity.Chapter) (*Config, error) {
	cfg := Config{}
	var chapterStructure ChapterStructure
	var Images ImagesConfig
	var appConfig AppConfig

	_, b, _, _ := runtime.Caller(0)
	rootPath := filepath.Dir(b)

	imageConfigPath := fmt.Sprintf(
		"%s/images/image.yaml",
		rootPath,
	)

	chapterConfigPath := fmt.Sprintf(
		"chapters/%s.yaml",
		resolveChapter(chapter),
	)

	appConfigPath := fmt.Sprintf(
		"%s/config.yaml",
		rootPath,
	)

	chapterConfigContent, err := configChapters.ReadFile(chapterConfigPath)
	if err != nil {
		return nil, err
	}

	if err = yaml.Unmarshal(chapterConfigContent, &chapterStructure); err != nil {
		return nil, err
	}

	imageConfigContent, err := os.ReadFile(imageConfigPath)
	if err != nil {
		return nil, err
	}

	if err = yaml.Unmarshal(imageConfigContent, &Images); err != nil {
		return nil, err
	}

	appConfigContent, err := os.ReadFile(appConfigPath)
	if err != nil {
		return nil, err
	}

	replaced := os.ExpandEnv(string(appConfigContent))

	if err = yaml.Unmarshal([]byte(replaced), &appConfig); err != nil {
		return nil, err
	}

	cfg.ChapterStructure = chapterStructure
	cfg.Images = Images
	cfg.AppConfig = appConfig

	return &cfg, nil
}

func resolveChapter(chapter entity.Chapter) string {
	switch chapter {
	case entity.Chapter1:
		return "chapter1"
	case entity.Chapter2:
		return "chapter2"
	case entity.Chapter3:
		return "chapter3"
	case entity.Chapter4:
		return "chapter4"
	case entity.Chapter5:
		return "chapter5"
	case entity.Chapter6:
		return "chapter6"
	case entity.Chapter7:
		return "chapter7"
	case entity.Chapter8:
		return "chapter8"
	case entity.Chapter9:
		return "chapter9"
	case entity.Chapter10:
		return "chapter10"
	default:
		return ""
	}
}
