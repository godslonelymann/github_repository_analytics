from datetime import date, datetime

from load import load_repositories


class FakeConnection:
    def __init__(self):
        self.executed = []

    def execute(self, statement, parameters):
        self.executed.append((statement, parameters))


class FakeTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc, traceback):
        return False


class FakeEngine:
    def __init__(self):
        self.connection = FakeConnection()

    def begin(self):
        return FakeTransaction(self.connection)


def test_load_repositories_inserts_repository_and_metrics():
    engine = FakeEngine()
    repository = {
        "repo_id": 123,
        "owner": "octocat",
        "repository_name": "example",
        "description": "Example repository",
        "language": "Python",
        "created_at": datetime(2020, 1, 1),
        "updated_at": datetime(2024, 1, 1),
        "snapshot_date": date(2026, 7, 12),
        "stars": 10,
        "forks": 3,
        "watchers": 8,
        "open_issues": 1,
    }

    load_repositories([repository], engine=engine)

    assert len(engine.connection.executed) == 2
    assert engine.connection.executed[0][1] == repository
    assert engine.connection.executed[1][1] == repository
