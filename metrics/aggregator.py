from collections import defaultdict

def aggregate(author_commit_results):

    authors = defaultdict(lambda: {
        "commits": 0,
        "complexity_sum": 0,
        "flake8_messages": 0,
    })

    for c in author_commit_results:
        author = c["author"]
        authors[author]["commits"] += 1
        authors[author]["complexity_sum"] += c["complexity"]

        flake8_output = c.get("flake8", {})
        out = flake8_output.get("output", "")
        err = flake8_output.get("errors", "")

        if out or err:
            count_out = len([line for line in out.splitlines() if line.strip()])
            count_err = len([line for line in err.splitlines() if line.strip()])
            authors[author]["flake8_messages"] += (count_out + count_err)

    results = {}
    for author, m in authors.items():
        commits = m["commits"]
        M = 1 / (1 + m["complexity_sum"] / commits if commits > 0 else 0)
        Q = 1 / (1 + m["flake8_messages"])

        final_score = 0.6*M + 0.4*Q

        results[author] = {
            **m,
            "maintainability": M,
            "quality": Q,
            "final_score": final_score
        }

    return results
