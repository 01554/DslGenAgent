from pydantic import BaseModel
from src.structure.edge import Edge


class WorkflowPlan(BaseModel):
    edges: list[Edge]

