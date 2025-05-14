package animation

import (
	"context"
	"fmt"
	"time"
)

func BroomSweepMultipleAnimation(ctx context.Context) {
	frames := []string{
		"🧹  ",
		" 🧹 ",
		"  🧹",
		"  🧹",
		" 🧹 ",
		"🧹  ",
	}

	tickerInterval := 250 * time.Millisecond
	ticker := time.NewTicker(tickerInterval)
	defer ticker.Stop()

	done := ctx.Done()
	index := 0

	defer fmt.Print("\r                                \r")

	for {
		select {
		case <-done:
			return
		case <-ticker.C:
			index = (index + 1) % len(frames)
			fmt.Printf("\r%s %s", frames[index], "clearing")
		}
	}
}
