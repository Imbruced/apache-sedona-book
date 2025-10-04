build-cli:
	(cd cli; go build -o sedona ./cmd)

run-cli:
	(cd cli; go run ./cmd)
