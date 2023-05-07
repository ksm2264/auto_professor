from pydantic import BaseModel
from typing import List

class Concept(BaseModel):
    name: str
    summary: str
    
class ConceptNameList(BaseModel):
    concepts: List[str]

class ConceptList(BaseModel):
    concepts: List[Concept]
