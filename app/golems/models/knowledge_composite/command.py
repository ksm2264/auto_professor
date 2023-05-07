from pydantic import BaseModel
from typing import List

class UpsertKnowledgeCommand(BaseModel):
    path = List[str]
    content = str