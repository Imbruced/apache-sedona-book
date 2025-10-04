package errors

import "errors"

var (
	ErrNetworkNotFound = errors.New("network not found")
	ErrImageNotFound   = errors.New("image not found")
)
