import os
import warnings
from pydriller import Repository


def collect_commits(repo_url: str, max_commits: int | None = None, skip_errors: bool = True):
    """
    Coleta commits de um repositório Git.
    
    Args:
        repo_url: URL do repositório Git
        max_commits: Número máximo de commits para coletar
        skip_errors: Se True, pula commits com erros e continua. Se False, levanta exceção.
    
    Returns:
        Lista de dicionários com informações dos commits
    """
    commit_data = []
    count = 0
    errors_skipped = 0
    cache_dir = os.path.join(os.getcwd(), '.cache', 'repoinsight')
    os.makedirs(cache_dir, exist_ok=True)

    try:
        repository = Repository(repo_url, clone_repo_to=cache_dir)
        
        for commit in repository.traverse_commits():
            try:
                commit_info = {
                    'hash': commit.hash,
                    'author': commit.author.name,
                    'date': commit.author_date,
                    'message': commit.msg,
                    'lines_added': commit.insertions,
                    'lines_deleted': commit.deletions,
                    'files_changed': len(commit.modified_files),
                    'files': [],
                    'path': commit.project_path,
                    'dmm_unit_complexity': commit.dmm_unit_complexity,
                    'dmm_unit_interfacing': commit.dmm_unit_interfacing,
                    'dmm_unit_size': commit.dmm_unit_size,
                }

                # Tentar coletar informações dos arquivos modificados
                for m in commit.modified_files:
                    try:
                        commit_info["files"].append({
                            "filename": m.filename,
                            "new_path": m.new_path,
                            "old_path": m.old_path,
                            "added_lines": m.added_lines,
                            "removed_lines": m.deleted_lines,
                            "complexity": m.complexity,   # radon integrado!
                            "source_code": m.source_code, # conteúdo do arquivo pós-commit
                        })
                    except (ValueError, AttributeError, Exception) as e:
                        # Se houver erro ao processar um arquivo específico, continua
                        if skip_errors:
                            warnings.warn(f"Erro ao processar arquivo no commit {commit.hash}: {str(e)}")
                            continue
                        else:
                            raise

                commit_data.append(commit_info)
                count += 1
                
                if max_commits is not None and count >= max_commits:
                    break
                    
            except (ValueError, AttributeError, Exception) as e:
                # Erro ao processar um commit específico
                if skip_errors:
                    errors_skipped += 1
                    warnings.warn(f"Erro ao processar commit {getattr(commit, 'hash', 'unknown')}: {str(e)}. Pulando...")
                    continue
                else:
                    raise
                    
    except Exception as e:
        error_msg = f"Erro ao acessar o repositório {repo_url}: {str(e)}\n"
        error_msg += "Dica: Tente limpar o cache com --clear-cache ou verifique se a URL do repositório está correta."
        raise RuntimeError(error_msg) from e

    if errors_skipped > 0:
        warnings.warn(f"Total de {errors_skipped} commit(s) foram pulados devido a erros.")

    return commit_data