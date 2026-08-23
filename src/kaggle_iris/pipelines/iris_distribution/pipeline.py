"""
This is a boilerplate pipeline 'iris_distribution'
generated using Kedro 1.5.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import get_iris_distribution, normalize_iris_dataset, noop


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=get_iris_distribution,
                inputs="iris",
                outputs="iris_distribution",
                name="iris_distribution",
            ),
            Node(
                func=normalize_iris_dataset,
                inputs="iris",
                outputs="iris_normalized",
                name="iris_normalized",
            ),
            Node(
                func=noop,
                inputs="iris_normalized",
                outputs="iris_normalized_upload",
                name="iris_normalized_upload",
            ),
        ]
    )
