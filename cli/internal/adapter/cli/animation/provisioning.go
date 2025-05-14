package animation

import (
	"context"
	"fmt"
	"time"
)

func Provisioning(ctx context.Context) {
	ticker := time.NewTicker(500 * time.Millisecond)
	defer ticker.Stop()

	done := ctx.Done()
	dots := 0
	timeEmojis := []string{"⏳", "⏳", "⌛", "⌛"}

	defer fmt.Print("\r                                \r")

	for {
		select {
		case <-done:
			return
		case <-ticker.C:
			dots = (dots + 1) % 4
			timeEmoji := timeEmojis[dots%4]
			dotText := ""
			for i := 0; i < dots; i++ {
				dotText += "."
			}

			fmt.Printf("\r%s %-3s", "provisioning", timeEmoji)
		}
	}
}
