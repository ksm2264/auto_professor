from dotenv import load_dotenv
load_dotenv()

import tempfile

from langchain.document_loaders import PyPDFLoader

from app.summarize_script.scene.parser import get_scene_buffer
from app.summarize_script.scene.buffer_manipulation import merge_scenes

from app.summarize_script.models import SceneAndPageNumber, FinalScenes

def create_temporary_file(pdf_content):
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    # Write the PDF content to the temporary file
    temp_file.write(pdf_content)
    temp_file.close()
    
    return temp_file.name

async def scenes_from_pdf(pdf_file_content, thread):
    temp_file_path = create_temporary_file(pdf_file_content)

    loader = PyPDFLoader(temp_file_path)
    pages = loader.load_and_split()

    current_scene = []

    all_scenes = []

    for idx, page in enumerate(pages):
        await thread.send(f'processing page {idx} of {len(pages)}')
        print(page.page_content)
        buffer = get_scene_buffer(
                text_chunk = page.page_content,
                current_scene = current_scene
            )
        if len(buffer.scenes)>0:
            current_scene = buffer.scenes[-1].characters

            for scene in buffer.scenes:
                scene_with_page = SceneAndPageNumber(scene=scene, pages=[page.metadata['page']+1])
                all_scenes.append(scene_with_page)
                print(scene_with_page)
    
    final_scenes = merge_scenes(all_scenes)

    final = FinalScenes(scenes = final_scenes)

    return final


if __name__ == '__main__':

    with open('ithaca.pdf', 'rb') as f:
        final = scenes_from_pdf(f.read())

    with open('result.txt', 'w') as f:
        f.write(final.to_json())