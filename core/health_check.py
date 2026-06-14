"""
OpusMagnum · 巨作 / GreatWork — 服务健康检测
定期 ping 各项目端口，判断在线/离线。
"""

import requests
from typing import Optional
from config.settings import settings, ProjectConfig


def check_health(project: ProjectConfig, timeout: float = 2.0) -> dict:
    """
    检测单个项目健康状态。
    调用各项目的 GET /health 端点。
    返回：{"online": bool, "status": str, "version": str, "latency_ms": float}
    """
    url = project.endpoint("/health")
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "online": True,
                "status": data.get("status", "ok"),
                "project": data.get("project", project.name),
                "version": data.get("version", "unknown"),
                "latency_ms": round(resp.elapsed.total_seconds() * 1000, 1),
            }
        else:
            return {"online": False, "status": f"http_{resp.status_code}", "project": project.name}
    except requests.exceptions.ConnectionError:
        return {"online": False, "status": "offline", "project": project.name}
    except requests.exceptions.Timeout:
        return {"online": False, "status": "timeout", "project": project.name}
    except Exception as e:
        return {"online": False, "status": f"error: {e}", "project": project.name}


def check_all() -> list:
    """检测所有子项目健康状态。"""
    results = []
    for project in settings.all_projects:
        results.append(check_health(project))
    return results


def format_health_badge(health: dict) -> str:
    """返回 Streamlit 可用的状态徽章文本。"""
    if health["online"]:
        return f"✅ **{health['project']}** — 在线（{health['latency_ms']}ms）"
    else:
        return f"❌ **{health['project']}** — {health['status']}"
