# Skill: Staff Software Architect & Clean Architecture Enforcer

**1. Estrutura de Diretórios Obrigatória:**
O projeto DEVE seguir esta estrutura raiz em `src/`:

- `domain/`: Regras de negócio puras (Entities, Value Objects, Interfaces/Ports).
- `application/use_cases/`: Orquestração da lógica de negócio.
- `infrastructure/`: Implementações reais (Adapters, BD, MQTT, Clientes Externos).
- `presentation/`: Controladores, Rotas FastAPI, Injeção de Dependências.

**2. Restrições de Acoplamento (Zero Tolerância):**

- Arquivos dentro de `src/domain/` NÃO PODEM importar bibliotecas de terceiros (exceto `dataclasses`, `enum`, `typing`, `datetime` e `uuid`). É PROIBIDO importar `sqlalchemy`, `fastapi`, `pydantic` ou `lightgbm` no domínio, além do fato de ser obrigatório o uso de value_objects(quando couber no escopo, não usar de forma desenfreada/generalizada ou sem necessidade).
- Entidades de Domínio são diferentes de Modelos de Banco de Dados. Você deve criar mapeadores (Mappers) na camada de infraestrutura para converter `Modelos SQLAlchemy` em `Entidades de Domínio` e vice-versa.

**3. Padrão de Interfaces (Ports):**

- Todo repositório ou serviço externo deve ter uma classe abstrata (`ABC`) definida em `src/domain/interfaces/`.
- Nomeie as interfaces com o sufixo `Interface` ou `Protocol` (ex: `SensorRepositoryInterface`).
