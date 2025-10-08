#!/bin/bash

set -e  # Terminar el script si ocurre un error

# Verificar que el CLI de Google Cloud esté instalado y autenticado
if ! command -v gcloud &> /dev/null
then
    echo "Error: El CLI de Google Cloud (gcloud) no está instalado."
    exit 1
fi

echo "Verificando autenticación con Google Cloud..."
gcloud auth login || { echo "Error: Falló la autenticación con Google Cloud."; exit 1; }

PROJECT_ID=$(gcloud config get-value project 2> /dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "Error: No se ha configurado un proyecto de Google Cloud. Usa 'gcloud config set project <PROJECT_ID>'."
    exit 1
fi

echo "Proyecto actual: $PROJECT_ID"

# Construir imágenes Docker y subirlas al Container Registry
SERVICES=("agent-runner" "document-service" "image-generator" "ui")
for SERVICE in "${SERVICES[@]}"
do
    echo "Construyendo imagen para $SERVICE..."
    docker build -t gcr.io/$PROJECT_ID/$SERVICE:latest ./services/$SERVICE || { echo "Error: Falló la construcción de la imagen para $SERVICE."; exit 1; }
    echo "Subiendo imagen de $SERVICE a Container Registry..."
    docker push gcr.io/$PROJECT_ID/$SERVICE:latest || { echo "Error: Falló el push de la imagen para $SERVICE."; exit 1; }
done

# Desplegar servicios en Google Cloud Run
echo "Desplegando servicios en Google Cloud Run..."

gcloud run deploy agent-runner \
    --image gcr.io/$PROJECT_ID/agent-runner:latest \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 || { echo "Error: Falló el despliegue de agent-runner."; exit 1; }

gcloud run deploy ui \
    --image gcr.io/$PROJECT_ID/ui:latest \
    --platform managed \
    --allow-unauthenticated \
    --port 80 || { echo "Error: Falló el despliegue de ui."; exit 1; }

gcloud run deploy document-service \
    --image gcr.io/$PROJECT_ID/document-service:latest \
    --platform managed \
    --no-allow-unauthenticated || { echo "Error: Falló el despliegue de document-service."; exit 1; }

gcloud run deploy image-generator \
    --image gcr.io/$PROJECT_ID/image-generator:latest \
    --platform managed \
    --no-allow-unauthenticated || { echo "Error: Falló el despliegue de image-generator."; exit 1; }

# Imprimir URLs públicas
echo "Servicios desplegados exitosamente."
echo "URL pública de agent-runner: $(gcloud run services describe agent-runner --format 'value(status.url)')"
echo "URL pública de ui: $(gcloud run services describe ui --format 'value(status.url)')"