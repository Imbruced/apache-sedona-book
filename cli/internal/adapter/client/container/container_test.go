package container

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/docker/docker/client"
	"github.com/stretchr/testify/assert"
	"io"
	"io/ioutil"
	"log"
	"strings"
	"sync"
	"testing"
)

func TestContainer_ListContainers(t *testing.T) {
	cli, err := client.NewClientWithOpts(
		client.FromEnv,
		client.WithAPIVersionNegotiation(),
	)
	assert.NoError(t, err)

	containerClient := NewContainer(cli)
	containers, err := containerClient.ListContainers(ctx)
	assert.NoError(t, err)
	println(len(containers))
}

func Test(t *testing.T) {
	cfg, err := config.LoadDefaultConfig(context.TODO(),
		config.WithRegion("us-west-2"),
	)
	if err != nil {
		log.Fatalf("unable to load SDK config, %v", err)
	}

	s3Client := s3.NewFromConfig(cfg)

	res, err := s3Client.ListObjectsV2(context.Background(), &s3.ListObjectsV2Input{
		Bucket: aws.String("overturemaps-us-west-2"),
		Prefix: aws.String("release/2025-04-23.0/theme=buildings/type=building"),
	}, func(options *s3.Options) {
		options.Credentials = nil
	})
	if err != nil {
		log.Fatalf("failed to list objects, %v", err)
	}

	dataToDownload := make([]string, 0)
	for _, obj := range res.Contents {
		if *obj.Size < 381816518 {
			dataToDownload = append(dataToDownload, *obj.Key)
		}
	}

	wg := sync.WaitGroup{}
	wg.Add(len(dataToDownload))

	for _, obj := range dataToDownload {
		println(obj)
		go func(obj string) {
			defer wg.Done()
			data, err := s3Client.GetObject(context.Background(), &s3.GetObjectInput{
				Bucket: aws.String("overturemaps-us-west-2"),
				Key:    aws.String(obj),
			}, func(options *s3.Options) {
				options.Credentials = nil
			})
			if err != nil {
				println(err.Error())
				return
			}

			bodyBytes, err := io.ReadAll(data.Body)
			if err != nil {
				println(err.Error())
				return
			}

			defer data.Body.Close()

			println("Size:", len(bodyBytes))

			fileName := obj[strings.LastIndex(obj, "/")+1:]
			err = ioutil.WriteFile(fileName, bodyBytes, 0644)
			if err != nil {
				println(err.Error())
			}

			println("Downloaded:", fileName)

		}(obj)

	}

	wg.Wait()

	println(len(res.Contents))
}
