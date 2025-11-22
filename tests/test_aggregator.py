"""
Testes para o módulo aggregator
"""
import pytest
from metrics.aggregator import aggregate


class TestAggregator:
    """Testes para a função aggregate"""
    
    def test_aggregate_single_author(self):
        """Teste 9: Verifica agregação com um único autor"""
        author_commit_results = [
            {
                "author": "Author1",
                "complexity": 10,
                "flake8": {
                    "output": "line1\nline2",
                    "errors": ""
                }
            },
            {
                "author": "Author1",
                "complexity": 5,
                "flake8": {
                    "output": "line3",
                    "errors": "error1"
                }
            }
        ]
        
        result = aggregate(author_commit_results)
        
        assert "Author1" in result
        assert result["Author1"]["commits"] == 2
        assert result["Author1"]["complexity_sum"] == 15
        assert result["Author1"]["flake8_messages"] == 4  # 2 + 1 + 1
        assert "maintainability" in result["Author1"]
        assert "quality" in result["Author1"]
        assert "final_score" in result["Author1"]
    
    def test_aggregate_multiple_authors(self):
        """Teste 10: Verifica agregação com múltiplos autores"""
        author_commit_results = [
            {
                "author": "Author1",
                "complexity": 10,
                "flake8": {"output": "", "errors": ""}
            },
            {
                "author": "Author2",
                "complexity": 5,
                "flake8": {"output": "line1", "errors": ""}
            },
            {
                "author": "Author1",
                "complexity": 3,
                "flake8": {"output": "", "errors": ""}
            }
        ]
        
        result = aggregate(author_commit_results)
        
        assert "Author1" in result
        assert "Author2" in result
        assert result["Author1"]["commits"] == 2
        assert result["Author2"]["commits"] == 1
        assert result["Author1"]["complexity_sum"] == 13
        assert result["Author2"]["complexity_sum"] == 5
        assert result["Author2"]["flake8_messages"] == 1
    
    def test_aggregate_empty_list(self):
        """Teste 11: Verifica agregação com lista vazia"""
        result = aggregate([])
        
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_aggregate_no_flake8(self):
        """Teste 12: Verifica agregação quando flake8 não está presente"""
        author_commit_results = [
            {
                "author": "Author1",
                "complexity": 10
            }
        ]
        
        result = aggregate(author_commit_results)
        
        assert "Author1" in result
        assert result["Author1"]["flake8_messages"] == 0
    
    def test_aggregate_scores_calculation(self):
        """Teste 13: Verifica cálculo correto dos scores"""
        author_commit_results = [
            {
                "author": "Author1",
                "complexity": 0,  # Complexidade zero
                "flake8": {"output": "", "errors": ""}
            }
        ]
        
        result = aggregate(author_commit_results)
        
        author_data = result["Author1"]
        # Com complexidade 0 e sem erros flake8, maintainability deve ser próximo de 1
        assert author_data["maintainability"] > 0.9
        assert author_data["quality"] > 0.9
        assert 0 <= author_data["final_score"] <= 1

