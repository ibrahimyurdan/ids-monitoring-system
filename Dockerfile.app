FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install flask prometheus_client

# Copy application code
COPY ./scripts/app.py .

# Expose port
EXPOSE 8080

# Start application
CMD ["python", "app.py"] 