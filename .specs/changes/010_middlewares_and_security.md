# Fase 010: Middlewares de Segurança e Proteção de Rotas

**Objetivo:** Adicionar camadas de proteção contra ataques comuns e criar o dependente de autorização para as rotas da API.

**Arquivos a criar/modificar:**

- `src/presentation/api/middlewares/security_headers.py`
- `src/presentation/api/dependencies/auth.py`
- Modificar `src/presentation/api/main.py`

**Instruções de Codificação:**

1. Crie o middleware `SecurityHeadersMiddleware` (Herdando de `BaseHTTPMiddleware`). Ele deve adicionar cabeçalhos como `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`.
2. Em `auth.py`, crie a dependência do FastAPI `get_current_user` usando `OAuth2PasswordBearer`. Essa dependência extrairá o token JWT do cabeçalho `Authorization`, fará o decode e validará se o usuário existe no banco de dados.
3. Adicione o middleware no `main.py` (cuidado com a ordem de empilhamento do CORS e do Security Headers).
4. Aplique a dependência `get_current_user` em rotas sensíveis criadas nas specs anteriores (ex: `POST /classrooms/{id}/toggle_light`), garantindo que apenas o diretor/zelador autenticado possa alterar o estado do IoT.

**Critérios de Aceitação (Hard Constraints):**

- A dependência de autenticação deve lidar graciosamente com tokens expirados ou inválidos, levantando um `HTTPException(status_code=401)` com escopo e descrição clara.
