from pydantic import BaseModel

from typing import List

import json

class Scene(BaseModel):

    characters: List[str]
    summary: str

class SceneBuffer(BaseModel):

    scenes : List[Scene]

    def to_json(self) -> str:
        return json.dumps(self.dict(), indent=2)
    
class SceneAndPageNumber(BaseModel):

    scene: Scene
    pages: List[int]

class FinalScenes(BaseModel):

    scenes: List[SceneAndPageNumber]

    def to_json(self) -> str:
        return json.dumps(self.dict(), indent=2)