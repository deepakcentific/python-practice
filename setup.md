# Flask API on kind with GitHub Actions, ArgoCD and Ingress

This project demonstrates a complete GitOps workflow running locally on a kind Kubernetes cluster.

## Architecture

```text
GitHub Repository
       |
       v
GitHub Actions
       |
       v
Docker Hub
       |
       v
Update deployment.yaml
       |
       v
Commit back to GitHub
       |
       v
ArgoCD
       |
       v
kind Cluster
       |
       v
NGINX Ingress
       |
       v
http://deepak.com/health
```

---

# Prerequisites

- Docker
- kind
- kubectl
- GitHub Account
- Docker Hub Account
- ArgoCD
- WSL/Linux environment (recommended)

---

# Step 1: Create kind Cluster with Ingress Support

Create a file named `kind-config.yaml`.

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4

nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP

  - containerPort: 443
    hostPort: 443
    protocol: TCP
```

Create cluster:

```bash
kind create cluster --name demo --config kind-config.yaml
```

Verify:

```bash
kubectl get nodes
```

---

# Step 2: Install NGINX Ingress Controller

Install:

```bash
kubectl apply -f \
https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Verify:

```bash
kubectl get pods -n ingress-nginx
```

Wait until all ingress controller pods are running.

---

# Step 3: Install ArgoCD

Create namespace:

```bash
kubectl create namespace argocd
```

Install ArgoCD:

```bash
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Verify:

```bash
kubectl get pods -n argocd
```

---

# Step 4: Access ArgoCD UI

Port-forward:

```bash
kubectl port-forward svc/argocd-server \
-n argocd 8080:443
```

Open:

```text
https://localhost:8080
```

Get admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d
```

Login:

```text
Username: admin
Password: <output from command>
```

---

# Repository Structure

```text
python-practice/
│
├── app.py
├── requirements.txt
├── Dockerfile
│
├── .github/
│   └── workflows/
│       └── build.yml
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
│
└── README.md
```

---

# GitHub Actions Configuration

Grant workflow permissions:

```yaml
permissions:
  contents: write
```

Checkout repository:

```yaml
- uses: actions/checkout@v4
  with:
    persist-credentials: true
```

---

# Build and Push Docker Image

Example:

```yaml
- name: Build and Push Docker image
  uses: docker/build-push-action@v6
  with:
    push: true
    tags: dsahoo165/flask-api:${{ github.sha }}
```

This creates immutable image tags:

```text
dsahoo165/flask-api:a1b2c3d
dsahoo165/flask-api:e4f5g6h
```

---

# Update Kubernetes Deployment Manifest

Deployment image:

```yaml
containers:
- name: flask-api
  image: dsahoo165/flask-api:latest
```

Update automatically:

```yaml
- name: Update deployment yaml
  run: |
    sed -i "s|dsahoo165/flask-api:.*|dsahoo165/flask-api:${GITHUB_SHA}*g" \
    k8s/deployment.yaml
```

*esult:

```yaml
image: dsahoo165/f*ask-api:5b79d9573c527a4cbee84c2ab6*fae27ad7447c4
```

---

# Commit D*ployment Changes Back to GitHub

`*`yaml
- name: Commit changes
  run* |
    git config user.name github*actions
    git config user.email *ithub-actions@github.com

    git *dd .

    if git diff --staged --q*iet; then
      echo "No changes t* commit"
    else
      git commit*-m "Update image tag"
      git pu*h
    fi
```

---

# Kubernetes De*loyment

Example deployment:

```y*ml
apiVersion: apps/v1
kind: Deplo*ment

metadata:
  name: flask-api
*spec:
  replicas: 2

  selector:
 *  matchLabels:
      app: flask-ap*

  template:
    metadata:
      *abels:
        app: flask-api

   *spec:
      containers:
      - na*e: flask-api
        image: dsahoo*65/flask-api:latest

        ports*
        - containerPort: 5000
```*
---

# Kubernetes Service

```yam*
apiVersion: v1
kind: Service

met*data:
  name: flask-api-service

s*ec:
  selector:
    app: flask-api*
  ports:
  - port: 80
    targetP*rt: 5000

  type: ClusterIP
```

A*ply:

```bash
kubectl apply -f ser*ice.yaml
```

---

# Kubernetes In*ress

```yaml
apiVersion: networki*g.k8s.io/v1
kind: Ingress

metadat*:
  name: flask-api-ingress

spec:
  ingressClassName: nginx

  rules:
  - host: deepak.com

    http:
      paths:
      - path: /
        pathType: Prefix

        backend:
          service:
            name: flask-api-service
            port:
              number: 80
```

Apply:

```bash
kubectl apply -f ingress.yaml
```

Verify:

```bash
kubectl get ingress
```

---

# Configure Local DNS

Open hosts file as Administrator:

```text
C:\Windows\System32\drivers\etc\hosts
```

Add:

```text
127.0.0.1 deepak.com
```

Verify:

```bash
ping deepak.com
```

Expected:

```text
127.0.0.1
```

---

# ArgoCD Application

Create an ArgoCD Application pointing to:

```text
Repository:
https://github.com/<username>/<repo>

Path:
k8s

Sync Policy:
Automatic
```

ArgoCD continuously monitors the repository.

Whenever deployment manifests change:

```text
Git Change
    |
    v
ArgoCD Detects Drift
    |
    v
Sync
    |
    v
Cluster Updated
```

---

# Verify End-to-End Flow

Watch pods:

```bash
kubectl get pods -w
```

Push code changes:

```bash
git add .
git commit -m "code change"
git push
```

Observe:

```text
GitHub Actions
      |
      v
Build Image
      |
      v
Push to Docker Hub
      |
      v
Update deployment.yaml
      |
      v
Commit Back to GitHub
      |
      v
ArgoCD Sync
      |
      v
Rolling Deployment
```

Test:

```text
http://deepak.com/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# Useful Commands

### Pods

```bash
kubectl get pods
kubectl get pods -w
```

### Deployments

```bash
kubectl get deploy
kubectl describe deploy flask-api
```

### Services

```bash
kubectl get svc
```

### Ingress

```bash
kubectl get ingress
kubectl describe ingress
```

### Logs

```bash
kubectl logs <pod-name>
```

### ArgoCD

```bash
kubectl get applications -n argocd
```

### Docker Images

```bash
docker images
```

### kind Cluster

```bash
kind get clusters
kubectl get nodes
```

---

# Final Outcome

A complete local GitOps platform:

```text
Developer Push
      |
      v
GitHub Actions (CI)
      |
      v
Docker Hub
      |
      v
Manifest Update
      |
      v
GitHub Repository
      |
      v
ArgoCD (CD)
      |
      v
kind Kubernetes Cluster
      |
      v
NGINX Ingress
      |
      v
http://deepak.com/health
```

This closely resembles a production AKS GitOps workflow, with:

- kind instead of AKS
- Docker Hub instead of ACR
- Local hosts file instead of public DNS
- Local ingress instead of Azure Load Balancer