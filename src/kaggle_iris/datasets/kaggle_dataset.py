import os
from typing import Any, NotRequired, TypedDict, Unpack

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
    """``kaggle_dataset.KaggleDataset`` loads Kaggle Datasets via kagglehub library using kagglehub.dataset_load(...). Requires environment 'KAGGLE_API_KEY' to access Kaggle API

    Examples:

        Loading the [Iris Dataset](https://www.kaggle.com/datasets/uciml/iris)

        *conf/base/catalog.yml*
        ```yaml
        iris:
        type: kaggle_iris.datasets.kaggle_dataset.KaggleDataset
        adapter: polars
        handle: "uciml/iris"
        kaggle_path: "Iris.csv"
        credentials: kaggle_creds
        ```

        *conf/base/local/credentials.yml*
        ```yaml
        kaggle_creds:
        KAGGLE_API_TOKEN: KGAT_xxxx
        ```

        Using it as a Kedro Node function
        ```python
        def get_iris_distribution(lf_iris: pl.LazyFrame) -> pl.DataFrame:
            return lf_iris.sql(
                "SELECT Species as species, Count(Species) as species_count FROM self GROUP BY Species"
            ).collect()
        ```
    """

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
        return {
            "adapter": self.adapter,
            "handle": self.handle,
            "kaggle_path": self.kaggle_path,
            "pandas_kwargs": self.pandas_kwargs,
            "sql_query": self.sql_query,
            "hf_kwargs": self.hf_kwargs,
        }

    def save(self, data: Any) -> None:
        self._logger.debug(
            "Kaggle dataset upload not implemented, skipping 'save' Dataset functionality"
        )
