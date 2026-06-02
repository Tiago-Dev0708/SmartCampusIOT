# Fase 006: Algoritmo LightGBM e Endpoint de ML e  Acoplamento do Modelo preditivo LightGBM ao Analytics do Mobile

**Objetivo 1:** Treinar o modelo a partir do HDFS e expor a predição para o React Native.

**Arquivos a criar/modificar:**

- `src/infra/ml/lightgbm_service.py`
- `src/application/use_cases/train_model_use_case.py`
- `src/application/use_cases/predict_economy_use_case.py`
- `src/presentation/api/routers/ml_router.py`

**Instruções de Codificação:**

1. Em `lightgbm_service.py`, crie `ModelManager` (Singleton). Ele deve ter o método `load_model()` (carrega o `.txt` salvo via `lgb.Booster(model_file)`) e `predict(features: dict)`.
2. Em `train_model_use_case.py`, implemente a busca do CSV do HDFS, crie os conjuntos de treino com `lightgbm.Dataset`, treine o `lgb.train()` e salve o artefato em disco.
3. Em `predict_economy_use_case.py`, pegue os parâmetros da requisição (temperatura, umidade do solo atual, presenças), passe pelo Singleton do LightGBM e retorne a projeção de custo de água/energia em Reais.
4. Conecte isso às rotas `POST /ml/train` e `GET /ml/predict` no router.

**Critérios de Aceitação (Hard Constraints):**

- A API deve instanciar o modelo LightGBM durante a inicialização (startup event/lifespan) e não a cada requisição na rota `/predict`.

**Objetivo 2:** Alimentar a tela de Analytics avançada do aplicativo com dados gerados pelo modelo tabular do LightGBM.

**Contrato de Resposta do Endpoint (`GET /api/analytics`):**
A resposta deve preencher rigorosamente as propriedades consumidas pela Bento Grid do React Native:
- `totalConsumption`: Valor consolidado em kWh.
- `efficiencyPercent`: Porcentagem de ganho de eficiência calculado pelo modelo (ex: comparação com o baseline).
- `co2Reduction`: Multiplicador estático ou dinâmico sobre a energia economizada (fórmula sugerida: `energia_economizada * 0.0004` toneladas de CO2).
- `projectedCost`: Gasto financeiro previsto pelo LightGBM com base nos padrões atuais de ativação de salas.
- `projectedCostBaseline`: Gasto que a escola teria sem o sistema IoT ativo.
- `predictedGoalDays`: Quantidade de dias calculada pelo modelo preditivo para atingir a meta sustentável estabelecida pela prefeitura.
- `chart`: Histórico real (WeeklyDataPoint).
- `forecastChart`: Curva de predição gerada pela inferência do LightGBM (WeeklyDataPoint com flag `isFuture: true`).

**Critérios de Aceitação (Hard Constraints):**
- Caso o arquivo do modelo LightGBM (`.txt` ou `.pkl`) não seja encontrado no diretório local durante o startup no `lifespan`, a API deve capturar a exceção e carregar um modelo de contingência matemático linear simples para não quebrar a rota `/api/analytics` do aplicativo móvel.