CREATE TABLE IF NOT EXISTS repositories (
    repo_id BIGINT PRIMARY KEY,
    owner VARCHAR(255) NOT NULL,
    repository_name VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS repository_metrics (
    repo_id BIGINT NOT NULL REFERENCES repositories(repo_id),
    snapshot_date DATE NOT NULL,
    stars INTEGER NOT NULL,
    forks INTEGER NOT NULL,
    watchers INTEGER NOT NULL,
    open_issues INTEGER NOT NULL
);

ALTER TABLE repositories
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP;

UPDATE repositories
SET updated_at = created_at
WHERE updated_at IS NULL;

ALTER TABLE repositories
ALTER COLUMN updated_at SET NOT NULL;
