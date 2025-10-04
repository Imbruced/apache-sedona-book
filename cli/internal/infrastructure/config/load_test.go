package config

import (
	"cli/internal/domain/entity"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestNewConfig(t *testing.T) {
	config, err := NewConfig(entity.Chapter3)
	assert.NoError(t, err)
	assert.NotNil(t, config)
}

func TestLoadingConfig(t *testing.T) {
	tests := map[string]struct {
		chapter        entity.Chapter
		validateConfig func(config *Config)
	}{
		"successful: chapter 3": {
			chapter: entity.Chapter3,
			validateConfig: func(config *Config) {
				assert.Len(t, config.Images.Images, 13)
				assert.Len(t, config.ChapterStructure.Sections, 4)
			},
		},
		"successful: chapter 4": {
			chapter: entity.Chapter4,
			validateConfig: func(config *Config) {
				assert.Len(t, config.Images.Images, 13)
				assert.Len(t, config.ChapterStructure.Sections, 5)
			},
		},
	}

	for testName, testCase := range tests {
		t.Run(string(testName), func(t *testing.T) {
			cfg, err := NewConfig(testCase.chapter)
			assert.NoError(t, err)
			assert.NotNil(t, cfg)
			testCase.validateConfig(cfg)
		})
	}
}
