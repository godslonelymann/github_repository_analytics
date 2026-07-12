import sys
import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

spec = importlib.util.spec_from_file_location("github_analytics_run_pipeline", SRC_DIR / "run_pipeline.py")
pipeline_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_module)
run_pipeline = pipeline_module.run_pipeline


if __name__ == "__main__":
    run_pipeline()
