# Multi-stage build for minimal final image (prepared for future dependencies)
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Placeholder for future dependencies
# If dependencies are added to requirements.txt, install them here:
# COPY requirements.txt .
# RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

# Set Python optimization environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONOPTIMIZE=1

# Create non-root user for security
RUN groupadd -r naydoe && useradd -r -g naydoe naydoe

# Set working directory
WORKDIR /app

# Copy application source files
COPY naydoev1.py .
COPY config.json .
COPY README.md .
COPY QUICKSTART.md .
COPY API.md .
COPY LICENSE .
COPY DOCKER.md .

# Create directory for persistent data (rollback markers)
RUN mkdir -p /app/data && chown -R naydoe:naydoe /app

# Switch to non-root user
USER naydoe

# Update PATH to include user-installed packages
ENV PATH=/home/naydoe/.local/bin:$PATH

# Add healthcheck (lightweight import test)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import naydoev1" || exit 1

# Expose port if needed for future HTTP API (currently not used)
# EXPOSE 8000

# Default command - Python interactive shell with naydoev1 imported
CMD ["python3", "-i", "-c", "from naydoev1 import NayDoeV1; assistant = NayDoeV1(); print('\\n=== NayDoeV1 Assistant Ready ==='); print('Usage: assistant.process_code(code, language)'); print('Type help(assistant) for more info\\n')"]
