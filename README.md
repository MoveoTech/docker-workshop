# Docker Workshop: Building and Managing Containerized Applications

Welcome to the Docker Workshop! In this hands-on session, you'll learn to containerize a full-stack Todo application, manage multi-container environments, and debug Docker deployments like a pro.

## 🎯 Workshop Objectives

By the end of this workshop, you'll be able to:
- Build and optimize Docker images for frontend and backend applications
- Run single containers with proper configuration
- Orchestrate multi-container applications using Docker Compose
- Debug containers using Docker CLI commands
- Use LazyDocker for visual container management
- Understand Docker networking, volumes, and best practices

## 📋 Prerequisites

- Docker Desktop installed and running
- Basic knowledge of command line
- Text editor (VS Code recommended)
- Git (for cloning/pushing changes)

### Install Required Tools

```bash
# Install LazyDocker (macOS)
brew install lazydocker

# Install LazyDocker (Linux)
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash

# Install LazyDocker (Windows)
# Download from: https://github.com/jesseduffield/lazydocker/releases
```

## 🏗️ Project Structure

```
docker-workshop/
├── backend/           # Flask API with SQLAlchemy
│   ├── app.py        # Main Flask application
│   ├── requirements.txt
│   ├── Dockerfile    # ⚠️ TO BE COMPLETED
│   └── Dockerfile.solution  # 💡 Solution reference
├── frontend/          # React Todo App
│   ├── src/
│   ├── package.json
│   ├── Dockerfile    # ⚠️ TO BE COMPLETED
│   └── Dockerfile.solution  # 💡 Solution reference
├── docker-compose.yml # ⚠️ TO BE COMPLETED
├── docker-compose.yml.solution # 💡 Solution reference
└── README.md         # This file
```

## 🚀 Getting Started

### Step 1: Explore the Applications

First, let's understand what we're containerizing:

**Backend (Flask API):**
- RESTful API for managing todos
- Supports both PostgreSQL and SQLite databases
- Health check endpoint
- CORS enabled for frontend communication

**Frontend (React App):**
- Modern React application
- Communicates with backend API
- Environment variable configuration for API URL

### Step 2: Build Your First Docker Image (Backend)

**Your Task:** Create a `backend/Dockerfile` to containerize the Flask application.

**Requirements:**
- Use Python 3.9 slim base image
- Set working directory to `/app`
- Copy `requirements.txt` first (for better layer caching)
- Install Python dependencies
- Copy application code
- Expose port 5000
- Run the application with `python app.py`

**Hints:**
- Use `COPY` to copy files into the container
- Use `RUN` to execute commands during build
- Use `CMD` to specify the default command
- Use `EXPOSE` to document the port (doesn't publish it)
- Use `WORKDIR` to set the working directory

**Need help?** Check `backend/Dockerfile.solution` for the complete solution.

Build and test the backend image:

```bash
# Navigate to backend directory
cd backend

# Build the image
docker build -t todo-backend .

# Run the container
docker run -p 5000:5000 todo-backend

# Test the API
curl http://localhost:5000/health
```

### Step 3: Build the Frontend Docker Image

**Your Task:** Create a `frontend/Dockerfile` using a multi-stage build to optimize the React application.

**Requirements:**
- **Stage 1 (Builder):** Use Node.js 18 Alpine image
  - Set working directory to `/app`
  - Copy `package*.json` files first
  - Install dependencies with `npm install`
  - Copy source code and build the app with `npm run build`
  
- **Stage 2 (Production):** Use nginx Alpine image
  - Copy built app from builder stage (`/app/build` → `/usr/share/nginx/html`)
  - Expose port 80
  - nginx starts automatically

**Hints:**
- Use `FROM node:18-alpine AS builder` for the first stage
- Use `FROM nginx:alpine` for the second stage
- Use `COPY --from=builder` to copy between stages
- The React build output goes to `/app/build`
- Nginx serves static files from `/usr/share/nginx/html`

**Need help?** Check `frontend/Dockerfile.solution` for the complete solution.

Build and test the frontend:

```bash
# Navigate to frontend directory
cd frontend

# Build the image
docker build -t todo-frontend .

# Run the container
docker run -p 3000:80 todo-frontend

# Open http://localhost:3000 in your browser
```

### Step 4: Docker Compose - Orchestrating Multiple Containers

**Your Task:** Create a `docker-compose.yml` file in the root directory to orchestrate all services.

**Requirements:**

**PostgreSQL Service:**
- Use `postgres:15` image
- Set environment variables: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- Create a named volume for data persistence
- Expose port 5432
- Add health check using `pg_isready`

**Backend Service:**
- Build from `./backend` directory
- Set `DATABASE_URL` environment variable to connect to postgres
- Expose port 5000
- Add dependency on postgres with health condition
- Mount `./backend:/app` for development
- Add health check using the `/health` endpoint

**Frontend Service:**
- Build from `./frontend` directory
- Set `REACT_APP_API_URL` environment variable
- Expose port 3000 (map to container port 80)
- Add dependency on backend service

**Hints:**
- Use `version: '3.8'`
- Use `build:` to build from local Dockerfiles
- Use `depends_on:` with `condition: service_healthy` for proper startup order
- Use `volumes:` for both bind mounts and named volumes
- Database URL format: `postgresql://user:password@host:port/database`
- Health check test format: `["CMD-SHELL", "command"]`

**Need help?** Check `docker-compose.yml.solution` for the complete solution.

Run the full stack:

```bash
# Start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🔧 Docker Debugging Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs <container-name>
docker logs -f <container-name>  # Follow logs

# Execute commands in running container
docker exec -it <container-name> /bin/bash
docker exec -it <container-name> /bin/sh  # For alpine images

# Inspect container details
docker inspect <container-name>

# View container resource usage
docker stats
docker stats <container-name>
```

### Image Management

```bash
# List images
docker images

# Remove unused images
docker image prune

# Remove specific image
docker rmi <image-name>

# View image layers
docker history <image-name>

# Build with no cache
docker build --no-cache -t <image-name> .
```

### Network and Volume Debugging

```bash
# List networks
docker network ls

# Inspect network
docker network inspect <network-name>

# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume-name>

# Remove unused volumes
docker volume prune
```

### Docker Compose Debugging

```bash
# View service logs
docker-compose logs <service-name>

# Scale services
docker-compose up -d --scale backend=3

# Restart specific service
docker-compose restart <service-name>

# View service status
docker-compose ps

# Execute command in service
docker-compose exec <service-name> <command>
```

## 🎮 Using LazyDocker

LazyDocker provides a terminal UI for managing Docker:

```bash
# Start LazyDocker
lazydocker
```

**Key LazyDocker Features:**
- **Tab Navigation**: Switch between containers, images, volumes, networks
- **Real-time Logs**: View and follow container logs
- **Resource Monitoring**: CPU, memory, and network usage
- **Quick Actions**: Start, stop, restart containers
- **Exec into Containers**: Easy shell access
- **Prune Operations**: Clean up unused resources

**LazyDocker Shortcuts:**
- `x`: Execute command in container
- `l`: View logs
- `s`: Stop container
- `r`: Restart container
- `d`: Delete container/image
- `p`: Prune unused resources

## 🏃‍♂️ Workshop Exercises

### Exercise 1: Backend Development Environment

**Your Task:** Create a development-friendly backend setup.

**Requirements:**
1. Create `backend/Dockerfile.dev` for development
2. Add development dependencies (like `flask-debugtoolbar`)
3. Set environment variables for debug mode
4. Configure for live code reloading with bind mounts

**Key Development Features:**
- Set `FLASK_ENV=development`
- Set `FLASK_DEBUG=1`
- Install additional dev dependencies
- Use bind mounts in docker-compose for instant code changes

**Hints:**
- Base it on your working `Dockerfile` but add dev-specific changes
- Use `ENV` to set environment variables
- Add `RUN pip install flask-debugtoolbar` for enhanced debugging
- Create a `docker-compose.dev.yml` that uses bind mounts

### Exercise 2: Frontend Development Environment

**Your Task:** Create a development setup with hot reloading.

**Requirements:**
1. Create `frontend/Dockerfile.dev` for development
2. Configure for development mode (no build step, no nginx)
3. Add bind mounts for source code changes
4. Use the React development server

**Key Development Features:**
- Use `npm start` instead of building and serving with nginx
- Expose port 3000 (React dev server default)
- Mount source code for instant hot reloading
- Skip the multi-stage build (development is single-stage)

**Hints:**
- Use Node.js base image (no nginx needed)
- Use `CMD ["npm", "start"]` for development server
- Create a `docker-compose.dev.yml` that mounts `./frontend:/app`
- Make sure to mount `node_modules` as an anonymous volume

### Exercise 3: Production Optimization

**Your Task:** Optimize your Docker images for production.

**Requirements:**
1. Use multi-stage builds to minimize image size
2. Add security improvements (non-root user)
3. Configure proper health checks
4. Optimize for production performance

**Backend Production Features:**
- Multi-stage build: builder stage + runtime stage
- Non-root user for security
- Minimal dependencies in final image
- Built-in health checks
- Optimized layer caching

**Frontend Production Features:**
- Already uses multi-stage build (builder + nginx)
- Minimal nginx-alpine runtime
- Optimized static file serving
- Security headers (via nginx config)

**Hints:**
- Use `FROM python:3.9-slim AS builder` for dependencies
- Create system user: `RUN groupadd -r appuser && useradd -r -g appuser appuser`
- Use `USER appuser` to switch to non-root
- Add `HEALTHCHECK` instruction for monitoring
- Use `--no-cache-dir` with pip to reduce image size

### Exercise 4: Advanced Docker Compose

**Your Task:** Create an advanced compose setup for production.

**Requirements:**
1. Environment-specific configurations
2. Secrets management for sensitive data
3. Resource limits and constraints
4. Service scaling and load balancing

**Advanced Features to Implement:**
- **Secrets Management:** Use Docker secrets for database passwords
- **Resource Limits:** Set CPU and memory limits for services
- **Service Scaling:** Configure backend replicas
- **Load Balancing:** Add nginx as reverse proxy
- **Production Dockerfiles:** Use optimized production images

**Key Components:**
- `docker-compose.prod.yml` for production configuration
- `secrets/` directory for sensitive data
- `nginx.conf` for reverse proxy configuration
- Resource constraints for each service
- Health checks and restart policies

**Hints:**
- Use `secrets:` top-level key and `POSTGRES_PASSWORD_FILE`
- Set `deploy.resources.limits` for CPU/memory constraints
- Use `deploy.replicas` for scaling services
- Configure nginx to proxy to backend services
- Use `dockerfile: Dockerfile.prod` for optimized builds

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

**Issue: Container won't start**
```bash
# Check logs
docker logs <container-name>

# Check container configuration
docker inspect <container-name>

# Try running interactively
docker run -it <image-name> /bin/bash
```

**Issue: Cannot connect to database**
```bash
# Check if database is running
docker-compose ps

# Check database logs
docker-compose logs postgres

# Test database connection
docker-compose exec postgres psql -U todouser -d todos
```

**Issue: Frontend can't reach backend**
```bash
# Check network connectivity
docker network ls
docker network inspect <network-name>

# Test API endpoint
docker-compose exec frontend curl http://backend:5000/health
```

**Issue: Changes not reflected**
```bash
# Rebuild images
docker-compose build --no-cache

# Remove containers and restart
docker-compose down
docker-compose up --build
```

### Performance Optimization

```bash
# Analyze image size
docker images

# Check container resource usage
docker stats

# Optimize builds with buildkit
DOCKER_BUILDKIT=1 docker build .

# Use .dockerignore to exclude unnecessary files
echo "node_modules" >> .dockerignore
echo "*.log" >> .dockerignore
```

## 📚 Best Practices

### Dockerfile Best Practices

1. **Use specific base image tags**
   ```dockerfile
   FROM node:18-alpine  # Not node:latest
   ```

2. **Leverage layer caching**
   ```dockerfile
   # Copy package.json first
   COPY package*.json ./
   RUN npm install
   # Then copy source code
   COPY . .
   ```

3. **Use multi-stage builds**
   ```dockerfile
   FROM node:18-alpine AS builder
   # Build stage
   FROM nginx:alpine AS production
   # Production stage
   ```

4. **Run as non-root user**
   ```dockerfile
   RUN addgroup -g 1001 -S nodejs
   RUN adduser -S nextjs -u 1001
   USER nextjs
   ```

### Docker Compose Best Practices

1. **Use health checks**
2. **Configure resource limits**
3. **Use secrets for sensitive data**
4. **Separate development and production configs**

## 🎓 Advanced Topics

### Docker Networking

```bash
# Create custom network
docker network create todo-network

# Run containers in custom network
docker run --network todo-network <image>

# Connect container to network
docker network connect todo-network <container>
```

### Docker Volumes

```bash
# Create named volume
docker volume create todo-data

# Use volume in container
docker run -v todo-data:/app/data <image>

# Backup volume
docker run --rm -v todo-data:/backup busybox tar czf /backup/backup.tar.gz /backup
```

### Container Monitoring

```bash
# Monitor container stats
docker stats --no-stream

# Check container health
docker inspect --format='{{.State.Health.Status}}' <container>

# View container processes
docker exec <container> ps aux
```

## 🎯 Workshop Completion Checklist

- [ ] Built backend Docker image
- [ ] Built frontend Docker image  
- [ ] Created working docker-compose.yml
- [ ] Tested full-stack application
- [ ] Used Docker debugging commands
- [ ] Explored LazyDocker interface
- [ ] Implemented health checks
- [ ] Created development environment
- [ ] Optimized production images
- [ ] Troubleshot common issues

## 📖 Additional Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [LazyDocker GitHub](https://github.com/jesseduffield/lazydocker)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

## 🎉 Congratulations!

You've completed the Docker workshop! You now have hands-on experience with:
- Building optimized Docker images
- Managing multi-container applications
- Debugging containerized applications
- Using modern Docker tooling

Keep practicing and exploring more advanced Docker features like Docker Swarm, Kubernetes integration, and CI/CD pipelines!

---

**Happy Dockerizing! 🐳** 