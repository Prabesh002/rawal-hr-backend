# Production Deployment Guide: Rawal HR Backend

This guide provides the full set of commands to build the production Docker image, push it to a container registry, and deploy it on a production server like a Hostinger VPS.

## 0. Prerequisites

Before you begin, ensure you have the following:

1.  **On Your Local Machine:**
    *   Docker Desktop (or Docker Engine) installed and running.
    *   An account on Docker Hub (or another container registry).

2.  **On Your Production Server (VPS):**
    *   SSH access.
    *   Docker and `docker-compose` installed.

---

## Part 1: Build & Push the Image (Run on your Local Machine)

This part packages the application into a production-ready Docker image and uploads it to Docker Hub.

### Step 1.1: Log in to Docker Hub

In your local terminal, authenticate with your Docker Hub account. You will be prompted for your username and password.

```sh
docker login
```

### Step 1.2: Build the Production Docker Image

This command uses the Dockerfile.prod blueprint to build a lean, optimized image.

First, set your Docker Hub username as a variable to avoid typos:  

```sh
# For macOS / Linux:
export DOCKER_HUB_USERNAME="your-dockerhub-username"

# For Windows (Command Prompt):
# set DOCKER_HUB_USERNAME="your-dockerhub-username"
```

**Now, run the build command:**

```sh
docker build -f Dockerfile.prod -t $DOCKER_HUB_USERNAME/rawal-backend:latest .
```

- `-f Dockerfile.prod`: Specifies that we are using the production Dockerfile.  
- `-t ...`: Tags the image with a name (your-username/image-name:tag).  
- `.`: Indicates the build context (the current directory).

### Step 1.3: Push the Image to Docker Hub

Upload the image you just built to the registry, making it available for your server to download.

```sh
docker push $DOCKER_HUB_USERNAME/rawal-backend:latest
```

You are now done with your local machine.

---

## Part 2: Deploy the Application (Run on your Hostinger VPS)

These commands are run on your production server via SSH. They will download your application image and start it alongside the database.

### Step 2.1: Connect to Your Server

```sh
ssh user@your_vps_ip_address
```

### Step 2.2: Create Project Directory

Create a dedicated folder for your application and navigate into it.

```sh
mkdir -p /opt/rawal-hr && cd /opt/rawal-hr
```

### Step 2.3: Create the Environment File (.env)


Run the following command to create and populate the file. You must replace the placeholder values with your actual production secrets.

```sh
DB_HOST=db
DB_PORT=5432
DB_HOST_PORT=5436
DB_NAME=rawal_prod_db
DB_USER=prod_user
DB_PASS=a_very_strong_and_secret_password_for_db
DATABASE_ECHO=False
LOG_LEVEL=INFO

ADMIN_USERNAME=admin@yourproductiondomain.com
ADMIN_PASSWORD=another_very_strong_secret_password

JWT_SECRET_KEY=generate_a_long_random_secret_string_for_this_using_a_password_manager
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_DAYS=30

APP_PORT=8000

# Gunicorn Workers (optional, defaults to 4)
WORKERS=5
```

### Step 2.4: Create the Docker Compose File

This file tells Docker how to run your application and the database together.

Remember to replace your-dockerhub-username with your actual Docker Hub username in the `image:` line.

```sh
cat << EOF > docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: pgvector/pgvector:pg17
    container_name: rawal-db-prod
    env_file:
      - .env
    environment:
      POSTGRES_USER: \${DB_USER}
      POSTGRES_PASSWORD: \${DB_PASS}
      POSTGRES_DB: \${DB_NAME}
    volumes:
      - postgres_data_prod:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \${DB_USER} -d \${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    restart: unless-stopped

  app:
    # yeta
    image: your-dockerhub-username/rawal-backend:latest
    container_name: rawal-backend-prod
    env_file:
      - .env
    ports:
      - "\${APP_PORT}:8000"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data_prod:
    driver: local
EOF
```

> Note: The backslashes `\` before the variables are important inside a `cat << EOF` block to prevent the shell from expanding them immediately.

### Step 2.5: Start the Application

Pull the latest version of your image from Docker Hub and start all services in detached mode (`-d`).

```sh
docker-compose -f docker-compose.prod.yml up -d
```

Your application is now live!

---

## Part 3: Managing the Live Application

Here are common commands to manage your running application on the VPS.

### Check container status:

```sh
docker-compose -f docker-compose.prod.yml ps
```

### View live application logs: (Press Ctrl+C to exit)

```sh
docker-compose -f docker-compose.prod.yml logs -f app
```

### Stop and remove all containers:

```sh
docker-compose -f docker-compose.prod.yml down
```

---

## How to Deploy an Update

When you've made code changes and want to deploy a new version:

- On your local machine, re-run the build and push steps (1.2 and 1.3).
- On your VPS, navigate to your project directory (`/opt/rawal-hr`) and run this single command:

```sh
docker-compose -f docker-compose.prod.yml up -d --pull
```

The `--pull` flag tells Compose to fetch the newest image version before starting, and it will intelligently recreate only the app container, resulting in a fast update.
