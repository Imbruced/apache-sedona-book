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
