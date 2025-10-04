package resolve

import (
	"cli/internal/domain/entity"
	"cli/internal/service/resolver"
	"context"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestService_ResolveURL(t *testing.T) {
	tests := map[string]struct {
		input    *entity.ResolveRequest
		expected string
	}{
		"successful: resolve URL chapter 3, sub chapter 3": {
			input: &entity.ResolveRequest{
				Chapter:    entity.Chapter3,
				SubChapter: entity.SubChapter3,
			},
			expected: "http://localhost:8888/lab/workspaces/auto-R/tree/ReadingFromPostgreSQL.ipynb",
		},
	}

	for testName, testCase := range tests {
		t.Run(testName, func(t *testing.T) {
			imageResolver := resolver.NewService()

			resolved, err := imageResolver.Resolve(context.Background(), testCase.input)
			assert.NoError(t, err)

			resolvedURL := resolved.ResolveURL()
			assert.NotEmpty(t, resolvedURL)
			assert.Equal(t, testCase.expected, *resolvedURL)
		})
	}
}
