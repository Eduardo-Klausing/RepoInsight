import sys, os
import shutil
from typer import Typer, Option, Argument
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
import json
import warnings
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from collectors.commit_collector import collect_commits
from analyzers.commit_analyzer import CommitAnalyzer
from metrics.aggregator import aggregate

app = Typer()
console = Console()

def _show_table(report, sort_by: str = "final_score", top: int = 10):
    table = Table(title="RepoInsight - Autores")
    table.add_column("Autor", style="cyan")
    table.add_column("Commits")
    table.add_column("Complexidade")
    table.add_column("Flake8")
    table.add_column("M", style="green")
    table.add_column("Q", style="green")
    table.add_column("Score", style="yellow")
    items = list(report.items())
    items.sort(key=lambda kv: kv[1].get(sort_by, 0), reverse=True)
    for author, m in items[:top]:
        table.add_row(
            author,
            str(m["commits"]),
            str(m["complexity_sum"]),
            str(m["flake8_messages"]),
            f"{m['maintainability']:.3f}",
            f"{m['quality']:.3f}",
            f"{m['final_score']:.3f}",
        )
    console.print(table)

def _show_top_commits(report, top: int = 20):
    items = list(report.items())
    items.sort(key=lambda kv: kv[1].get("commits", 0), reverse=True)
    top_items = items[:top]
    max_commits = max((m[1]["commits"] for m in top_items), default=1)
    table = Table(title="Top por commits")
    table.add_column("#")
    table.add_column("Autor", style="cyan")
    table.add_column("Commits", style="yellow")
    table.add_column("Bar")
    for idx, (author, m) in enumerate(top_items, start=1):
        commits = m["commits"]
        bar_len = 30
        filled = int((commits / max_commits) * bar_len)
        bar = "█" * filled + " " * (bar_len - filled)
        table.add_row(str(idx), author, str(commits), bar)
    console.print(table)

def _show_top_commits_full(report, top: int = 20):
    items = list(report.items())
    items.sort(key=lambda kv: kv[1].get("commits", 0), reverse=True)
    top_items = items[:top]
    max_commits = max((m[1]["commits"] for m in top_items), default=1)
    table = Table(title="Top 20 por commits (detalhado)")
    table.add_column("#")
    table.add_column("Autor", style="cyan")
    table.add_column("Commits", style="yellow")
    table.add_column("Complexidade")
    table.add_column("Flake8")
    table.add_column("M", style="green")
    table.add_column("Q", style="green")
    table.add_column("Score", style="yellow")
    table.add_column("Bar")
    for idx, (author, m) in enumerate(top_items, start=1):
        commits = m["commits"]
        bar_len = 20
        filled = int((commits / max_commits) * bar_len)
        bar = "█" * filled + " " * (bar_len - filled)
        table.add_row(
            str(idx),
            author,
            str(commits),
            str(m["complexity_sum"]),
            str(m["flake8_messages"]),
            f"{m['maintainability']:.3f}",
            f"{m['quality']:.3f}",
            f"{m['final_score']:.3f}",
            bar,
        )
    console.print(table)

@app.command()
def run(
    repo_url: str = Argument(..., help="URL do repositório Git (ex: https://github.com/user/repo)"),
    max_commits: int | None = Option(None, "--max-commits", help="Número máximo de commits para analisar"),
    min_commits: int | None = Option(0, "--min-commits", help="Número mínimo de commits por autor"),
    clear_cache: bool = Option(False, "--clear-cache", help="Limpa o cache do repositório antes de coletar"),
):
    # Limpar cache se solicitado
    if clear_cache:
        cache_dir = os.path.join(os.getcwd(), '.cache', 'repoinsight')
        if os.path.exists(cache_dir):
            console.print("[yellow]Limpando cache...[/yellow]")
            try:
                shutil.rmtree(cache_dir, ignore_errors=True)
                console.print("[green]Cache limpo com sucesso![/green]")
            except Exception as e:
                console.print(f"[red]Erro ao limpar cache: {e}[/red]")
    
    # Suprimir warnings durante a coleta para não poluir a saída
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
        ) as progress:
            t1 = progress.add_task("[bold blue]Coletando commits", total=None)
            try:
                commits = collect_commits(repo_url, max_commits, skip_errors=True)
                progress.update(t1, completed=1)
            except Exception as e:
                progress.update(t1, completed=1)
                console.print(f"[bold red]Erro ao coletar commits:[/bold red] {str(e)}")
                console.print("[yellow]Dica: Tente usar --clear-cache para limpar o cache corrompido[/yellow]")
                raise
    ca = CommitAnalyzer()
    if commits:
        counts = {}
        for c in commits:
            a = c.get("author")
            counts[a] = counts.get(a, 0) + 1
        commits = [c for c in commits if counts.get(c.get("author", 0), 0) > min_commits]
    analyzed = []
    if commits:
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
        ) as progress:
            t2 = progress.add_task("[bold green]Analisando commits", total=len(commits))
            for c in commits:
                res = ca.analyze_commit(c)
                analyzed.append(res)
                progress.advance(t2)
    report = aggregate(analyzed)
    with open("analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)
    console.print("[bold white]Arquivo salvo: [bold yellow]analysis_report.json")
    _show_table(report)

@app.command()
def view(
    path: str = Option("analysis_report.json", "--path"),
    sort_by: str = Option("final_score", "--sort-by"),
    top: int = Option(10, "--top"),
):
    with open(path) as f:
        report = json.load(f)
    _show_table(report, sort_by, top)

@app.command()
def top(
    path: str = Option("analysis_report.json", "--path"),
    top: int = Option(20, "--top"),
    detailed: bool = Option(True, "--detailed/--no-detailed"),
):
    with open(path) as f:
        report = json.load(f)
    if detailed:
        _show_top_commits_full(report, top)
    else:
        _show_top_commits(report, top)

if __name__ == "__main__":
    app()
