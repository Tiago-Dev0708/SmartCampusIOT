# Fase 007: Containerização para Servidor CachyOS

**Objetivo:** Empacotar a aplicação pronta para ser exposta através do Zero Trust Cloudflare.

**Arquivos a criar/modificar:**

- `Dockerfile` (raiz)
- `docker-compose.yml` (raiz)
- `.env.example`

**Instruções de Codificação:**

1. Crie o `Dockerfile` conforme as skills: Multi-stage, imagem `python:3.14-slim`, instalação das dependências. Comando de inicialização usando `uvicorn src.presentation.api.main:app --host 0.0.0.0 --port 8000`.
2. No `docker-compose.yml`, declare os seguintes serviços:
   - `api`: Build do Dockerfile. Rede `backend`.
   - `db`: Imagem `postgres:15-alpine`.
   - `mqtt`: Imagem `eclipse-mosquitto:latest`. Portas `1883:1883` expostas localmente apenas para o Wokwi conectar.
   - `cloudflared`: Imagem `cloudflare/cloudflared`. Comando `tunnel --no-autoupdate run --token ${CLOUDFLARE_TOKEN}`. Conectado à rede `backend`.
3. Preencha `.env.example` com placeholders para variáveis de DB, HDFS_URL e CLOUDFLARE_TOKEN.

**Critérios de Aceitação (Hard Constraints):**

- O serviço `api` NÃO deve ter a tag `ports: - "8000:8000"`. A exposição para a internet ocorrerá exclusivamente através do container `cloudflared`, que roteia o tráfego do domínio DuckDNS para o DNS interno do docker (ex: `http://api:8000`).
