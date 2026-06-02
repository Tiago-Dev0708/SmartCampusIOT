# Skill: Machine Learning Engineer (Time Series & Tabular Data)

**1. Pipeline de LightGBM:**
- Utilize `lightgbm` via sua API Python padrão (`import lightgbm as lgb`).
- Separe rigidamente o código em `treinamento` (script/use_case apartado) e `inferência` (serviço carregado em memória).

**2. Carregamento do Modelo (Inference):**
- O modelo `.txt` ou `.pkl` deve ser carregado APENAS UMA VEZ usando o padrão Singleton, preferencialmente durante o evento `lifespan` do FastAPI, para evitar latência nas requisições do app mobile.

**3. Constraints de Dados:**
- Antes do modelo processar o JSON recebido na inferência, os dados devem ser validados via um Pydantic Schema.
- Impute valores nulos e trate outliers na camada de transformação (Feature Engineering) antes de passar para o `model.predict()`.