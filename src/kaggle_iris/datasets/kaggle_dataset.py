from typing import Any, NotRequired, TypedDict, Unpack
import os
import kagglehub  # type: ignore
from kedro.io import AbstractDataset


class KaggleDatasetParams(TypedDict):
    """
    Referenced directly from dataset_load() args

    See: [dataset_load()](https://github.com/Kaggle/kagglehub/blob/4fe0a176e0e9b815ca4101c371b504ff97239b97/src/kagglehub/datasets.py#L98)
    """

    adapter: str
    handle: str
    kaggle_path: str
    pandas_kwargs: NotRequired[Any]
    sql_query: NotRequired[str | None]
    hf_kwargs: NotRequired[Any]
    credentials: dict[str, Any]


class KaggleDataset(AbstractDataset[Any, Any]):
    def __init__(self, **params: Unpack[KaggleDatasetParams]) -> None:
        self._params = params

    @property
    def adapter(self) -> kagglehub.KaggleDatasetAdapter:
        return kagglehub.KaggleDatasetAdapter(self._params.get("adapter"))

    @property
    def handle(self) -> str:
        return self._params.get("handle")

    @property
    def kaggle_path(self) -> str:
        return self._params.get("kaggle_path")

    @property
    def pandas_kwargs(self) -> Any:
        return self._params.get("pandas_kwargs")

    @property
    def sql_query(self) -> str | None:
        return self._params.get("sql_query")

    @property
    def hf_kwargs(self) -> Any:
        return self._params.get("hf_kwargs")

    @property
    def credentials(self) -> dict[str, Any]:
        return self._params.get("credentials")

    def load(self) -> Any:
        if "KAGGLE_API_TOKEN" in self.credentials:
            os.environ["KAGGLE_API_TOKEN"] = self.credentials.get(
                "KAGGLE_API_TOKEN", ""
            )

        return kagglehub.load_dataset(
            adapter=self.adapter,
            handle=self.handle,
            path=self.kaggle_path,
            pandas_kwargs=self.pandas_kwargs,
            sql_query=self.sql_query,
            hf_kwargs=self.hf_kwargs,
        )

    def _describe(self) -> dict[str, Any]:
        return dict()

    def save(self, data: Any) -> None:
        self._logger.debug(
            "Kaggle dataset upload not implemented, skipping 'save' Dataset functionality"
        )
