from collections import defaultdict

def aggregate(author_commit_results):

    authors = defaultdict(lambda: {
        "commits": 0,
        "complexity_sum": 0,
        "bandit_issues": 0,
        "bandit_high": 0,
        "flake8_messages": 0,
    })

    for c in author_commit_results:
        author = c["author"]
        authors[author]["commits"] += 1
        authors[author]["complexity_sum"] += c["complexity"]

        # Bandit
        for issue in c["bandit"]:
            authors[author]["bandit_issues"] += 1
            if issue["issue_severity"] == "HIGH":
                authors[author]["bandit_high"] += 1

        # flake8
        flake8_output = c.get("flake8", {})
        out = flake8_output.get("output", "")

        if out:
            # Cada linha de saída é uma violação
            count = len([line for line in out.splitlines() if line.strip()])
            authors[author]["flake8_messages"] += count

    # calcular scores
    results = {}
    for author, m in authors.items():
        commits = m["commits"]
        security_score = m["bandit_high"]*3 + m["bandit_issues"]
        M = 1 / (1 + m["complexity_sum"] / commits if commits > 0 else 0)
        Q = 1 / (1 + m["flake8_messages"])
        S = 1 / (1 + security_score)

        final_score = 0.4*M + 0.2*Q + 0.4*S

        results[author] = {
            **m,
            "maintainability": M,
            "quality": Q,
            "security": S,
            "final_score": final_score
        }

    return results
