# installing required libraries
!pip install pydub
!pip install git+https://github.com/openai/whisper.git
!sudo apt update && sudo apt install ffmpeg
!pip install networkx matplotlib
!pip install openai
!pip install requests

# connecting google drive to import video samples ---------------------------------------

from google.colab import drive
import os
drive.mount('/content/drive')

video_files = '/content/drive/My Drive/video_files'
audio_files = '/content/drive/My Drive/audio_files'
text_files = '/content/drive/My Drive/text_files'

folders = [video_files, audio_files, text_files]
for folder in folders:
    # Check if the output folder exists
    if not os.path.exists(folder):
    # If not, create the folder
        os.makedirs(folder)


# Extracting audio from video ------------------------------------------------------------

from pydub import AudioSegment
# Extract audio from videos
for video_file in os.listdir(video_files):
    if video_file.endswith('.mp4'):
        video_path = os.path.join(video_files, video_file)
        audio = AudioSegment.from_file(video_path, format="mp4")

        # Save audio as WAV
        audio.export(os.path.join(audio_files, f"{video_file[:-4]}.wav"), format="wav")


# Transcribing audio to text -------------------------------------------------------------

import re
import subprocess
# function to transcribe and save the output in txt file
def transcribe_and_save(audio_files, text_files, model='medium.en'):
    # Construct the Whisper command
    whisper_command = f"whisper '{audio_files}' --model {model}"
    # Run the Whisper command
    transcription = subprocess.check_output(whisper_command, shell=True, text=True)

    # Clean and join the sentences
    output_without_time = re.sub(r'\[\d+:\d+\.\d+ --> \d+:\d+\.\d+\]  ', '', transcription)
    sentences = [line.strip() for line in output_without_time.split('\n') if line.strip()]
    joined_text = ' '.join(sentences)

    # Create the corresponding text file name
    audio_file_name = os.path.basename(audio_files)
    text_file_name = os.path.splitext(audio_file_name)[0] + '.txt'
    file_path = os.path.join(text_files, text_file_name)

    # Save the output as a txt file
    with open(file_path, 'w') as file:
        file.write(joined_text)

    print(f'Text for {audio_file_name} has been saved to: {file_path}')

# Transcribing all the audio files in the directory
for audio_file in os.listdir(audio_files):
    if audio_file.endswith('.wav'):
        audio_files = os.path.join(audio_files, audio_file)
        transcribe_and_save(audio_files, text_files)


# Building the knowledge graph ------------------------------------------------------------

import requests
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Global Constants API endpoint, API key, prompt text
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
api_key = "your_openai_api_key_goes_here"
prompt_text = """Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.
If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2]. The relationship is directed, so the order matters.
Example:
prompt: Sun is the source of solar energy. It is also the source of Vitamin D.
updates:
[["Sun", "source of", "solar energy"],["Sun","source of", "Vitamin D"]]
prompt: $prompt
updates:"""

# Graph Creation Function

def create_graph(df, rel_labels):
    G = nx.from_pandas_edgelist(df, "source", "target",
                              edge_attr=True, create_using=nx.MultiDiGraph())
    plt.figure(figsize=(12, 12))

    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=rel_labels,
        font_color='red'
    )
    plt.show()

# Data Preparation Function

def preparing_data_for_graph(api_response):
    #extract response text
    response_text = api_response.text
    entity_relation_lst = json.loads(json.loads(response_text)["choices"][0]["text"])
    entity_relation_lst = [x for x in entity_relation_lst if len(x) == 3]
    source = [i[0] for i in entity_relation_lst]
    target = [i[2] for i in entity_relation_lst]
    relations = [i[1] for i in entity_relation_lst]

    kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
    relation_labels = dict(zip(zip(kg_df.source, kg_df.target), kg_df.edge))
    return kg_df,relation_labels

# OpenAI API Call Function
def call_gpt_api(api_key, prompt_text):
    global API_ENDPOINT
    try:
        data = {
            "model": "gpt-3.5-turbo",
            "prompt": prompt_text,
            "max_tokens": 3000,
            "stop": "\n",
            "temperature": 0
        }
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
        r = requests.post(url=API_ENDPOINT, headers=headers, json=data)
        response_data = r.json()  # Parse the response as JSON
        print("Response content:", response_data)
        return response_data
    except Exception as e:
        print("Error:", e)

  # Main function

def main(text_file_path, api_key):

    with open(file_path, 'r') as file:
        kb_text = file.read()

    global prompt_text
    prompt_text = prompt_text.replace("$prompt", kb_text)

    api_response = call_gpt_api(api_key, prompt_text)
    df, rel_labels = preparing_data_for_graph(api_response)
    create_graph(df, rel_labels)code

# Start Function

def start():
    for filename in os.listdir(text_files):
        if filename.endswith(".txt"):
        # Construct the full path to the text file
            text_file_path = os.path.join(text_files, filename)
    main(text_file_path, api_key)
