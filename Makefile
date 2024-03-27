DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = fastapi
STORAGES_FILE = docker_compose/storages.yaml
DB_CONTAINER = database
WORKERS_FILE = docker_compose/workers.yaml
WORKER_CONTAINER = celery-worker

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} -f ${STORAGES_FILE} ${ENV} -f ${WORKERS_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: worker-logs
worker-logs:
	${LOGS} ${WORKER_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${WORKERS_FILE} down --remove-orphans

.PHONY: db-logs
db-logs:
	${DC} -f ${STORAGES_FILE} logs -f
