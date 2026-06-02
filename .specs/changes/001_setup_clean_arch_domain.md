# Fase 001: Implementação da Camada de Domínio, Core da Aplicação e

# Modelagem do Domínio Baseado nos Contratos Mobile

**Objetivo 1:** Estabelecer o coração da aplicação com Entidades e Interfaces puras.

**Arquivos a criar/modificar:**

- `src/domain/entities/sensor_data.py`
- `src/domain/entities/classroom.py`
- `src/domain/interfaces/repositories.py` 

**Instruções de Codificação:**

1. Em `sensor_data.py`, crie a `dataclass` `SensorDataEntity` com os campos: `id` (UUID), `device_id` (str), `sensor_type` (str: 'presence', 'light', 'soil_moisture', 'temperature'), `value` (float), `timestamp` (datetime).
2. Em `classroom.py`, crie a `dataclass` `ClassroomEntity` com os campos: `id` (UUID), `name` (str), `is_occupied` (bool), `light_status` (bool), `last_updated` (datetime). Adicione métodos de comportamento à entidade, como `update_occupancy(self, status: bool)`.
3. Em `repositories.py`, importe `ABC` e `abstractmethod`. Crie `SensorRepositoryInterface` (método: `async def save(self, sensor_data: SensorDataEntity) -> None`) e `ClassroomRepositoryInterface` (métodos: `async def get_by_id(self, id: UUID) -> ClassroomEntity | None`, `async def update(self, classroom: ClassroomEntity) -> None`).

**Critérios de Aceitação (Hard Constraints):**

- ZERO importações de `sqlalchemy`, `pydantic` ou `fastapi` em todos os arquivos desta spec.
- Mypy deve passar sem erros (tipagem explícita em todos os atributos e retornos).

**Objetivo 2:** Criar as entidades de domínio puras mapeando de forma exata os tipos requisitados pelo ecossistema React Native.

**Modelos de Domínio e Atributos Obrigatórios:**

1. `src/domain/entities/room.py` -> `RoomEntity`:
   - `id`: str (UUID gerado ou string incremental vinda do hardware)
   - `name`: str
   - `block`: str
   - `floor`: str
   - `status`: str (Restrito aos literais: 'active' ou 'inactive')
   - `temperature`: float
   - `energy_usage`: float
2. `src/domain/entities/external_sensors.py` -> `ExternalSensorsEntity`:
   - `temperature`: float
   - `humidity: float
   - `co2`: float
   - `wind_speed`: float
   - `status`: str ('active' | 'inactive')
3. `src/domain/entities/dashboard.py` -> `DashboardDataEntity` e `WeeklyDataPoint`:
   - `WeeklyDataPoint`: `day` (str), `value` (float), `is_current` (bool), `is_future` (bool)
   - `DashboardDataEntity`: `current_consumption` (float), `consumption_unit` (str: "kWh"), `consumption_max` (float), `avg_temperature` (float), `monthly_savings` (float), `savings_percent` (float), `system_status` (str: 'optimal' | 'warning' | 'critical'), `zone_count` (int), `savings_chart` (List[WeeklyDataPoint]), `realtime_chart` (List[WeeklyDataPoint])

**Critérios de Aceitação (Hard Constraints):**

- Proibido expor tipos TypeScript diretamente. O domínio usa tipos nativos Python.
- As validações de estado do `system_status` e `status` das salas devem ser garantidas por Enums ou literais estritos em Python.
