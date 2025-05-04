package main

import (
	"cli/internal/adapter/cli"
	containerClient "cli/internal/adapter/client/container"
	"cli/internal/service/container"
	"cli/internal/service/resolver"
	"github.com/docker/docker/client"
	"github.com/spf13/cobra"
)

func main() {
	dockerClient, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {

	}

	containerClient := containerClient.NewContainer(dockerClient)
	resolverService := resolver.NewService()

	containerService := container.NewService(containerClient, resolverService)
	cliClient := cli.NewClient(containerService)
	commands := cliClient.GetCommands()

	var rootCmd = &cobra.Command{Use: "sedona"}

	for _, cmd := range commands {
		rootCmd.AddCommand(cmd)
	}

	if err = rootCmd.Execute(); err != nil {
		rootCmd.PrintErrf("Error executing command: %v\n", err)
		return
	}
}
