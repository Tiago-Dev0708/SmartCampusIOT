# Fase 003: Integração MQTT e Ingestão de Dados

**Objetivo:** Processar o fluxo de dados do microcontrolador ESP32-S3 em background.

**Arquivos a criar/modificar:**

- `src/application/use_cases/save_sensor_data.py`
- `src/infra/mqtt/client.py`
- `src/presentation/api/schemas/mqtt_schemas.py`

**Instruções de Codificação:**

1. Crie o schema Pydantic `SensorPayloadDTO` em `mqtt_schemas.py` para validar o JSON bruto recebido do ESP32.
2. Crie `SaveSensorDataUseCase`. O método `execute` deve receber o DTO, convertê-lo em `SensorDataEntity` e chamar `self.sensor_repo.save()`.
3. Em `client.py`, crie a função `async def start_mqtt_listener()`. Ela deve usar `aiomqtt.Client`, conectar ao broker, assinar os tópicos, e em um loop `async for message in client.messages:`, fazer o parse do JSON, instanciar o Use Case e processar.

**Critérios de Aceitação (Hard Constraints):**

- Qualquer erro no payload JSON (ex: chave ausente) deve lançar um erro capturado no próprio loop do MQTT (ex: `except ValidationError`), logado com a biblioteca `logging`, sem quebrar a execução do Listener.
