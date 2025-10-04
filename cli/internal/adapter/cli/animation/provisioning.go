package animation

import (
	"cli/internal/domain/dto"
	"cli/internal/domain/entity"
	"context"
	"fmt"
	"strings"
	"time"
)

func Provisioning(ctx context.Context, provisioningInterval time.Duration) {
	ticker := time.NewTicker(provisioningInterval)
	defer ticker.Stop()

	dots := 0
	timeEmojis := []string{"⏳", "⏳", "⌛", "⌛"}

	defer fmt.Print("\r                                \r")

	for {
		select {
		case <-ctx.Done():
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

func BuildingImages(ctx context.Context, images *dto.StartContainersRequest) {
	ticker := time.NewTicker(500 * time.Millisecond)
	defer ticker.Stop()

	done := ctx.Done()
	dots := 0
	timeEmojis := []string{"⏳", "⏳", "⌛", "⌛"}

	emojiText := ""

	for {
		select {
		case <-done:
			fmt.Printf("\r %-3s", emojiText)
			return
		case <-ticker.C:
			dots = (dots + 1) % 4
			timeEmoji := timeEmojis[dots%4]
			emojiText = createImagesStatusText(images.GetAllImages(), timeEmoji)

			fmt.Printf("\r %-3s", emojiText)
			clearLines(len(strings.Split(emojiText, "\n")) - 1)
		}
	}
}

func clearLines(n int) {
	for i := 0; i < n; i++ {
		fmt.Print("\033[A")
	}
}

func createImagesStatusText(images []*entity.ImageReady, buildingIcon string) string {
	statusText := "Building images:\n"
	for _, el := range images {
		status := buildingIcon
		if el.Ready {
			status = "✅"
		}

		statusText += fmt.Sprintf("  %s %s\n", status, el.Image)
	}

	return statusText
}
