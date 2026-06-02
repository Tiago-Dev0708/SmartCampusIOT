# Fase 012: Ambiente de Testes e Cobertura (Pytest)

**Objetivo:** Configurar o ecossistema de testes automatizados garantindo isolamento total da infraestrutura física, focando na integridade da Clean Architecture.

**Arquivos a criar/modificar:**

- `pyproject.toml` (ou `pytest.ini`)
- `tests/conftest.py`
- `tests/unit/` (Diretório)
- `tests/integration/` (Diretório)

**Instruções de Codificação:**

1. Configure o `pytest` no arquivo `pyproject.toml`. Adicione dependências para o ecossistema assíncrono e cobertura: `pytest-asyncio`, `pytest-cov` e `httpx` (para o `TestClient` do FastAPI).
2. Em `tests/conftest.py`, crie as **Fixtures** cruciais para o projeto:
   - `mock_db_session`: Uma sessão de banco de dados (SQLite em memória assíncrono) para testes de repositório, garantindo um banco limpo a cada teste.
   - `mock_mqtt_client`: Um mock da biblioteca `aiomqtt` para garantir que testes unitários não tentem conectar ao broker real.
   - `mock_hdfs_client`: Um dublê para o cliente Hadoop, retornando sucesso na exportação sem precisar do cluster rodando.
   - `client`: Instância do `AsyncClient` do `httpx` montada sobre a aplicação FastAPI.
3. No diretório `tests/unit/`, estabeleça os testes para a camada de `domain` e `use_cases`.
4. No diretório `tests/integration/`, estabeleça os testes para a camada de `presentation/api` (batendo nas rotas usando o cliente de teste) e os adaptadores de banco de dados (`infrastructure`).

**Critérios de Aceitação (Hard Constraints):**

- **Isolamento Estrito:** Testes da pasta `unit` NÃO PODEM realizar I/O real (banco de dados, rede, disco, inferência real do LightGBM). Devem rodar em milissegundos usando mocks/stubs.
- **Cobertura Mínima (Coverage):** Configure o `pytest-cov` para falhar a suíte de testes caso a cobertura de código caia abaixo de **85%** (`--cov-fail-under=85`).
- Os testes assíncronos devem estar devidamente decorados com `@pytest.mark.asyncio`.
