# Fase 009: Autenticação de Usuários (JWT e Refresh Token)

**Objetivo:** Implementar o fluxo de registro e login com segurança, seguindo a Clean Architecture.

**Arquivos a criar/modificar:**

- `src/domain/entities/user.py`
- `src/domain/interfaces/auth_providers.py`
- `src/infrastructure/auth/jwt_provider.py`
- `src/infrastructure/auth/password_hasher.py`
- `src/use_cases/register_user.py`
- `src/use_cases/login_user.py`
- `src/presentation/api/routers/auth_router.py`

**Instruções de Codificação:**

1. Na Camada de Domínio, crie a entidade `UserEntity` e as interfaces `PasswordHasherInterface` e `TokenProviderInterface`.
2. Na Infraestrutura, crie o adaptador `PasswordHasher` usando `passlib` (bcrypt). Crie o `JwtProvider` usando `PyJWT` para gerar tokens de acesso (curta duração) e refresh tokens (longa duração).
3. Em `register_user.py`, crie o Use Case que recebe email e senha, valida se o usuário já existe no repositório, faz o hash da senha e salva.
4. Em `login_user.py`, crie o Use Case que verifica credenciais e retorna o par `access_token` e `refresh_token`.
5. Em `auth_router.py`, exponha os endpoints `POST /auth/register`, `POST /auth/login` e `POST /auth/refresh`.

**Critérios de Aceitação (Hard Constraints):**

- A camada de Use Case NÃO DEVE importar o `PyJWT` ou `passlib`. Ela deve confiar apenas nas interfaces do domínio injetadas.
- As senhas NUNCA devem trafegar ou ser exibidas em texto plano, nem nos logs do sistema.
