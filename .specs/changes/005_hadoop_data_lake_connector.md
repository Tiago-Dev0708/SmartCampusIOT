# Fase 005: Pipeline ETL para HDFS (Big Data)

**Objetivo:** Extrair dados consolidados do banco relacional PostgreSQL e exportar para o Hadoop.

**Arquivos a criar/modificar:**

- `src/infra/hadoop/hdfs_client.py`
- `src/application/use_cases/export_to_datalake.py`
- `src/presentation/api/routers/etl_router.py`

**Instruções de Codificação:**

1. Em `hdfs_client.py`, crie uma classe que inicialize o cliente `hdfs.InsecureClient` (ou equivalente) apontando para a URL do Namenode local.
2. Em `export_to_datalake.py`, crie o Use Case. Ele deve chamar o repositório do banco para buscar os dados de sensores do mês anterior, transformar essa massa de dados em um formato tabular (CSV string ou buffer Parquet via Pandas) e enviar para o `hdfs_client`.
3. Crie a rota `POST /etl/trigger_monthly_export` no `etl_router.py` para acionar esse Use Case sob demanda.

**Critérios de Aceitação (Hard Constraints):**

- O processamento de dados para conversão em DataFrame/CSV não deve travar a API (use `asyncio.to_thread` se a biblioteca HDFS for bloqueante/síncrona).
