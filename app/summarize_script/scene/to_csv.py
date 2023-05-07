import pandas as pd
import json
import io


def create_final_scenes_dataframe(data):
    # Extract the list of scenes and characters from the JSON data
    scenes_data = data["scenes"]
    characters = sorted(set([char for scene_data in scenes_data for char in scene_data["scene"]["characters"]]))
    scenes = [scene_data["scene"]["summary"] for scene_data in scenes_data]

    # Initialize an empty DataFrame with characters as index and scene summaries as columns
    final_scenes_df = pd.DataFrame(index=characters, columns=scenes)

    # Fill the DataFrame with 'X' if a character is present in the scene, and empty otherwise
    for i, scene_data in enumerate(scenes_data):
        for character in characters:
            final_scenes_df.at[character, scenes[i]] = 'X' if character in scene_data["scene"]["characters"] else ''

    return final_scenes_df

import pandas as pd
import io

def csv_from_scenes_dict(data):
    # Extract the list of scenes, characters, and pages from the JSON data
    scenes_data = data["scenes"]
    characters = sorted(set([char for scene_data in scenes_data for char in scene_data["scene"]["characters"]]))
    scenes = [scene_data["scene"]["summary"] for scene_data in scenes_data]
    pages = ['/'.join(map(str, scene_data["pages"])) for scene_data in scenes_data]

    # Initialize an empty DataFrame with characters as index and scene summaries as columns
    characters_df = pd.DataFrame(index=characters, columns=scenes)
    characters_df.index.name = 'Characters'

    # Fill the DataFrame with 'X' if a character is present in the scene, and empty otherwise
    for i, scene_data in enumerate(scenes_data):
        for character in characters:
            characters_df.at[character, scenes[i]] = 'X' if character in scene_data["scene"]["characters"] else ''

    # Create a DataFrame with pages as index and scene summaries as columns
    pages_df = pd.DataFrame([pages], index=['Pages'], columns=scenes)

    # Concatenate the pages DataFrame and the characters DataFrame vertically
    final_scenes_df = pd.concat([pages_df, characters_df])

    print(final_scenes_df)
    data = io.BytesIO(final_scenes_df.to_csv(index=True).encode('utf-8'))

    return data


    

if __name__ == '__main__':

        # Load JSON data

    with open('result.txt') as f:
        data = json.load(f)
    # Create the DataFrame
    final_scenes_df = csv_from_scenes_dict(data)

    with open('test.csv','wb') as f:
        f.write(final_scenes_df.getbuffer())
