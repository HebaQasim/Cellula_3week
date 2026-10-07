"""Part 1 (step B): download the README of every public GitHub repository and save it in data/github."""
from pathlib import Path

import requests

GITHUB_USERNAME = "HebaQasim"

BASE_DIR = Path(__file__).parent
GITHUB_DIR = BASE_DIR / "data" / "github"


def get_repositories(username):
    """Return the list of public repositories of a GitHub user."""
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, params={"per_page": 100}, timeout=30)
    response.raise_for_status()
    return response.json()


def get_readme(username, repo_name):
    """Return the README text of a repository, or an empty text if it has no README."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    response = requests.get(url, headers={"Accept": "application/vnd.github.raw+json"}, timeout=30)
    if response.status_code == 404:
        return ""
    response.raise_for_status()
    return response.text


def save_github_documents():
    """Save one .md file per repository: a short header (name, link, description, language) + the README."""
    GITHUB_DIR.mkdir(parents=True, exist_ok=True)
    repositories = get_repositories(GITHUB_USERNAME)

    for repo in repositories:
        readme = get_readme(GITHUB_USERNAME, repo["name"])
        text = (
            f"GitHub repository: {repo['name']}\n"
            f"Link: {repo['html_url']}\n"
            f"Description: {repo['description'] or 'No description'}\n"
            f"Main language: {repo['language'] or 'Not specified'}\n\n"
            f"{readme}"
        )
        (GITHUB_DIR / f"{repo['name']}.md").write_text(text, encoding="utf-8")
        print(f"Saved {repo['name']}.md  ({len(readme)} characters of README)")


if __name__ == "__main__":
    save_github_documents()
