from pydantic import BaseModel

from typing import List

class KnowledgeElements(BaseModel):
    elements: List[str]