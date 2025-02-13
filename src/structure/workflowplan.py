from pydantic import BaseModel


class WorkflowPlan(BaseModel):
    workflow_plan: str

