"""
Testes para o módulo commit_analyzer
"""
import pytest
from analyzers.commit_analyzer import CommitAnalyzer, run_cmd


class TestCommitAnalyzer:
    """Testes para a classe CommitAnalyzer"""
    
    def test_analyze_commit_with_files(self):
        """Teste 4: Verifica análise de commit com arquivos"""
        analyzer = CommitAnalyzer()
        commit_info = {
            "hash": "abc123",
            "author": "Test Author",
            "files": [
                {
                    "filename": "test.py",
                    "new_path": "test.py",
                    "old_path": "test.py",
                    "added_lines": 10,
                    "removed_lines": 5,
                    "complexity": 5,
                    "source_code": "def hello():\n    print('Hello')\n"
                }
            ]
        }
        
        result = analyzer.analyze_commit(commit_info)
        
        assert result["sha"] == "abc123"
        assert result["author"] == "Test Author"
        assert result["complexity"] == 5
        assert len(result["files_analyzed"]) > 0
        assert "flake8" in result
    
    def test_analyze_commit_without_source_code(self):
        """Teste 5: Verifica análise de commit sem source_code"""
        analyzer = CommitAnalyzer()
        commit_info = {
            "hash": "def456",
            "author": "Test Author",
            "files": [
                {
                    "filename": "test.py",
                    "new_path": "test.py",
                    "old_path": "test.py",
                    "added_lines": 10,
                    "removed_lines": 5,
                    "complexity": None,
                    "source_code": None
                }
            ]
        }
        
        result = analyzer.analyze_commit(commit_info)
        
        assert result["sha"] == "def456"
        assert result["complexity"] == 0
        assert len(result["files_analyzed"]) == 0
    
    def test_analyze_commit_empty_files(self):
        """Teste 6: Verifica análise de commit com lista de arquivos vazia"""
        analyzer = CommitAnalyzer()
        commit_info = {
            "hash": "ghi789",
            "author": "Test Author",
            "files": []
        }
        
        result = analyzer.analyze_commit(commit_info)
        
        assert result["sha"] == "ghi789"
        assert result["complexity"] == 0
        assert len(result["files_analyzed"]) == 0


class TestRunCmd:
    """Testes para a função run_cmd"""
    
    def test_run_cmd_success(self):
        """Teste 7: Verifica execução de comando bem-sucedido"""
        returncode, out, err = run_cmd("echo test")
        
        assert returncode == 0
        assert isinstance(out, str)
        assert isinstance(err, str)
    
    def test_run_cmd_failure(self):
        """Teste 8: Verifica execução de comando que falha"""
        returncode, out, err = run_cmd("nonexistentcommand12345")
        
        # O comando deve falhar (returncode != 0)
        assert returncode != 0

