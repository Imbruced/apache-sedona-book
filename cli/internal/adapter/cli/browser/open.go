package browser

import (
	"os/exec"
)

func Open(url string) {
	err := exec.Command("open", "-a", "Google Chrome", url).Run()
	if err != nil {
		return
	}
}
