# Fase 004: Controladores e Injeção de Dependências (FastAPI) e Implementação de Rotas e Engine de Simulação Dinâmica

**Objetivo 1:** Expor as rotas REST que o app React Native irá consumir e o endpoint para injeção simulada.

**Arquivos a criar/modificar:**

- `src/presentation/api/dependencies.py`
- `src/presentation/api/routers/classroom_router.py`
- `src/presentation/api/routers/simulation_router.py`
- `src/presentation/api/main.py`

**Instruções de Codificação:**

1. Em `dependencies.py`, crie os generators (`yield`) para a `AsyncSession` e factories para injetar os Repositórios e Use Cases (`def get_classroom_use_case(...)`).
2. Em `classroom_router.py`, defina um `APIRouter`. Crie a rota `GET /{id}` retornando o status da sala. Crie a rota `POST /{id}/toggle_light` que chama um Use Case e retorna status HTTP 200.
3. Em `simulation_router.py`, crie a rota `POST /simulate/month` que aceita uma lista de `SensorPayloadDTO` (simulando 1 mês de dados) e processa em lote via repository.
4. Em `main.py`, instancie `FastAPI()`. No `lifespan`, inicie o `start_mqtt_listener()` criado na Fase 003 como uma background task. Inclua os routers criadaos.

**Critérios de Aceitação (Hard Constraints):**

- Documentação OpenAPI (Swagger) totalmente preenchida e testável para as rotas.
- Padrão RESTFUL estrito. As rotas dependem (`Depends()`) exclusivamente das Factories.

**Objetivo 2:** Criar os endpoints REST sob o prefixo `/api` e codificar os algoritmos da engine de simulação matemática que reagem às ações de toggle do usuário.

**Lógica da Engine de Simulação (Mandatória):**
Toda requisição para `GET /api/dashboard` ou `GET /api/rooms` deve calcular dados em tempo real baseando-se no estado atual das salas no banco de dados.

1. **Fórmula do Consumo Atual (`currentConsumption`):**
   - Defina uma constante `CONSUMO_BASE = 25.0` (kWh).
   - `currentConsumption = CONSUMO_BASE + somatório(energy_usage)` de todas as salas onde `status == 'active'`.
2. **Fórmula da Temperatura Média (`avgTemperature`):**
   - Para cada sala no banco de dados:
     - Se `status == 'active'`, o valor da coluna `temperature` deve convergir/ser fixado em `21.0` (Celsius).
     - Se `status == 'inactive'`, o valor da coluna `temperature` deve convergir/ser fixado em `25.5` (Celsius).
   - O campo `avgTemperature` do dashboard deve ser a média aritmética simples de todas as salas cadastradas.
3. **Regra de Negócio para o Status Geral (`systemStatus`):**
   - Retorne `"optimal"` se `currentConsumption < (0.75 * consumptionMax)`.
   - Retorne `"warning"` se `currentConsumption` estiver entre `75%` e `95%` de `consumptionMax`.
   - Retorne `"critical"` se `currentConsumption > (0.95 * consumptionMax)` OU se `avgTemperature > 26.0`.

**Mapeamento Exato de Endpoints:**
- `POST /api/auth/login` -> Payload: `{"email": "...", "password": "..."}`. Retorno: status 200 com token JWT e objeto `user`.
- `GET /api/rooms` -> Retorno: Lista de salas com valores calculados dinamicamente pela engine.
- `POST /api/rooms/{id}/toggle` -> Payload: `{"status": "active" | "inactive"}`. Altera o estado no banco de dados e roda a recomputação da engine imediatamente, retornando o objeto da sala modificado.
- `GET /api/rooms/sensors/external` -> Retorna dados estáticos ou randômicos da estação meteorológica simulada.
- `GET /api/dashboard` -> Retorna as métricas consolidadas agregadas de consumo e economia.

**Critérios de Aceitação (Hard Constraints):**
- O frontend envia requisições HTTP para `/rooms/:id/toggle` mas o código do serviço executa via axios apontando para `/rooms/${id}/toggle`. Garanta que a rota FastAPI capture o ID como path parameter (`/api/rooms/{id}/toggle`).
- Ative a flag `populate_by_name=True` em todos os Schemas de apresentação Pydantic para garantir que o output enviado via HTTP seja convertido automaticamente para camelCase.