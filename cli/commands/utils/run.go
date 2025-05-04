package utils

import "github.com/spf13/cobra"

type RunCommand interface {
	GetCobraCommand() *cobra.Command
}
