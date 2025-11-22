"""
Testes para o módulo commit_collector
"""
import pytest
from collectors.commit_collector import collect_commits


class TestCommitCollector:
    """Testes para a função collect_commits"""
    
    def test_collect_commits_basic(self):
        """Teste 1: Verifica se collect_commits retorna uma lista"""
        # Usando um repositório pequeno para teste
        repo_url = "https://github.com/ishepard/pydriller"
        result = collect_commits(repo_url, max_commits=1)
        
        assert isinstance(result, list)
        assert len(result) >= 0
    
    def test_collect_commits_with_max_commits(self):
        """Teste 2: Verifica se max_commits limita o número de commits coletados"""
        repo_url = "https://github.com/ishepard/pydriller"
        max_commits = 3
        result = collect_commits(repo_url, max_commits=max_commits)
        
        assert len(result) <= max_commits
    
    def test_collect_commits_structure(self):
        """Teste 3: Verifica se a estrutura dos dados coletados está correta"""
        repo_url = "https://github.com/ishepard/pydriller"
        result = collect_commits(repo_url, max_commits=1)
        
        if len(result) > 0:
            commit = result[0]
            assert "hash" in commit
            assert "author" in commit
            assert "date" in commit
            assert "message" in commit
            assert "lines_added" in commit
            assert "lines_deleted" in commit
            assert "files_changed" in commit
            assert "files" in commit
            assert isinstance(commit["files"], list)

