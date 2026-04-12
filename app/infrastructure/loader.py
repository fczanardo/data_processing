from typing import Any

from domain.etl import Loader


class DataLoader(Loader):
    def load(self, data: Any) -> None:
        pass
