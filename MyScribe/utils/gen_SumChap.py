from ollama import AsyncClient
import json

async def generate_chapters(transcript, num_chapters):
    try:
        client = AsyncClient()
        response = await client.chat(
            model='llama3:8b',
            format="json",
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that generates chapters for a video transcript. Only reply with the starting timecode and descriptive title for each chapter in this JSON format {"HH:MM:SS": "title1", "HH:MM:SS": "title2", "HH:MM:SS": "title3"}',
                },
                {
                    'role': 'user',
                    'content': f'Please provide a list of chapter titles and starting timecodes for the following transcript:\n\n{transcript}',
                }
            ]
        )
        json_data = response['message']['content']
        data = json.loads(json_data)
        formatted_list = [f"[{key}] {value}" for key, value in data.items()]
        # Join the formatted strings with "\n\n"
        chapters = "\n".join(formatted_list)
        return chapters
    except Exception as e:
        print(f"Error generating chapters: {str(e)}")
        return "Error generating chapters. Please try again."

async def generate_summary(transcript):
    try:
        client = AsyncClient()
        response = await client.chat(
            model='llama3:8b',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that summarizes transcripts. Only reply with the summary. Do not mention the transcript in your response.',
                },
                {
                    'role': 'user',
                    'content': f'Please summarize the following transcript in a concise manner:\n\n{transcript}',
                }
            ]
        )
        summary = response['message']['content']
        return summary
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "Error generating summary. Please try again."