import reflex as rx
from ..utils.whisper_processor import process_audio
from ..utils.gen_SumChap import generate_chapters, generate_summary

class uploadState(rx.State):
    file: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s)."""
        if files:
            self.file = files[0].filename
            for file in files:
                upload_data = await file.read()
                outfile = rx.get_upload_dir() / file.filename

                # Save the file.
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)

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

    generate_button: bool = False
    gen_start: bool = False

    num_chapters: str = "5 Chapters"
    transcript: str = rx.LocalStorage("", name="transcript")
    subtitles: str = rx.LocalStorage("", name="subtitles")
    chapters: str = rx.LocalStorage("", name="chapters")
    summary: str = rx.LocalStorage("", name="summary")

    def change_variant(self, button: str):
        self.variants[button] = "solid" if self.variants[button] == "outline" else "outline"

    async def generate(self):
        self.gen_start = True
        self.generate_button = True
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
                self.grab_subs = subtitles

        for option, variant in self.variants.items():
            if variant == "solid":
                if option == "Transcript":
                    await self.transcript_complete()
                elif option == "Subtitles":
                    await self.subtitles_complete()
                elif option == "Chapters":
                    await self.chapters_complete()
                elif option == "Summary":
                    await self.summary_complete()
        yield

    async def transcript_complete(self):
        self.complete["Transcript"] = True

    async def subtitles_complete(self):
        self.subtitles = self.grab_subs
        self.complete["Subtitles"] = True

    async def chapters_complete(self):
        self.chapters = await generate_chapters(self.transcript, self.num_chapters)
        self.complete["Chapters"] = True

    async def summary_complete(self):
        self.summary = await generate_summary(self.transcript)
        self.complete["Summary"] = True

    def download_srt(self):
        return rx.download(
            data=self.subtitles,
            filename="subtitles.srt"
        )