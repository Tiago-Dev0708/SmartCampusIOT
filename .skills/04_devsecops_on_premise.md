# Skill: DevSecOps Engineer (CachyOS + Cloudflare)

**1. Dockerfile Otimizado:**
- Use `FROM python:3.11-slim` como base.
- Implemente Multi-stage build: Crie um stage `builder` para compilar rodas (wheels) via `pip install -r requirements.txt` e um stage `runtime` final.
- Crie um usuário não-root (ex: `appuser`) e rode a aplicação com ele. O diretório de trabalho DEVE ser `/app`.

**2. Docker Compose (Zero Trust):**
- O `docker-compose.yml` NÃO DEVE expor portas para o host (`ports:`), exceto se for estritamente necessário para debug local. A comunicação externa se dará pela rede interna do docker conectada ao container do `cloudflared`.
- Adicione o serviço `cloudflared` configurado para ler o token de um arquivo `.env`.