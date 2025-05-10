package cli

import (
	"cli/internal/adapter/cli/transform"
	"cli/internal/domain/entity"
	"context"
	"github.com/spf13/cobra"
)

type ContainerService interface {
	ListContainers(ctx context.Context) ([]*entity.ContainerMetadata, error)
	Clear(ctx context.Context) error
	StartContainers(ctx context.Context, request *entity.RunPreRequisiteRequest) error
}

type Client struct {
	containerService ContainerService
}

func NewClient(containerService ContainerService) *Client {
	return &Client{
		containerService: containerService,
	}
}

func (c *Client) GetCommands() []*cobra.Command {
	return []*cobra.Command{
		c.listContainers(context.Background()),
		c.clear(context.Background()),
		c.provision(context.Background()),
	}
}

func (c *Client) clear(ctx context.Context) *cobra.Command {
	var command = &cobra.Command{
		Use:  "clear",
		Args: cobra.NoArgs,
	}

	command.Run = func(cmd *cobra.Command, args []string) {
		err := c.containerService.Clear(ctx)
		if err != nil {
			cmd.PrintErrf("Error clearing containers: %v\n", err)
			return
		}

		cmd.Println("Containers cleared successfully.")
	}

	return command
}

func (c *Client) listContainers(ctx context.Context) *cobra.Command {
	var command = &cobra.Command{
		Use:  "list",
		Args: cobra.NoArgs,
	}

	command.Run = func(cmd *cobra.Command, args []string) {
		containers, err := c.containerService.ListContainers(ctx)
		if err != nil {
			cmd.PrintErrf("Error listing containers: %v\n", err)
		}

		for _, container := range containers {
			cmd.Printf("Container ID: %s, Name: %s, State: %s\n", container.ID, container.Name, container.State)
		}
	}

	return command
}

func (c *Client) provision(ctx context.Context) *cobra.Command {
	var chapter string
	var copyData bool
	var subChapter int

	var command = &cobra.Command{
		Use:  "provision",
		Args: cobra.NoArgs,
	}

	command.Flags().StringVarP(&chapter, "chapter", "c", "", "Chapter to provision")
	command.Flags().Bool("copy", copyData, "Copy the data to minio bucket if applicable")
	command.Flags().IntVarP(&subChapter, "sub-chapter", "s", 0, "Selected Sub chapter, if empty full chapter will be provisioned")

	command.Run = func(cmd *cobra.Command, args []string) {
		var chapterDomain entity.Chapter

		if chapter != "" {
			chapterDomainRaw, err := transform.ChapterToDomain(chapter)
			if err != nil {
				command.PrintErrf("Error transforming chapter: %v\n", err)
				return
			}

			chapterDomain = chapterDomainRaw
		}

		err := c.containerService.StartContainers(ctx, &entity.RunPreRequisiteRequest{
			Chapter:    chapterDomain,
			SubChapter: entity.SubChapter(subChapter),
			CopyData:   copyData,
		})
		if err != nil {
			cmd.PrintErrf("Error starting containers: %v\n", err)
			return
		}

		cmd.Println("Containers started successfully.")
	}

	return command
}
