from dotenv import load_dotenv
load_dotenv()

from typing import List, Dict

from app.sample_assets.papers import sample_text_chunks
from app.golems.models.concept import Concept

from app.golems.parsers.concept import get_concept_name_list, get_concept

def update_concepts_list(concepts: Dict[str, str], new_chunk: str, chunk_buffer: List[str]) -> List[Concept]:

    
    concept_name_list = get_concept_name_list(new_chunk)

    for name in concept_name_list.concepts:

        current_summary = concepts.get(name, '')

        concept = get_concept(new_chunk, chunk_buffer, Concept(name=name, summary=current_summary))

        concepts[name] = concept


    return concepts

if __name__ == '__main__':

    sample_text_chunks

    concepts = {}

    chunk_buffer = []

    for chunk in sample_text_chunks:
        chunk_buffer.append(chunk)

        if len(chunk_buffer) > 5:
            chunk_buffer.pop(0)

        concepts = update_concepts_list(concepts, chunk, chunk_buffer)

        print(chunk)
        print(concepts)