# Use official Python slim image
FROM python:3.14-slim

# Set working directory
WORKDIR /usr/src/app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Set default port and environment (can be overridden)
ARG PORT=80
ENV PORT=${PORT}

ARG ENVIRONMENT=prod
ENV ENVIRONMENT=${ENVIRONMENT}

# Expose the port
EXPOSE ${PORT}

# Start the app with dev/prod logic
CMD ["sh", "-c", "\
  if [ \"$ENVIRONMENT\" = 'dev' ]; then \
    uvicorn server:app --host 0.0.0.0 --port $PORT --reload; \
  else \
    uvicorn server:app --host 0.0.0.0 --port $PORT; \
  fi"]
