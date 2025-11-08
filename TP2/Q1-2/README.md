# Rapport TP2 - Question 1 et 2 : Déploiement Kubernetes et Load balancing avec HaProxy

**Réalisé par :** Arno BIDET & Antoine MAMOU  
**Date :** 

## Question 1

### TL;DR lancer le tout

- Créer le fichier `secrets.yaml` à partir de `secrets.example.yaml`. Compléter les champs en y mettant des valeurs en base 64 `echo -n "[TRUC A CHIFFRER]" | base64`.
- Lancer Minikube `minikube start`
- Tout lancer `make all`
- Obtenir l'ip du serveur `minikube ip`
- Accéder au serveur WEB à `[minikube ip]:30080`
- Regarder les différentes ressources générées `make lookup`
- Tout arrêter `make clean-all`
- Vider la BDD `make clean very-all`
- Arrêter minikube `make stop`

### Étape 1 - Installation

Docker est déjà installé sur nos machines :

```sh
docker --version
# Docker version 28.3.2, build 578ccf6
```

---

Pour installer Kubectl, les commandes suivantes provenants de la [documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) ont été effectuée :

```sh
sudo apt update
curl -LO "https://dl.k8s.io/release/$(curl -L https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
rm kubectl.sha256
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

Pour vérifier l'installation 

```sh 
kubectl version
# Client Version: v1.34.1
# Kustomize Version: v5.7.1
# The connection to the server localhost:8080 was refused - did you specify the right host or port?
```
---

Pour installer MiniKube via la [documentation](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)

```sh
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

```sh
minikube start
# 😄  minikube v1.37.0 sur Ubuntu 24.04
# ✨  Choix automatique du pilote docker. Autres choix: none, ssh
# 📌  Utilisation du pilote Docker avec le privilège root
# 👍  Démarrage du nœud "minikube" primary control-plane dans le cluster "minikube"
# 🚜  Extraction de l'image de base v0.0.48...
# 💾  Téléchargement du préchargement de Kubernetes v1.34.0...
#     > preloaded-images-k8s-v18-v1...:  337.07 MiB / 337.07 MiB  100.00% 6.07 Mi
#     > gcr.io/k8s-minikube/kicbase...:  488.51 MiB / 488.52 MiB  100.00% 6.97 Mi
# 🔥  Création de docker container (CPU=2, Memory=3072Mo) ...
# 🐳  Préparation de Kubernetes v1.34.0 sur Docker 28.4.0...
# 🔗  Configuration de bridge CNI (Container Networking Interface)...
# 🔎  Vérification des composants Kubernetes...
#     ▪ Utilisation de l'image gcr.io/k8s-minikube/storage-provisioner:v5
# 🌟  Modules activés: storage-provisioner, default-storageclass
# 🏄  Terminé ! kubectl est maintenant configuré pour utiliser "minikube" cluster et espace de noms "default" par défaut.
```

Pour rappel de ce que sont ces trois utiilitaires que nous avons installés :
- `Docker` : Nous permet de tester nos images de manière isolées ou groupées (docker-compose)
- `Kubectl` : Utilitaire de commande permettant de contrôler des systèmes Kubernetes. Il communique avec le Kubernetes API Server qui contrôle le cluster configuré.
- `Minikube` : Un mini cluster Kubernetes local, compatible avec le Kubernetes réel du cloud.

### Étape 1 bis - Utiliser un fichier de secret

Parce que on va vouloir utiliser des variables d'environnement, et parce qu'on fait les choses bien, on va utiliser un fichier de secret qui aura les variables d'environnement.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
type: Opaque
data:
  MYSQL_USER:
  MYSQL_PASSWORD:
  MYSQL_DATABASE: dG9kb19saXN0
  MYSQL_ROOT_PASSWORD:
```

Et pour remplir le fichier on utilise la commande `echo -n "[TRUC A CHIFFRER]" | base64`

Sources : 
- https://stackoverflow.com/questions/33478555/kubernetes-equivalent-of-env-file-in-docker
- https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/

### Étape 2 - Déployer une base de données

Il nous est donné un plan de déploiment de base de donnée :

```yaml
# mysql-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec: 
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:5.7
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "password"
          ports:
            - containerPort: 3306
```

Quelques points d'intérêts :

- `kind` donne le type de ressource Kubernetes. Ici un déploiment. La partie `metadata` indique que ce déploiement est nommé "mysql".
```yaml
kind: Deployment
metadata:
  name: mysql
```

- `replicas` indique le nombre de pods à créer.
```yaml
spec: 
  replicas: 1
```

- `selector` est un critère pour identifier quels pods ce déploiement gère, soit : tous les pods avec le label `app: mysql`.
```yaml
selector:
  matchLabels:
    app: mysql
```

- `template` : Modèle pour créer les pods
- `labels` : Étiquettes appliquées aux pods créés
- `containers` : Configuration du conteneur MySQL
  - `image` : Image Docker MySQL version 5.7
  - `env` : Variables d'environnement (mot de passe root MySQL)
  - `ports` : Port exposé par le conteneur (3306 pour MySQL)

En somme, Ce déploiement crée un pod MySQL accessible sur le port 3306 avec le mot de passe root "password". Attention, l'accessibilité n'est qu'à l'intérieur du cluster, entre les ports. Et c'est très bien comme ça.

```yaml
template:
  metadata:
    labels:
      app: mysql
  spec:
    containers:
      - name: mysql
        image: mysql:5.7
        env:
          - name: MYSQL_ROOT_PASSWORD
            value: "password"
        ports:
          - containerPort: 3306
```
Avant de l'appliquer, on va modifier la manière de passer les variables d'environnement et les variables d'environnement en question. On va aussi créer un configMap afin de pouvoir passer le script d'initialisation de la base de donnée au container.

```yaml
# mysql-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-init-script
data:
  init.sql: |
    CREATE DATABASE IF NOT EXISTS todo_list;
    USE todo_list;

    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        status ENUM('pending', 'completed') DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
```

Et pour la partie deployment, on modifie tel que :

```yaml
# mysql-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec: 
  replicas: 1
  selector:
    matchLabels:
      app: mysql-pod
  template:
    metadata:
      labels:
        app: mysql-pod
    spec:
      containers:
        - name: mysql
          image: mysql:5.7
          ports:
            - containerPort: 3306
          envFrom:
            - secretRef:
                name: mysql-secret
          volumeMounts:
            - name: mysql-initdb
              mountPath: /docker-entrypoint-initdb.d
      volumes:
        - name: mysql-initdb
          configMap:
            name: mysql-init-script   
```

Appliquons le :

```sh
kubectl apply -f mysql-deployment.yaml
# deployment.apps/mysql created
```

---

Ensuite on nous demande de l'exposer à travers un service. Faire ça permet à tous les pods du cluster de se connecter à notre base de donnée.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
    - port: 3306
  selector:
    app: mysql
```

De la même manière, `kind` indique le type de ressource Kubernetes, `metadata` de premier niveau indique le nom de ce service, la section `spec` indique les détails techniques du service, qui sont l'exposition du port 3306 pour les containers ayant le label `mysql`.

### Étape 3 - Déployer une application frontend

Puisque nous sommes fainéant, nous prenons un repo pour notre frontend : https://github.com/obadaKraishan/ToDoListPHP

On ajoute un Dockerfile pour faire tourner le tout sur le cloud :

```Dockerfile
FROM php:8.2-apache

# On copie les fichiers src
COPY . /var/www/html/

WORKDIR /var/www/html

# On install le connecteur pour mysql
RUN docker-php-ext-install mysqli 

EXPOSE 80
```

Puis on build : `make build-deploy-front`

Le projet cité ci-dessus contient tout ce qu'il nous faut pour nous connecter, il nous suffit de mettre en place le passage des arguments en variable d'environnement.
Pour `TP2/Q1-2/src/includes/db.php` de :
```php
$servername = "localhost"; // The hostname of the database server
$username = "root";        // The username to connect to the database
$password = "";            // The password to connect to the database
$dbname = "todo_list";     // The name of the database to connect to
```
À :
```php
$servername = 'mysql-service'; // The hostname of the database server
$username = $_ENV['MYSQL_USER']; // The username to connect to the database
$password = $_ENV['MYSQL_PASSWORD']; // The password to connect to the database
$dbname = $_ENV['MYSQL_DATABASE'];       // The name of the database to connect to
```

Une fois cela fait, on créé le fichier de déploiement et de service :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: arno/todo-frontend:latest
          ports:
            - containerPort: 80
          imagePullPolicy: Never # On veut forcer l'utilisation de l'image locale
          envFrom:
            - secretRef:
                name: mysql-secret
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080
  selector:
    app: frontend
```

Attardons nous sur `type: NodePort`. Si on se réfère à la [documentation](https://kubernetes.io/docs/concepts/services-networking/service/), cette directive nous permet de manière effective d'exposer le container au monde, là ou le service qui exposait simplement le port ne le faisait en fait qu'à l'intérieur du cluster.

Pour que ça marche, on ajoute `nodePort: 30080` pour pouvoir accéder au service.

### Étape 4 - Accéder à notre serveur

1. Build l'image de front : `make build-deploy-front`
2. On lance le server avec `make`

La commande `minikube ip` nous donne l'adresse locale de notre cluster, avec cette dernière on peut accéder à notre serveur via `[MINIKUBE_IP]:30080`.

Et tout marche bien, mais si on redémarre le server, on perd toute les données !

Donc on va mettre en place la persistance :

### Étape 5 - Mettre en place la persistance

On nous donne la chose suivante :

```yaml
# mysql-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

et on modifie notre base de donnée pour qu'elle exploite cette ressource :

```yaml
# Section spec.template.spec.containers[0].volumeMounts[1]
            - name: mysql-persistent-storage
              mountPath: /var/lib/mysql
# Section spec.template.spec.volumes[1]
        - name: mysql-persistent-storage
          persistentVolumeClaim:
            claimName: mysql-pvc
```

Maintenant, si on essaie tout ça ensemble, on a notre todo-list qui résiste aux redémarrage. Vive la persistence !

