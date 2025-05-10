package resolver

import (
	"context"
	"os"
	"testing"
)

var (
	ctx      context.Context
	resolver *Service
)

func TestMain(m *testing.M) {
	code := m.Run()

	resolver = NewService()

	os.Exit(code)
}
