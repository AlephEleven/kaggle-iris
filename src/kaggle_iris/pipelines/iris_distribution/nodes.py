from typing import Any

import polars as pl


def get_iris_distribution(lf_iris: pl.LazyFrame) -> pl.DataFrame:
    return lf_iris.sql(
        "SELECT Species as species, Count(Species) as species_count FROM self GROUP BY Species"
    ).collect()


def normalize_iris_dataset(lf_iris: pl.LazyFrame) -> pl.DataFrame:
    c = pl.col("SepalLengthCm", "SepalWidthCm", "PetalWidthCm")
    return lf_iris.with_columns(c / c.sum()).collect()


def noop(_: Any):
    return ""
