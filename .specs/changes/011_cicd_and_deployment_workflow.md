# Fase 011: Workflow CI/CD, Build Otimizado e Deploy On-Premise

**Objetivo:** Automatizar o build da imagem Docker, os testes de lint/segurança e preparar a entrega contínua para o servidor CachyOS rodando a infra de Zero Trust.

**Arquivos a criar/modificar:**

- `.github/workflows/main.yml` (ou o equivalente para sua ferramenta CI/CD)
- `Dockerfile` (Aprimoramento da Spec 007)
- `deploy.sh` (Script local para o servidor)

**Instruções de Codificação:**

1. **Dockerfile Otimizado:** Atualize o Dockerfile para usar Multi-stage builds com cache eficiente. Use ferramentas modernas como `uv` ou `poetry` para instalar dependências em um stage de builder temporário e apenas copie a roda (`.whl`) compilada para o container final, reduzindo a superfície de ataque e o tamanho da imagem.
2. **Workflow YAML:** Configure um pipeline com os seguintes jobs:
   - `lint_and_test`: Roda `Ruff` (linter/formatter) e Mypy.
   - `security_scan`: Roda `bandit` ou similar para detectar vulnerabilidades no código.
   - `build_and_deploy`: Faz o build da imagem e faz o push para o ambiente alvo.
3. **Deploy CachyOS:** Escreva o `deploy.sh` e especifique no CI/CD os comandos para atualizar os containers. O deploy será feito via acesso SSH pelo túnel Cloudflare ou usando um Self-Hosted Runner na própria máquina.
4. **Alerta para a IA:** *Se informações cruciais sobre a configuração do runner (ex: chaves SSH, Secrets do Github, variáveis do DuckDNS) não estiverem presentes no contexto, você DEVE interromper a geração desta Spec e solicitar explicitamente ao usuário os parâmetros de infraestrutura faltantes.*

**Critérios de Aceitação (Hard Constraints):**

- O processo de build Docker não pode demorar minutos processando pip installs desnecessários. O cache de camadas deve estar configurado corretamente no CI.
- O pipeline deve falhar e barrar o deploy se a análise do `Mypy` ou do `Ruff` encontrar erros na base de código.
