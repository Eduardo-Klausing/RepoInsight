import pandas as pd
from pydriller import Repository


def collect_commits():
    commit_data = []

    for commit in Repository('https://github.com/TheAlgorithms/Python').traverse_commits():
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

    #df_commits = pd.DataFrame(commit_data)
    #df_commits.head()

    return commit_data