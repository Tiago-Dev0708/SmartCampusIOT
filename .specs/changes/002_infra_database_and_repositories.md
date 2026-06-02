# Fase 002: Infraestrutura de Banco de Dados

**Objetivo:** Implementar os modelos físicos do banco e os adaptadores que satisfazem as interfaces do domínio.

**Arquivos a criar/modificar:**

- `src/infra/database/config.py`
- `src/infra/database/models.py --> caso tenhamos mais de uma model, usaremos a modularização onde fica models como pasta e após isso os arquivos para cada model dentro(inclusive, siga isso para todos os outros modulos também)`
- `src/infra/repositories/sensor_repository.py`
- `src/infra/repositories/classroom_repository.py`

**Instruções de Codificação:**

1. Em `config.py`, configure um `AsyncEngine` e `async_sessionmaker` usando `sqlalchemy.ext.asyncio`. Leia a URL do banco (PostgreSQL) usando `pydantic_settings`.
2. Em `models.py`, crie `Base = declarative_base()`. Crie as classes `SensorDataModel` e `ClassroomModel` usando as anotações do SQLAlchemy 2.0 (`Mapped[str]`, `mapped_column()`).
3. Nos repositórios, crie as classes concretas herdando das interfaces do domínio (ex: `class SensorRepositoryImpl(SensorRepositoryInterface):`).
4. **Crucial:** O método `save` do repositório deve receber a Entidade de Domínio, instanciar o Modelo SQLAlchemy correspondente (Mapeamento), adicionar à sessão e executar `commit()`.

**Critérios de Aceitação (Hard Constraints):**

- A injeção da sessão assíncrona (`AsyncSession`) deve ser via construtor (`__init__`) nos repositórios.
- Operações de I/O de banco devem utilizar `await`.
