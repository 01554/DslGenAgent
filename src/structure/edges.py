from pydantic import BaseModel
from src.structure.edge import Edge


class Edges(BaseModel):
    edges: list[Edge]

