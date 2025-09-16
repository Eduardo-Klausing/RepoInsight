RepoInsight
## Mineração de Repositórios de Software  

### 1. Membros do Grupo  
- Eduardo Klausing Gervásio Muniz 
- Flávio Gabriel Soares Melo  
- Gabriel Arcanjo Campelo Fadoul
  
---

### 2. Explicação do Sistema  
O sistema consiste em uma ferramenta de **linha de comando (CLI)** que analisa a contribuição da equipe em projetos de software hospedados em repositórios Git/GitHub.  

O foco principal é:  
- **Métricas de contribuição**  
  - Número total de commits por autor.  
  - Frequência de commits ao longo do tempo.  
  - Issues abertas e fechadas por cada colaborador.  
  - Cálculo do **bus factor** → identificar se apenas um desenvolvedor é responsável por grande parte do código.  

- **Métricas de qualidade do código**  
  - Contagem de linhas de código por arquivo/módulo (complexidade estrutural).  
  - Identificação de **bugs potenciais e falhas de segurança** usando analisadores estáticos (Bandit para Python, PMD para múltiplas linguagens).  

A ferramenta será executada via terminal e poderá gerar relatórios resumidos para auxiliar na avaliação de manutenção e qualidade do projeto.  

---

### 3. Tecnologias Utilizadas  

- **Mineração e Análise de Repositórios**  
  - [Git](https://git-scm.com/) → coleta do histórico de commits.  
  - [PyDriller](https://github.com/ishepard/pydriller) → extração de informações de commits, autores e datas.  
  - [PyGithub](https://github.com/PyGithub/PyGithub) → análise de issues, pull requests e dados do GitHub.  
  - [GitPython](https://github.com/gitpython-developers/GitPython) → interação direta com repositórios Git.  

- **Análise de Código**  
  - [Bandit](https://github.com/PyCQA/bandit) → análise de vulnerabilidades em Python.  
  - [PMD](https://github.com/pmd/pmd) → análise estática para detectar bugs em múltiplas linguagens.  

- **Interface de Linha de Comando (CLI)**  
  - [Typer](https://github.com/fastapi/typer) → construção da interface amigável em linha de comando.  

---

### Decisões Importantes  
- **Origem dos dados**: Git + GitHub.  
- **Artefatos analisados**: commits, issues, código-fonte.  
- **Resultados apresentados**: métricas por autor, histórico de contribuição, contagem de linhas de código, vulnerabilidades potenciais.  
- **Objetivo principal**: ajudar equipes a identificar concentração de trabalho em poucos membros e problemas de manutenção/segurança.

- Possibilidades de implementação:
- 1: Rodar bandits através dos diffs dos commits
- 2: Rodar bandit através de todos os arquivos que contém dependências do diff
- 3: Rodar bandit através do projeto inteiro de cada commit

---
