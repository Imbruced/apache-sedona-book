package animation

import (
	"bytes"
	"context"
	"github.com/stretchr/testify/assert"
	"io"
	"os"
	"testing"
	"time"
)

func captureOutput(f func()) string {
	// save the original stdout
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// run the function that prints to stdout
	f()

	// restore stdout
	w.Close()
	os.Stdout = old

	var buf bytes.Buffer
	io.Copy(&buf, r)
	return buf.String()
}

func TestProvisioning(t *testing.T) {
	ctx := context.Background()
	ctx, cancel := context.WithTimeout(ctx, time.Second*1)
	defer cancel()

	output := captureOutput(func() {
		Provisioning(ctx, 50*time.Millisecond)
	})
	assert.Contains(t, output, "⏳")
	assert.Contains(t, output, "⏳")
	assert.Contains(t, output, "⌛")
	assert.Contains(t, output, "⌛")
}
