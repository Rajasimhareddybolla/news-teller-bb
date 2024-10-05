import os
import shutil
import json
from datetime import datetime

# Function to delete all files and folders in a directory
def clean_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Function to update the history.json file
def update_history_file(directory):
    chats_history = {"history": []}
    with open(os.path.join(directory, 'history.json'), 'w') as f:
        json.dump(chats_history, f)

# Check if a new day has started
def is_new_day():
    last_run_file = 'last_run_date.txt'
    today = datetime.now().date()

    if os.path.exists(last_run_file):
        with open(last_run_file, 'r') as f:
            last_run_date = f.read().strip()
            if last_run_date == str(today):
                return False

    with open(last_run_file, 'w') as f:
        f.write(str(today))

    return True

if is_new_day():
    # Clean the 'chats' directory
    chats_directory = 'chats'
    clean_directory(chats_directory)
    update_history_file(chats_directory)

    # Clean the 'summarized/audio' directory
    audio_directory = 'summarized/audio'
    clean_directory(audio_directory)

    # Define the directory to clean
    directory = 'chats'

    # Delete all files and folders in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # Replace history.json with chats_history
    chats_history = {"history": []}
    with open(os.path.join(directory, 'history.json'), 'w') as f:
        json.dump(chats_history, f)
        
    directory = "summarized/audio"
    # Delete all files and folders in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # Replace history.json with chats_history
    chats_history = {"history": []}
    with open(os.path.join(directory, 'history.json'), 'w') as f:
        json.dump(chats_history, f)
        
        

    directory = "summarized/text"
    # Delete all files and folders in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    directory = "db"
    # Delete all files and folders in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

