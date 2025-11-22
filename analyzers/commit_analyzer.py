import os, subprocess, tempfile, json, re, shutil

def run_cmd(cmd, cwd=None):
    p = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=False,
    )
    out = p.stdout.decode("utf-8", "ignore") if p.stdout else ""
    err = p.stderr.decode("utf-8", "ignore") if p.stderr else ""
    return p.returncode, out, err

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

        tmpdir = tempfile.mkdtemp()
        try:
            for f in commit_info["files"]:
                if not f["source_code"]:
                    continue

                path = os.path.join(tmpdir, f["filename"])
                dirpath = os.path.dirname(path)
                os.makedirs(dirpath, exist_ok=True)

                with open(path, "w", encoding="utf-8", errors="ignore") as fp:
                    fp.write(f["source_code"] or "")

                results["files_analyzed"].append(path)
                file_paths.append(path)

                if f["complexity"] is not None:
                    results["complexity"] += f["complexity"]

            results["bandit"] = []

            if len(file_paths) > 0:
                files_str = " ".join(file_paths)
                #cmd_flake8 = f"flake8 --exit-zero {files_str}"
                cmd_flake8 = f"flake8 --isolated --disable-noqa --exit-zero {tmpdir}"
                #out_flake, err_flake = run_cmd(cmd_flake8)
                _, out_flake, err_flake = run_cmd(cmd_flake8)
                results["flake8"]["output"] = out_flake or ""
                results["flake8"]["errors"] = err_flake or ""
        finally:
            try:
                shutil.rmtree(tmpdir, ignore_errors=True)
            except Exception:
                pass

        return results
