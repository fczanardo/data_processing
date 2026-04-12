import config
from domain.etl import ETLPipeline
from infrastructure.extractor import TarGzExtractor
from infrastructure.transformer import QuarterlyDataTransformer
from infrastructure.loader import DataLoader


def execute() -> None:
    pipeline = ETLPipeline(
        extractor=TarGzExtractor(
            archive=config.ARCHIVE_PATH,
            destination=config.EXTRACTION_DESTINATION,
        ),
        transformer=QuarterlyDataTransformer(),
        loader=DataLoader(),
    )
    pipeline.run()
