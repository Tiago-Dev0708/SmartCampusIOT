#!/bin/bash
set -e

echo "======================================"
echo "Iniciando Deploy - Smart Campus IoT"
echo "======================================"

# Derruba os containers atuais caso estejam rodando
echo "[1/3] Parando containers antigos..."
docker compose down

# Força o rebuild da imagem (usando cache local eficientemente graças ao multi-stage)
echo "[2/3] Executando Docker Build..."
docker compose build

# Sobe toda a arquitetura em background
echo "[3/3] Iniciando serviços (API, DB, MQTT, Cloudflared)..."
docker compose up -d

echo "======================================"
echo "Deploy finalizado com sucesso!"
echo "Os containers estão rodando."
echo "======================================"
