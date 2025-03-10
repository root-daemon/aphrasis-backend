import requests
import tempfile

def download_audio_file(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status() 

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(response.content)
        return temp_file.name

