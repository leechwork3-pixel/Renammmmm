# Use an official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Set environment variables (optional fallback)
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "bot.py"]
