# Deployment Guide

This guide provides step-by-step instructions for deploying a FastAPI application connected to a MySQL database in a Kubernetes cluster. It assumes that you have Docker and Kubernetes installed and configured.

## Prerequisites

- Kubernetes cluster (e.g  k3s)
- kubectl installed and configured to manage your Kubernetes cluster

## Steps

### 1. Create Kubernetes Deployment

```bash
kubectl apply -f my-deployment-eval.yaml
```

### 2. Create Kubernetes Service

```bash
kubectl apply -f my-service-eval.yaml
```

### 3. Create Kubernetes Secret for MySQL Password

```bash
kubectl apply -f my-secret-eval.yaml
```

### 4. Create Kubernetes Ingress

```bash
kubectl apply -f my-ingress-eval.yaml
```

### 5. Verify Deployment

```bash
kubectl get all
```

## Clean Up (Optional)

After testing, you can clean up the deployed resources using the following commands:

```bash
kubectl delete -f mysql-deployment.yaml
kubectl delete -f fastapi-deployment.yaml
kubectl delete -f mysql-service.yaml
kubectl delete -f fastapi-service.yaml
```

## Additional Notes

Docker Images: The Docker images for MySQL and FastAPI are already available in Docker Hub. If you want to redeploy them to your Docker Hub account, follow the steps below.

### Redeploy Docker Images to Docker Hub

### 1. Login to Docker Hub: Use the following command to login to Docker Hub

```bash
docker login
```

### 2. Build and Push Docker Images: After logging in, rebuild the Docker images if necessary and push them to Docker Hub using the following commands

```bash
docker build -t your_username/datascientest_user_api:v1 -f path/to/Dockerfile_fastapi .
docker push your_username/datascientest_user_api:v1
```
