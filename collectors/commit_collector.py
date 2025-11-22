import os
from pydriller import Repository


def collect_commits(repo_url: str = 'https://github.com/ishepard/pydriller', max_commits: int | None = None):
    commit_data = []
    count = 0
    cache_dir = os.path.join(os.getcwd(), '.cache', 'repoinsight')
    os.makedirs(cache_dir, exist_ok=True)

    for commit in Repository(repo_url, clone_repo_to=cache_dir).traverse_commits():
        commit_data.append({
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
        })

        for m in commit.modified_files:
            commit_data[-1]["files"].append({
                "filename": m.filename,
                "new_path": m.new_path,
                "old_path": m.old_path,
                "added_lines": m.added_lines,
                "removed_lines": m.deleted_lines,
                "complexity": m.complexity,   # radon integrado!
                "source_code": m.source_code, # conteúdo do arquivo pós-commit
            })
        count += 1
        if max_commits is not None and count >= max_commits:
            break

    return commit_data