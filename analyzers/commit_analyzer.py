import os, subprocess, tempfile, json, re

def run_cmd(cmd, cwd=None):
    p = subprocess.run(cmd, shell=True, cwd=cwd,
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

class CommitAnalyzer:

    def analyze_commit(self, commit_info):
        """
        commit_info = dict produzido pelo coletor via PyDriller
        """

        results = {
            "sha": commit_info["hash"],
            "author": commit_info["author"],
            "bandit": [],
            "pylint": [],
            "flake8": {"output": "", "errors": ""},
            "complexity": 0,
            "files_analyzed": []
        }

        file_paths = []

        with tempfile.TemporaryDirectory() as tmpdir:

            # salva os arquivos alterados do commit nesse tmpdir
            for f in commit_info["files"]:
                if not f["source_code"]:
                    continue

                path = os.path.join(tmpdir, f["filename"])
                dirpath = os.path.dirname(path)
                os.makedirs(dirpath, exist_ok=True)

                with open(path, "w", encoding="utf-8") as fp:
                    fp.write(f["source_code"])

                results["files_analyzed"].append(path)

                file_paths.append(path)

                # complexidade (já vem do PyDriller / radon)
                if f["complexity"] is not None:
                    results["complexity"] += f["complexity"]

            # --- Rodar Bandit ---
            cmd_bandit = f"bandit -r {tmpdir} -f json"
            _, outb, _ = run_cmd(cmd_bandit)

            try:
                results["bandit"] = json.loads(outb).get("results", [])
            except:
                results["bandit"] = []

            # --- Rodar Flake8 ---
            if len(file_paths) > 0:
                files_str = " ".join(file_paths)

                cmd_flake8 = f"flake8 {files_str}"
                _, out_flake, err_flake = run_cmd(cmd_flake8)

                results["flake8"]["output"] = out_flake
                results["flake8"]["errors"] = err_flake

        return results
