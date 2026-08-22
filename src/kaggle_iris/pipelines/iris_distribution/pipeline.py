"""
This is a boilerplate pipeline 'iris_distribution'
generated using Kedro 1.5.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import get_iris_distribution


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=get_iris_distribution,
                inputs="iris",
                outputs="iris_distribution",
                name="iris_distribution",
            )
        ]
    )
