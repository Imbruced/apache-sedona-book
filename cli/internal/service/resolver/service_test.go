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
				Chapter:  entity.Chapter5,
				LoadData: true,
			},
			validateResult: func(in []*entity.ContainerRunRequest) error {
				assert.Equal(t, 2, len(in))

				sedonaImage := getRunRequest(in, "apache/sedona:1.7.1")
				assert.NotNil(t, sedonaImage)
				assert.Len(t, sedonaImage.MountFiles, 7)
				assert.Equal(t, []string{
					"chapter5/MapAlgebra.ipynb",
					"chapter5/Raster SQL and Raster Data Manipulation.ipynb",
					"chapter5/RasterJoin.ipynb",
					"chapter5/RasterModel.ipynb",
					"chapter5/Use Case Insurance Risk Modeling.ipynb",
					"chapter5/Zonal Statistics.ipynb",
					"chapter5/images",
				}, orderList(sedonaImage.MountFiles))

				minioImage := getRunRequest(in, "quay.io/minio/minio:latest")
				assert.NotNil(t, minioImage)
				assert.Len(t, minioImage.MountFiles, 12)
				assert.Equal(t, []string{
					"scripts/copy_minio.sh", "source_data/buildings",
					"source_data/fdi_data", "source_data/fire_risk",
					"source_data/flood", "source_data/infrastructure",
					"source_data/nir_b08_tiles", "source_data/ny_rail_road_and_aviation_noise",
					"source_data/ny_redfin_sold_offers", "source_data/places",
					"source_data/swir_b11_tiles", "source_data/world_population_raster",
				}, orderList(minioImage.MountFiles))

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

				sedonaImage := getRunRequest(in, "apache/sedona:1.7.1")
				assert.NotNil(t, sedonaImage)

				assert.Len(t, sedonaImage.MountFiles, 2)
				assert.Equal(t, []string{
					"chapter5/Raster SQL and Raster Data Manipulation.ipynb", "chapter5/images",
				}, orderList(sedonaImage.MountFiles))

				return nil
			},
		},
		"success: load data is turned off": {
			request: &entity.ResolveRequest{
				Chapter:    entity.Chapter5,
				LoadData:   false,
				SubChapter: 4,
			},
			validateResult: func(in []*entity.ContainerRunRequest) error {
				assert.Equal(t, 2, len(in))

				minioImage := getRunRequest(in, "quay.io/minio/minio:latest")
				assert.NotNil(t, minioImage)

				assert.Equal(t, []string{}, orderList(minioImage.MountFiles))

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
