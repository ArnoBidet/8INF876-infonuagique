K8S_FOLDER=./k8s
FRONTEND_FOLDER=${K8S_FOLDER}/frontend
DB_FOLDER=${K8S_FOLDER}/db
SECRET_FOLDER=${K8S_FOLDER}/secret

all: deploy-secret deploy-front deploy-db

build-deploy-front:
	docker build -t arno/todo-frontend:latest ./src
	minikube image load arno/todo-frontend:latest
	minikube image list

deploy-front:
	kubectl apply -f $(FRONTEND_FOLDER)/frontend-deployment.yaml
	kubectl apply -f $(FRONTEND_FOLDER)/frontend-service.yaml

lookup:
	echo "Deployments:"
	kubectl get deployment -n default
	echo "Services:"
	kubectl get services -n default
	echo "Pods:"
	kubectl get pods -n default
	echo "Persistent Volume Claims:"
	kubectl get pvc -n default
	echo "Config Maps:"
	kubectl get configmap -n default
	echo "Secrets:"
	kubectl get secrets -n default

clean-front:
	kubectl delete -f $(FRONTEND_FOLDER)/frontend-deployment.yaml
	kubectl delete -f $(FRONTEND_FOLDER)/frontend-service.yaml

deploy-db:
	kubectl apply -f $(DB_FOLDER)/mysql-configmap.yaml
	kubectl apply -f $(DB_FOLDER)/mysql-pvc.yaml
	kubectl apply -f $(DB_FOLDER)/mysql-deployment.yaml
	kubectl apply -f $(DB_FOLDER)/mysql-service.yaml

clean-db-pvc:
	kubectl delete -f $(DB_FOLDER)/mysql-pvc.yaml

clean-db:
	kubectl delete -f $(DB_FOLDER)/mysql-deployment.yaml
	kubectl delete -f $(DB_FOLDER)/mysql-service.yaml
	kubectl delete -f $(DB_FOLDER)/mysql-configmap.yaml

restart-all:
	kubectl

deploy-secret:
	kubectl apply -f $(SECRET_FOLDER)/secret.yaml

clean-secret:
	kubectl delete -f $(SECRET_FOLDER)/secret.yaml

clean-all: clean-front clean-db clean-secret

clean-very-all: clean-all clean-db-pvc

stop:
	minikube stop