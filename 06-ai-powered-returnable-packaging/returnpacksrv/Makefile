helm-deploy:
	helm upgrade -n returnpack -i returnpacksrv-db helm/returnpacksrv-db --install
	helm upgrade -n returnpack -i returnpacksrv-srv helm/returnpacksrv-srv --install

helm-undeploy:
	helm uninstall -n returnpack returnpacksrv-srv
	helm uninstall -n returnpack returnpacksrv-db


