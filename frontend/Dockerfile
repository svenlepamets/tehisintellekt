# 1. Builder
FROM node:22-alpine AS builder

# Set working directory
WORKDIR /usr/src/app

# Copy package files first to leverage Docker cache
COPY package*.json ./

# Install dependencies and cache them
RUN npm install --prefer-offline --no-audit --progress=false

# Copy the rest of the app
COPY . .

# 2. Runtime
FROM node:22-alpine

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy from builder
COPY --from=builder /usr/src/app .

# Expose Next.js dev server port
EXPOSE 3000

# Start Next.js dev server
CMD ["npm", "run", "dev"]
