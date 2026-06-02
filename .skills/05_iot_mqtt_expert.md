# Skill: IoT & Data Ingestion Architect

**1. Gerenciamento Assíncrono MQTT:**
- Use a biblioteca `aiomqtt` (assíncrona).
- A conexão MQTT deve ser gerenciada pelo `lifespan` manager do FastAPI (`@asynccontextmanager def lifespan(app: FastAPI):`).
- O loop de escuta de mensagens MQTT deve rodar como uma Task em background (`asyncio.create_task()`) para não bloquear a thread principal que serve as requisições HTTP do app mobile.

**2. Resiliência e Tópicos:**
- Assine tópicos no formato: `smartcampus/+/sensors/#`.
- Nível de Qualidade de Serviço: Use `QoS 1` para garantir a entrega das medições do ESP32-S3.
- Todo payload recebido DEVE ser convertido em um schema Pydantic `SensorPayloadDTO` e só depois repassado ao `SaveSensorDataUseCase`. Se o JSON for inválido, faça log do erro, descarte a mensagem e não interrompa a task.