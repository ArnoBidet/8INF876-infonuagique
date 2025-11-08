# Kubernetes Demo Application

## Description

Cette application est une démonstration complète d’un **déploiement Kubernetes multi-conteneurs**.  
Elle illustre la communication entre plusieurs services dans un cluster local (Docker Desktop) et montre des concepts clés du Cloud Computing et de Kubernetes tels que :

- Déploiements multi-conteneurs
- Services et découverte de services
- Communication inter-pods
- Stockage persistant
- Secrets et configuration
- Montée en charge / scaling

### Architecture

```
Frontend (Nginx)  <--->  Backend (Node.js + Express)  <--->  PostgreSQL
```

- **Frontend (Nginx)** : sert une page HTML avec un bouton pour interroger le backend.  
- **Backend (Node.js)** : expose une API simple, retourne des messages et interagit avec la base PostgreSQL.  
- **PostgreSQL** : base de données persistante via un volume Kubernetes (PVC).  

Tous les composants sont orchestrés par Kubernetes via des **déploiements et services**, permettant de démontrer la résilience et l’extensibilité d’une application Cloud.

---

## Prérequis

- Docker Desktop avec Kubernetes activé  
- `kubectl` configuré pour communiquer avec le cluster Docker Desktop  
- Node.js et npm (pour reconstruire l’image backend si nécessaire)

---

## Structure du projet

```
8INF876-infonuagique-tp2/
├─ backend/                  # Backend Node.js
│  ├─ server.js
│  ├─ package.json
│  └─ Dockerfile
├─ frontend/                 # Frontend Nginx
│  ├─ html/index.html
│  └─ Dockerfile
├─ k8s/                      # Fichiers YAML Kubernetes
│  ├─ backend-deployment.yaml
│  ├─ backend-service.yaml
│  ├─ frontend-deployment.yaml
│  ├─ frontend-service.yaml
│  ├─ postgres-deployment.yaml
│  ├─ postgres-service.yaml
│  ├─ postgres-pvc.yaml
│  └─ postgres-secret.yaml
```

---

## Instructions pour lancer l’application

### 1 Construire les images Docker

#### Backend
```bash
cd backend
docker build -t k8s-backend:v1 .
```

#### Frontend
```bash
cd ../frontend
docker build -t frontend-demo:v1 .
```

> Si vous utilisez Docker Hub, taggez vos images et poussez-les :  
```bash
docker tag k8s-backend:v1 <username>/k8s-backend:v1
docker push <username>/k8s-backend:v1
docker tag frontend-demo:v1 <username>/frontend-demo:v1
docker push <username>/frontend-demo:v1
```

---

### 2 Déployer PostgreSQL dans Kubernetes

```bash
kubectl apply -f k8s/postgres-secret.yaml
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

---

### 3 Déployer le backend Node.js

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

Vérifiez que le pod backend est **Running** :

```bash
kubectl get pods
```

---

### 4 Déployer le frontend Nginx

```bash
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Vérifiez que les pods frontend sont **Running** :

```bash
kubectl get pods
```

---

### 5 Accéder à l’application

- Frontend : [http://localhost:30003](http://localhost:30003)  
- Backend (Node.js) : [http://localhost:30002](http://localhost:30002)  
- PostgreSQL : accessible via le service `postgres-service` à l’intérieur du cluster.

Cliquez sur **“Appeler le backend”** dans la page frontend pour voir la réponse du backend.

---

### 6 Commandes utiles

- Vérifier l’état des pods :
```bash
kubectl get pods
```

- Vérifier les services :
```bash
kubectl get svc
```

- Voir les logs d’un pod :
```bash
kubectl logs <nom_du_pod>
```

- Mettre à l’échelle le backend (exemple : 4 réplicas) :
```bash
kubectl scale deployment backend --replicas=4
kubectl get pods
```

- Supprimer un déploiement :
```bash
kubectl delete deployment backend
```

---

### 7 Notes importantes

- L’image backend utilise **CORS activé** pour permettre au frontend sur un autre port (`30003`) de communiquer avec le backend (`30002`).  
- PostgreSQL est **persistant** grâce au volume PVC : les données survivent au redémarrage des pods.  
- Tous les services communiquent via **DNS interne Kubernetes**, sauf pour le NodePort utilisé depuis l’extérieur.

---

### 8 Résultat attendu

1. Ouvrir `http://localhost:30003`  
2. Cliquer sur **“Appeler le backend”**  
3. Voir la réponse :
```
Hello from Node.js backend via Kubernetes!
```
4. Backend peut également répondre à `/db` pour obtenir l’heure de PostgreSQL.
