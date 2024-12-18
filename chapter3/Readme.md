# Sedona Vector Data loading

## Pre-requisites
- Install uv python package manager

## How to run
- Run the following command in the terminal
```bash
# starts docker compose with all the infra
./start-containers.sh

# run migrations, table create and data load
./start.sh

# start jupyter notebook
uv run jupyter notebook
```

To stop everything, run the following command
```bash
./stop-containers.sh
```
