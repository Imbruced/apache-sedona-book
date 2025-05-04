package config

import (
	"cli/internal/domain/entity"
	"fmt"
	"github.com/goccy/go-yaml"
	"os"
	"path/filepath"
	"runtime"
)

func NewConfig(chapter entity.Chapter) (*Config, error) {
	cfg := Config{}
	var chapterStructure ChapterStructure
	var Images ImagesConfig

	_, b, _, _ := runtime.Caller(0)
	rootPath := filepath.Dir(b)

	imageConfigPath := fmt.Sprintf(
		"%s/images/image.yaml",
		rootPath,
	)

	chapterConfigPath := fmt.Sprintf(
		"%s/chapters/%s.yaml",
		rootPath,
		resolveChapter(chapter),
	)

	chapterConfigContent, err := os.ReadFile(chapterConfigPath)
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

	cfg.ChapterStructure = chapterStructure
	cfg.Images = Images

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
	default:
		return ""
	}
}
