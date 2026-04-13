import config
from domain.etl import ETLPipeline
from infrastructure.extractor import TarGzExtractor


def execute() -> None:
    pipeline = ETLPipeline(
        extractor=TarGzExtractor(
            archive=config.ARCHIVE_PATH,
            destination=config.EXTRACTION_DESTINATION,
        ),
        transformer=None,
        loader=None
    )
    pipeline.run()
