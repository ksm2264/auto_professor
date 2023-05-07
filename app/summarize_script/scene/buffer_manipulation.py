from typing import List

from app.summarize_script.models import SceneBuffer, SceneAndPageNumber

def merge_buffers(buffers: List[SceneBuffer]) -> SceneBuffer:
    merged_scenes = []
    for i, buffer in enumerate(buffers):
        if i == 0:
            merged_scenes.extend(buffer.scenes)
        else:
            if merged_scenes[-1].characters == buffer.scenes[0].characters:
                merged_scenes.extend(buffer.scenes[1:])
            else:
                merged_scenes.extend(buffer.scenes)
    return SceneBuffer(scenes=merged_scenes)

def merge_scenes(scene_and_page_numbers: List[SceneAndPageNumber]) -> List[SceneAndPageNumber]:
    merged_scenes = []

    for labeled_scene in scene_and_page_numbers:
        if not merged_scenes or merged_scenes[-1].scene.characters != labeled_scene.scene.characters:
            merged_scenes.append(labeled_scene)
        else:
            merged_scenes[-1].pages += labeled_scene.pages

    return merged_scenes