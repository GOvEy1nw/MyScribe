import torch
from faster_whisper import WhisperModel
import logging

# Force unbuffered output
import sys
import os

sys.stdout.reconfigure(line_buffering=True)
os.environ['PYTHONUNBUFFERED'] = '1'

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = WhisperModel("large-v3", device=device)

async def process_audio(file_path):
    yield f"Transcribing audio..."
    segments, info = model.transcribe(file_path, beam_size=5, vad_filter=True)

    transcript = ""
    subtitles = []

    for segment in segments:
        transcript += segment.text + " "
        subtitles.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    # Yield the final result
    yield transcript.strip(), subtitles
    print(transcript.strip())
    print(subtitles)