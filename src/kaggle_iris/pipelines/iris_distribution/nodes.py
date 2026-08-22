import polars as pl


def get_iris_distribution(lf_iris: pl.LazyFrame) -> pl.DataFrame:
    return lf_iris.sql(
        "SELECT Species as species, Count(Species) as species_count FROM self GROUP BY Species"
    ).collect()
