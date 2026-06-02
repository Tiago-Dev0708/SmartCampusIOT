# Skill: Senior Python & FastAPI Engineer

**1. Estado da Arte em Python:**
- Use tipagem estrita (Mypy compliance). Exemplo de retorno: `async def get_sensor() -> SensorEntity | None:`.
- Pydantic V2 obrigatório: Use `model_config` em vez de `Config`. Use `Field` para validações (ex: `Field(gt=0)`).

**2. Padrão de Roteamento FastAPI:**
- As rotas devem ficar em `src/presentation/api/routers/`.
- Nunca injete a sessão do banco de dados diretamente na rota. Injete o **Use Case**, que por sua vez recebe o repositório configurado via um sistema de injeção de dependências (use uma fábrica/factory no `Depends` do FastAPI).

**3. Tratamento de Erros HTTP:**
- O domínio levanta exceções personalizadas (ex: `SensorNotFoundError(Exception)`).
- A camada `presentation/api/middlewares` ou manipuladores de exceção do FastAPI (`@app.exception_handler`) capturam essas exceções do domínio e as traduzem para `HTTPException` (ex: 404 Not Found), garantindo que mensagens de erro de banco de dados nunca vazem para o cliente.