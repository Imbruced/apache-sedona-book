package resolver

import (
	"cli/internal/domain/entity"
	"github.com/stretchr/testify/assert"
	"slices"
	"testing"
)

func TestService_Resolve(t *testing.T) {
	tests := map[string]struct {
		request        *entity.ResolveRequest
		validateResult func(in []*entity.ContainerRunRequest) error
		expectedError  error
	}{
		"success: happy path full chapter 5": {
			request: &entity.ResolveRequest{
				Chapter:    entity.Chapter5,
				SubChapter: entity.SubChapter1,
			},
			validateResult: func(in []*entity.ContainerRunRequest) error {
				assert.Equal(t, 1, len(in))

				sedonaImage := getRunRequest(in, "sedona:1.7.2")
				assert.NotNil(t, sedonaImage)
				assert.Len(t, sedonaImage.MountFiles, 1)
				assert.Equal(t, []string{
					"chapter5/RasterModel.ipynb:/opt/workspace/RasterModel.ipynb",
				}, orderList(sedonaImage.MountFiles))

				return nil
			},
		},
		"success: should properly resolve for subchapter": {
			request: &entity.ResolveRequest{
				Chapter:    entity.Chapter5,
				LoadData:   true,
				SubChapter: 2,
			},
			validateResult: func(in []*entity.ContainerRunRequest) error {
				assert.Equal(t, 1, len(in))

				sedonaImage := getRunRequest(in, "sedona:1.7.2")
				assert.NotNil(t, sedonaImage)

				assert.Len(t, sedonaImage.MountFiles, 1)
				assert.Equal(t, []string{
					"chapter5/Raster SQL and Raster Data Manipulation.ipynb:/opt/workspace/Raster SQL and Raster Data Manipulation.ipynb",
				}, orderList(sedonaImage.MountFiles))

				return nil
			},
		},
	}

	for name, testCase := range tests {
		t.Run(name, func(t *testing.T) {
			containerRunRequest, err := resolver.Resolve(ctx, testCase.request)
			assert.ErrorIs(t, testCase.expectedError, err)

			if testCase.validateResult == nil {
				return
			}

			assert.NoError(t, testCase.validateResult(containerRunRequest))
		})
	}
}

func getRunRequest(requests []*entity.ContainerRunRequest, name string) *entity.ContainerRunRequest {
	for _, r := range requests {
		if r.Image == name {
			return r
		}
	}

	return nil
}

func orderList(l []string) []string {
	slices.Sort(l)
	return l
}
