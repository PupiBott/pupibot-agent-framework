#!/bin/bash

# Levantar todos los servicios con docker-compose
docker-compose up -d

# Esperar unos segundos para asegurarse de que los servicios estén en funcionamiento
sleep 5

# Mostrar las URLs de los servicios en la consola
echo "Servicios levantados:"
echo "Agent Runner: http://localhost:8080"
echo "UI: http://localhost:3000"