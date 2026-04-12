import logging

from use_cases import run_pipeline

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

if __name__ == "__main__":
    run_pipeline.execute()