# Docker Deployment Guide for NayDoeV1

This guide provides detailed instructions for deploying NayDoeV1 using Docker.

## Quick Start

### Option 1: Docker CLI

```bash
# Build the image
docker build -t naydoev1:latest .

# Run interactively
docker run -it --rm naydoev1:latest

# Run with persistent data
docker run -it --rm -v naydoev1-data:/app/data naydoev1:latest
```

### Option 2: Docker Compose (Recommended)

```bash
# Start the service
docker compose up -d

# View logs
docker compose logs -f

# Stop the service
docker compose down
```

## Image Details

- **Base Image**: python:3.11-slim
- **Final Size**: ~125MB
- **User**: naydoe (non-root)
- **Working Directory**: /app
- **Data Directory**: /app/data (for persistent storage)

## Configuration

### Environment Variables

The following environment variables are pre-configured for optimal performance:

- `PYTHONDONTWRITEBYTECODE=1` - Prevents Python from writing .pyc files
- `PYTHONUNBUFFERED=1` - Ensures immediate output logging
- `PYTHONOPTIMIZE=1` - Enables Python optimizations

### Volume Mounts

#### Data Volume
Mount `/app/data` for persistent rollback marker storage:

```bash
docker run -v naydoev1-data:/app/data naydoev1:latest
```

#### Custom Configuration
Mount a custom config.json (optional):

```bash
docker run -v ./custom-config.json:/app/config.json:ro naydoev1:latest
```

## Resource Management

### Default Limits (docker-compose.yml)

- **Memory Limit**: 512MB
- **Memory Reservation**: 128MB
- **CPU Limit**: 2.0 cores
- **CPU Reservation**: 0.5 cores

### Custom Resource Limits

Using Docker CLI:

```bash
docker run --memory="512m" --cpus="2.0" naydoev1:latest
```

Using docker-compose.yml, modify:

```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'      # Increase CPU limit
      memory: 1G       # Increase memory limit
```

## Health Checks

The container includes a built-in health check that runs every 30 seconds:

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Health check details:
- **Command**: `python3 -c "import naydoev1"`
- **Interval**: 30 seconds
- **Timeout**: 3 seconds
- **Retries**: 3
- **Start Period**: 5 seconds

## Usage Examples

### Interactive Python Session

Start an interactive Python session with NayDoeV1 loaded:

```bash
docker run -it --rm naydoev1:latest
```

This drops you into a Python shell with:
```python
>>> from naydoev1 import NayDoeV1
>>> assistant = NayDoeV1()
>>> # Use the assistant...
```

### Run a Python Script

```bash
docker run --rm -v $(pwd)/my_script.py:/app/my_script.py naydoev1:latest python3 /app/my_script.py
```

### Execute One-time Command

```bash
docker run --rm naydoev1:latest python3 -c "
from naydoev1 import NayDoeV1
assistant = NayDoeV1()
code = 'def hello(): return \"World\"'
result = assistant.process_code(code, 'python')
print(f'Processing time: {result[\"processing_time_ms\"]}ms')
"
```

## Development Workflow

### Building for Development

```bash
# Build with a specific tag
docker build -t naydoev1:dev .

# Build with no cache (force rebuild)
docker build --no-cache -t naydoev1:dev .
```

### Debugging

```bash
# Run with shell access
docker run -it --rm naydoev1:latest /bin/bash

# View container logs
docker logs naydoev1-assistant

# Inspect running container
docker exec -it naydoev1-assistant /bin/bash
```

## Production Deployment

### Best Practices

1. **Use Named Volumes**: For persistent data across container restarts
   ```bash
   docker volume create naydoev1-data
   docker run -v naydoev1-data:/app/data naydoev1:latest
   ```

2. **Set Restart Policy**: Ensure container restarts on failure
   ```bash
   docker run --restart=unless-stopped naydoev1:latest
   ```

3. **Monitor Resource Usage**:
   ```bash
   docker stats naydoev1-assistant
   ```

4. **Regular Updates**: Rebuild image when code changes
   ```bash
   docker build -t naydoev1:latest .
   docker compose up -d --force-recreate
   ```

### Security Considerations

✅ **Non-root User**: Container runs as user 'naydoe' (not root)
✅ **Minimal Base Image**: Uses slim Python image to reduce attack surface
✅ **No Unnecessary Tools**: Only includes what's needed to run the application
✅ **Read-only Config**: Config file mounted as read-only
✅ **Health Checks**: Built-in monitoring for container health

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker logs naydoev1-assistant
```

Verify image was built successfully:
```bash
docker images naydoev1
```

### Permission Issues

Ensure volumes have correct permissions:
```bash
docker run --rm -v naydoev1-data:/app/data naydoev1:latest ls -la /app/data
```

### Memory Issues

Increase memory limit in docker-compose.yml or CLI:
```bash
docker run --memory="1g" naydoev1:latest
```

### Health Check Failing

Test health check manually:
```bash
docker run --rm naydoev1:latest python3 -c "import naydoev1"
```

## Performance Optimization

### Layer Caching

The Dockerfile is optimized for layer caching:
1. Base image and system setup (rarely changes)
2. Application code (changes frequently)

This means rebuilds are fast if only code changes.

### Startup Time

- Container starts in < 1 second
- Application initializes in ~0.98ms
- Health check validates import in ~100ms

## Multi-Architecture Support

The image is based on official Python images which support multiple architectures:

- linux/amd64 (x86_64)
- linux/arm64 (ARM 64-bit)
- linux/arm/v7 (ARM 32-bit)

Build for specific platform:
```bash
docker buildx build --platform linux/amd64 -t naydoev1:amd64 .
docker buildx build --platform linux/arm64 -t naydoev1:arm64 .
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t naydoev1:latest .
      - name: Test image
        run: docker run --rm naydoev1:latest python3 -c "from naydoev1 import NayDoeV1; NayDoeV1()"
```

## Additional Resources

- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review [QUICKSTART.md](QUICKSTART.md)
- See [API.md](API.md) for API reference
