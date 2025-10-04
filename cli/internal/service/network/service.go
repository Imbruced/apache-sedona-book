package network

import (
	"cli/internal/domain/entity"
	domainerrors "cli/internal/domain/errors"
	"context"
	"errors"
	"time"
)

const (
	SedonaNetworkName   = "sedona"
	SedonaLabelName     = "sedona"
	HealthCheckTimeout  = 120 * time.Second
	HealthCheckTickTime = time.Second * 2
)

type Client interface {
	CreateNetwork(ctx context.Context, request *entity.CreateNetworkRequest) (*entity.CreateNetworkResponse, error)
	RemoveNetwork(ctx context.Context, networkID string) error
	GetNetworkID(ctx context.Context, networkName string) (*entity.Network, error)
}

type Service struct {
	client Client
}

func NewService(client Client) *Service {
	return &Service{
		client: client,
	}
}

func (s *Service) CreateOrGetNetwork(ctx context.Context, networkName string) (*entity.Network, error) {
	network, err := s.client.GetNetworkID(ctx, networkName)
	if err == nil {
		return network, nil
	}

	if !errors.Is(err, domainerrors.ErrNetworkNotFound) {
		return nil, err
	}

	networkResponse, err := s.client.CreateNetwork(ctx, &entity.CreateNetworkRequest{
		Name: networkName,
	})
	if err != nil {
		return nil, err
	}

	return &entity.Network{
		ID: networkResponse.ID,
	}, nil
}

func (s *Service) RemoveNetwork(ctx context.Context, networkID string) error {
	return s.client.RemoveNetwork(ctx, networkID)
}
