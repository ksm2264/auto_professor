import pandas as pd
import io

from app.summarize_script.scene.summarize import scenes_from_pdf
from app.summarize_script.scene.to_csv import csv_from_scenes_dict

def test_csv():

    # assign data of lists.  
    data = {'Name': ['Tom', 'Joseph', 'Krish', 'John'], 'Age': [20, 21, 19, 18]}  
    
    # Create DataFrame  
    df = pd.DataFrame(data)  
    
    data = io.BytesIO(df.to_csv(index=False).encode('utf-8'))

    return data


async def csv_data_from_pdf_bytes(pdf_bytes, thread):

    scenes = await scenes_from_pdf(pdf_bytes, thread)

    csv_bytes = csv_from_scenes_dict(scenes.dict())

    return csv_bytes
