# Dockerfile for Project Management MVP
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --upgrade pip && pip install -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend static build
COPY frontend/out/ ./frontend/out/

# Expose port
EXPOSE 8000

# Environment variables (should be passed via -e at runtime or --build-arg)
ARG OPENROUTER_API_KEY
ENV OPENROUTER_API_KEY=$OPENROUTER_API_KEY
ARG JWT_SECRET
ENV JWT_SECRET=$JWT_SECRET

# Start FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
