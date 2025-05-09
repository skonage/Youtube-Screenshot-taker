# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install ffmpeg (required for screenshots)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy server code and requirements
COPY server.py requirements.txt ../youtube_screenshot_taker.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for SSE (optional, not needed for stdio)
EXPOSE 8050

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_QUIET=1
ENV PYTHONPATH=/app

# Run the MCP server
CMD ["python", "server.py"] 