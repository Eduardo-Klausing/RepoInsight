from collectors.commit_collector import collect_commits
from analyzers.commit_analyzer import CommitAnalyzer
from metrics.aggregator import aggregate
import json

def main():

    print("[1] Coletando commits...")
    commits = collect_commits()

    print("[2] Analisando commits (Bandit, flake8, complexidade)...")
    ca = CommitAnalyzer()

    analyzed = []
    for c in commits:
        res = ca.analyze_commit(c)
        analyzed.append(res)

    print("[3] Agregando métricas por autor...")
    report = aggregate(analyzed)

    print("[4] Salvando resultado final...")
    with open("analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Done.")

if __name__ == "__main__":
    import sys
    main()
