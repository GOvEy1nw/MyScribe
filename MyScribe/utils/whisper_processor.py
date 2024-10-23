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

async def process_audio(file_path, min_chars_per_line=100):
    transcribing_message = "Processing audio..."
    yield transcribing_message
    segments_generator, info = model.transcribe(file_path, beam_size=5, vad_filter=True, language="en")
    segments = list(segments_generator)  # Convert generator to list

    transcript = []
    subtitles = []
    current_line = ""
    line_start = 0

    def format_time(seconds):
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    for i, segment in enumerate(segments):
        # Add subtitle entry
        start_time = format_time(segment.start)
        end_time = format_time(segment.end)
        subtitles.append(f"{i+1}\n{start_time} --> {end_time}\n{segment.text.strip()}\n\n")

        # Build transcript
        current_line += segment.text + " "
        if len(current_line) >= min_chars_per_line:
            transcript.append(f"[{format_time(line_start)} --> {format_time(segment.end)}]\n{current_line.strip()}\n\n")
            current_line = ""
            line_start = segment.end
    # Add any remaining text to transcript
    if current_line:
        transcript.append(f"[{format_time(line_start)} --> {format_time(segments[-1].end)}]\n{current_line.strip()}\n\n")

    # Join transcript lines and yield results
    full_transcript = "".join(transcript).strip()
    subtitles = "".join(subtitles).strip()
    yield full_transcript, subtitles
    print(full_transcript)
