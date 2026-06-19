"""
OpusMagnum · 巨作 / GreatWork — GitHub API 客户端
封装 PyGithub，读取各项目仓库的 Issues、提交记录、状态。
"""

from typing import Optional
from github import Github, Repository
from config.settings import settings


class GitHubClient:
    """轻量 GitHub API 客户端。"""

    def __init__(self):
        token = settings.github_token
        self.gh = Github(token) if token else None

    def _get_repo(self, repo_full_name: str) -> Optional[Repository.Repository]:
        if not self.gh:
            return None
        try:
            return self.gh.get_repo(repo_full_name)
        except Exception:
            return None

    def list_issues(self, repo_full_name: str, state: str = "open") -> list:
        """
        读取仓库 Issues。
        返回格式符合 task.schema.json（简化版）。
        """
        repo = self._get_repo(repo_full_name)
        if not repo:
            return []
        issues = repo.get_issues(state=state)
        return [
            {
                "task_id": str(issue.number),
                "title": issue.title,
                "status": "done" if issue.state == "closed" else "todo",
                "project": repo_full_name.split("/")[-1],
                "labels": [label.name for label in issue.labels],
                "github_issue_url": issue.html_url,
                "created_at": issue.created_at.isoformat() if issue.created_at else "",
                "updated_at": issue.updated_at.isoformat() if issue.updated_at else "",
            }
            for issue in issues[:50]  # 最多取 50 条
        ]

    def list_all_issues(self, state: str = "open") -> dict:
        """读取所有子项目仓库的 Issues，按项目分组。"""
        repos = {
            "athanor": settings.citrinitas_repo,
            "alembic": settings.nigredo_repo,
            "crucible": settings.albedo_repo,
            "opus-magnum": settings.opus_repo,
        }
        result = {}
        for key, repo_name in repos.items():
            result[key] = self.list_issues(repo_name, state=state)
        return result

    def get_repo_summary(self, repo_full_name: str) -> dict:
        """
        获取仓库摘要：Issue 数量、最新提交、Stars。
        """
        repo = self._get_repo(repo_full_name)
        if not repo:
            return {"error": "repo_not_found_or_token_missing"}
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "open_issues": repo.open_issues_count,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "default_branch": repo.default_branch,
            "last_commit": (
                repo.get_commits()[0].commit.sha[:7]
                if repo.get_commits().totalCount > 0
                else "none"
            ),
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else "",
        }
