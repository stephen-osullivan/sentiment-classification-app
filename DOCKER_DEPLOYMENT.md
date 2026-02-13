# Docker Deployment Guide

This guide explains how to deploy the sentiment classification application using Docker. The deployment consists of two main components: a training pipeline (using DVC) and a FastAPI application.

## Prerequisites

- Docker and Docker Compose installed
- All dependencies locked in `uv.lock`

## Project Structure

- `Dockerfile.train`: Container for running the DVC pipeline to train the model
- `Dockerfile.api`: Container for running the FastAPI application
- `docker-compose.yml`: Orchestrates both services
- `.dockerignore`: Excludes unnecessary files from Docker build context

## Quick Start (Both Services)

To build and run both the training pipeline and FastAPI app together:

```bash
docker-compose up --build
```

This will:
1. Build both images
2. Start the training service to train the model (if needed)
3. Start the API service with the trained model
4. Expose the API on `http://localhost:8000`

## Command 1: Train the Model

### Using Docker Compose (Recommended)

Build and run just the training service:

```bash
docker-compose build train
docker-compose run --rm train
```

## Command 2: Launch the FastAPI App

### Option A: Using Docker Compose (Recommended)

Once training is complete, run the API service:

```bash
docker-compose up api
```

## Usage Examples

### Test the API with cURL

Once the API is running, test it with a prediction request:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This movie was absolutely amazing"}'
```

Expected response:
```json
{"label":"positive","confidence":0.7296}
```

### View API Documentation

Open your browser and navigate to:
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Container Details

### Training Container (`sentiment-train`)

**Purpose**: Runs the DVC pipeline to download data, process it, train the model, and evaluate

**Volume Mounts**:
- `./data:/app/data` - Raw and processed data
- `./artifacts:/app/artifacts` - Trained model and metrics

**Environment**: 
- Uses the frozen `uv.lock` file for reproducible environments
- Builds on Python 3.12 slim image

### API Container (`sentiment-api`)

**Purpose**: Serves the trained model via FastAPI

**Volume Mounts**:
- `./artifacts:/app/artifacts` - Loads the trained model
- `./src:/app/src` - Sentiment processing utilities

**Environment**:
- Exposes port 8000
- Loads model on startup
- Gracefully handles shutdown

**Dependencies**:
- In `docker-compose.yml`, the API depends on the train service (will wait for training to complete)

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, modify `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "8001:8000"  # Map to port 8001 instead
```

### Model Not Found

Ensure the training pipeline has completed and the model exists at `artifacts/sentiment_model.joblib`

### View Logs

For API logs:
```bash
docker-compose logs -f api
```

For training logs:
```bash
docker-compose logs -f train
```

### Clean Up

Stop and remove all containers:

```bash
docker-compose down
```

Remove all images:

```bash
docker-compose down --rmi all
```

## Production Considerations

1. **Use specific image tags** instead of `latest` for reproducibility
2. **Separate volumes** for training and inference to avoid conflicts
3. **Health checks** can be added to services
4. **Environment variables** for configuration (model paths, API settings)
5. **Logging** should be configured for monitoring
6. **Resource limits** should be set based on your infrastructure

Example production docker-compose snippet:

```yaml
services:
  api:
    image: sentiment-api:v1.0.0
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DVC Documentation](https://dvc.org/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [uv Package Manager](https://docs.astral.sh/uv/)
