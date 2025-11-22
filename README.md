RepoInsight

### TP: Mineração de Repositórios de Software

**Objetivo**
- Desenvolver uma ferramenta de linha de comando que identifique problemas relevantes de manutenção/evolução de software por meio da mineração de repositórios.

**Membros do grupo**
- Eduardo Klausing Gervásio Muniz
- Flávio Gabriel Soares Melo
- Gabriel Arcanjo Campelo Fadoul

**Tecnologias utilizadas**
- PyDriller: extração de commits, autores, arquivos e métricas de complexidade.
- Flake8: verificação de estilo/qualidade, contabilizada em relatórios.
- Typer: CLI organizada com comandos.
- Rich: saída visual (tabelas e progresso) no terminal.

**Instalação**
- `pip install -r requirements.txt`

**Como utilizar**
- Executar a mineração e análise:
  - `python scripts/run_analysis.py run`
  - Opções:
    - `--repo-url <url>` para escolher o repositório
    - `--max-commits <N>` para limitar commits
- Visualizar ranking geral (score final):
  - `python scripts/run_analysis.py view --top 10 --sort-by final_score`
- Top por número de commits (detalhado):
  - `python scripts/run_analysis.py top --top 20 --detailed`

**Como executar os testes localmente**
- `pytest` ou `python -m pytest`
- Os testes devem cobrir coleta (PyDriller), análise (Flake8) e agregação de métricas.

**GitHub Actions**
- Configure um workflow para executar `pytest` automaticamente em cada push/PR.
- Exemplo de passos: checkout, setup Python, instalar dependências, rodar testes.

**Especificação atendida**
- CLI com comandos (`run`, `view`, `top`).
- Mineração de repositórios e agregação de métricas de manutenção e qualidade (Flake8).
- Coluna de Flake8 contabilizada no relatório de autores.

**Nota sobre segurança**
- A contagem de vulnerabilidades via Bandit foi descontinuada para estabilizar a análise em múltiplas plataformas.
- O score final agora considera apenas:
  - `M` (Maintainability): inversamente proporcional à complexidade agregada por autor.
  - `Q` (Quality): inversamente proporcional ao total de mensagens do Flake8.
  - `Score`: `0.6*M + 0.4*Q`.
