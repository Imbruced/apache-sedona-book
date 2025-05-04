package container

import (
	"context"
	"os"
	"testing"
)

var (
	ctx context.Context
)

func TestMain(m *testing.M) {
	ctx = context.Background()
	os.Exit(m.Run())
}
