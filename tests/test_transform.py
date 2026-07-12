from datetime import date

import pytest

from transform import transform_repository


def sample_repository():
    return {
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


def test_transform_repository_keeps_required_fields():
    transformed = transform_repository(sample_repository(), snapshot_date=date(2026, 7, 12))

    assert transformed["repo_id"] == 123
    assert transformed["owner"] == "octocat"
    assert transformed["repository_name"] == "example"
    assert transformed["language"] == "Python"
    assert transformed["updated_at"].year == 2024
    assert transformed["stars"] == 10
    assert transformed["forks"] == 3
    assert transformed["watchers"] == 8
    assert transformed["open_issues"] == 1
    assert transformed["snapshot_date"] == date(2026, 7, 12)


def test_transform_repository_rejects_missing_required_field():
    repository = sample_repository()
    del repository["id"]

    with pytest.raises(ValueError):
        transform_repository(repository)
