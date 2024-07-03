import reflex as rx
from ..utils.whisper_processor import process_audio
import json
from ollama import AsyncClient

class uploadState(rx.State):
    file: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s)."""
        if files:
            self.file = files[0].filename

    def clear_file(self):
        """Clear the uploaded file."""
        self.file = ""

class llm_selected(rx.State):
    llmOptions: list[str] = [
        "Ollama",
        "OpenAI",
        "Claude",
        "Gemini"
    ]
    llm: str = ""
    api_key: str = ""

    def save_api_key(self):
        self.llm = self.llm
        if self.llm == "OpenAI":
            self.OpenAI_api = self.api_key
            self.api_key = ""
        elif self.llm == "Ollama":
            self.Ollama_api = self.api_key
            self.api_key = ""
        elif self.llm == "Claude":
            self.Claude_api = self.api_key
            self.api_key = ""
        elif self.llm == "Gemini":
            self.Gemini_api = self.api_key
            self.api_key = ""

    OpenAI_api: str = rx.LocalStorage("", name="OpenAI")
    Ollama_api: str = rx.LocalStorage("", name="Ollama")
    Claude_api: str = rx.LocalStorage("", name="Claude")
    Gemini_api: str = rx.LocalStorage("", name="Gemini")

    def delete_api_key(self):
        self.llm = self.llm
        if self.llm == "OpenAI":
            return rx.remove_local_storage("OpenAI")
        elif self.llm == "Ollama":
            return rx.remove_local_storage("Ollama")
        elif self.llm == "Claude":
            return rx.remove_local_storage("Claude")
        elif self.llm == "Gemini":
            return rx.remove_local_storage("Gemini")

class ClickState(uploadState):
    variants: dict[str, str] = {
        "Transcript": "outline",
        "Subtitles": "outline",
        "Chapters": "outline",
        "Summary": "outline"
    }
    processing: dict[str, bool] = {
        "Transcript": False,
        "Subtitles": False,
        "Chapters": False,
        "Summary": False
    }
    disable: dict[str, bool] = {
        "Transcript": False,
        "Subtitles": False,
        "Chapters": False,
        "Summary": False
    }
    complete: dict[str, bool] = {
        "Transcript": False,
        "Subtitles": False,
        "Chapters": False,
        "Summary": False
    }

    num_chapters: int = 5
    transcript: str = rx.LocalStorage("", name="transcript")
    subtitles: str = rx.LocalStorage("", name="subtitles")
    chapters: str = rx.LocalStorage("", name="chapters")
    summary: str = rx.LocalStorage("", name="summary")

    def change_variant(self, button: str):
        self.variants[button] = "solid" if self.variants[button] == "outline" else "outline"

    async def generate(self):
        yield
        for option, variant in self.variants.items():
            if variant == "solid":
                if option == "Transcript":
                    self.processing[option] = True
                    yield
                elif option == "Subtitles":
                    self.processing[option] = True
                    yield
                elif option == "Chapters":
                    self.processing[option] = True
                    yield
                elif option == "Summary":
                    self.processing[option] = True
                    yield
            else:
                self.disable[option] = True
                yield

        file_path = "./uploaded_files/" + self.file
        async for progress in process_audio(file_path):
            if isinstance(progress, str):
                print(progress)
            else:
                self.transcript, subtitles = progress
                self.subtitles = json.dumps(subtitles)

        for option, variant in self.variants.items():
            if variant == "solid":
                if option == "Transcript":
                    await self.generate_transcript()
                elif option == "Subtitles":
                    await self.generate_subtitles()
                elif option == "Chapters":
                    await self.generate_chapters()
                elif option == "Summary":
                    await self.generate_summary()
        yield

    async def generate_transcript(self):
        self.complete["Transcript"] = True

    async def generate_subtitles(self):
        self.complete["Subtitles"] = True

    async def generate_chapters(self):
        print("Generating chapters...")
        try:
            client = AsyncClient()
            response = await client.chat(
                model='llama3:8b',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant that generates chapters for a video transcript. Only reply with the chapter titles.',
                    },
                    {
                        'role': 'user',
                        'content': f'Please generate {self.num_chapters} chapters for the following transcript:\n\n{self.transcript}',
                    }
                ]
            )
            self.chapters = response['message']['content']
            self.complete["Chapters"] = True
        except Exception as e:
            print(f"Error generating chapters: {str(e)}")
            self.chapters = "Error generating chapters. Please try again."

    async def generate_summary(self):
        print("Generating summary...")
        try:
            client = AsyncClient()
            response = await client.chat(
                model='llama3:8b',
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant that summarizes transcripts. Only reply with the summary.',
                    },
                    {
                        'role': 'user',
                        'content': f'Please summarize the following transcript in a concise manner:\n\n{self.transcript}',
                    }
                ]
            )
            self.summary = response['message']['content']
            self.complete["Summary"] = True
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            self.summary = "Error generating summary. Please try again."