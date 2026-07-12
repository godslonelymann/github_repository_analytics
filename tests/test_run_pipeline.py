from datetime import date

import run_pipeline as pipeline


def test_run_pipeline_extracts_transforms_and_loads(monkeypatch):
    raw_repository = {
        "id": 123,
        "name": "example",
        "owner": {"login": "octocat"},
        "description": "Example repository",
        "language": "Python",
        "stargazers_count": 10,
        "forks_count": 3,
        "watchers_count": 8,
        "open_issues_count": 1,
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }
    loaded_rows = []

    monkeypatch.setattr(pipeline, "extract_repositories", lambda repositories: [raw_repository])
    monkeypatch.setattr(
        pipeline,
        "transform_repositories",
        lambda repositories: [
            {
                "repo_id": repositories[0]["id"],
                "owner": repositories[0]["owner"]["login"],
                "repository_name": repositories[0]["name"],
                "description": repositories[0]["description"],
                "language": repositories[0]["language"],
                "created_at": repositories[0]["created_at"],
                "updated_at": repositories[0]["updated_at"],
                "snapshot_date": date(2026, 7, 12),
                "stars": repositories[0]["stargazers_count"],
                "forks": repositories[0]["forks_count"],
                "watchers": repositories[0]["watchers_count"],
                "open_issues": repositories[0]["open_issues_count"],
            }
        ],
    )
    monkeypatch.setattr(pipeline, "load_repositories", lambda repositories: loaded_rows.extend(repositories))

    result = pipeline.run_pipeline(["octocat/example"])

    assert result == loaded_rows
    assert loaded_rows[0]["repo_id"] == 123
