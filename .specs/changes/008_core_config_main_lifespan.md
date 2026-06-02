# Fase 008: Core Configuration, Bootstrap e Telemetria (Lifespan)

**Objetivo:** Centralizar configurações, estruturar o ciclo de vida e implementar uma fundação de logs coesa e estruturada, evitando poluição de stdout.

**Arquivos a criar/modificar:**

- `src/core/config/settings.py`
- `src/core/config/cors.py`
- `src/core/config/logger.py`
- `src/presentation/api/main.py`

**Instruções de Codificação:**

1. Em `settings.py`, crie a classe `Settings(BaseSettings)` do Pydantic V2 contendo as variáveis: `PROJECT_NAME`, `VERSION`, `ENVIRONMENT` (dev/prod), `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS` e `LOG_LEVEL`.
2. Em `cors.py`, defina as configurações de CORS buscando os domínios permitidos do `settings` (incluindo as variáveis para o túnel DuckDNS).
3. Em `logger.py`, configure um sistema de logs estruturado (recomenda-se `structlog` ou a configuração de `dictConfig` do pacote padrão `logging`).
   - O log DEVE ser formatado em JSON se `ENVIRONMENT == "prod"`. Em ambiente `dev`, use formatação amigável ao console (colorida).
   - Filtre ruídos desnecessários de bibliotecas de terceiros (ex: diminua a verbosidade do `uvicorn.access`, `aiomqtt` e `sqlalchemy.engine` para nível WARNING ou superior).
4. Em `main.py`, crie o gerenciador de contexto `lifespan` (`@asynccontextmanager`).
   - **Startup:** Inicialize o logger estruturado, abra o pool do banco, inicie a task do worker MQTT e carregue o singleton do LightGBM. Intercepte erros de inicialização e faça o log como `CRITICAL` antes de encerrar.
   - **Shutdown:** Encerre graciosamente as conexões MQTT e de banco de dados. Registre o log de "Shutting down application gracefully".
5. Inicialize o `FastAPI(lifespan=lifespan)` e adicione o middleware de CORS.

**Critérios de Aceitação (Hard Constraints):**

- É ESTRITAMENTE PROIBIDO o uso de `@app.on_event("startup")` ou `@app.on_event("shutdown")`.
- É ESTRITAMENTE PROIBIDO usar `print()` na base de código. Toda saída deve utilizar o logger configurado.
- Os logs devem possuir um ID de correlação (correlation ID) caso a requisição passe pelas rotas da API, para facilitar o rastreamento do Mobile até o Banco de Dados.

  **Para garantir a tradução automática entre os padrões snake_case e camelCase sem precisar renomear atributos manualmente em cada dicionário, adicione esta regra de configuração global à Skill ou especificação de configuração:**

  # Exemplo de configuração a ser exigida na Spec de Config/Pydantic

  from pydantic import BaseModel, ConfigDict
  from pydantic.alias_generators import to_camel

  class BaseSchema(BaseModel):
  model_config = ConfigDict(
  alias_generator=to_camel,
  populate_by_name=True,
  from_attributes=True
  )
