import reflex as rx
from ..utils.whisper_processor import process_audio
from ..utils.gen_SumChap import generate_chapters, generate_summary

class uploadState(rx.State):
    file: str = rx.LocalStorage("", name="file")
    file_loaded: str = rx.LocalStorage("", name="file_loaded")
    uploading: bool = False
    up_progress: int = 0
    total_bytes: int = 0
    grab_subs: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s)."""
        if files:
            self.file = files[0].filename
            self.file_loaded = True
            for file in files:
                upload_data = await file.read()
                outfile = rx.get_upload_dir() / file.filename
                self.total_bytes += len(await file.read())                

                # Save the file.
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)

    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.up_progress = round(progress["progress"] * 100)
        if self.up_progress >= 100:
            self.uploading = False


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
    gen_start: bool = False
    transcribing_message: str = " "
    generate_button: bool = False
    finished: bool = False

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

    def clear_file(self):
        """Clear the uploaded file."""
        self.file_loaded = "False"
        self.processing = {key: False for key in self.processing}
        self.disable = {key: False for key in self.disable}
        self.complete = {key: False for key in self.complete}
        self.generate_button = False
        self.gen_start = False
        self.initialize_button_variants()
        self.initialize_storage()
        self.uploading = False
        self.up_progress = 0
        self.total_bytes = 0
        self.finished = False

    def initialize_button_variants(self):
        """Initialize button variants based on local storage values."""
        self.variants["Transcript"] = "solid" if self.btn_transcript == "True" else "outline"
        self.variants["Subtitles"] = "solid" if self.btn_subtitles == "True" else "outline"
        self.variants["Chapters"] = "solid" if self.btn_chapters == "True" else "outline"
        self.variants["Summary"] = "solid" if self.btn_summary == "True" else "outline"
    
    def initialize_storage(self):
        """Initialize button variants based on local storage values."""
        self.transcript = self.transcript
        self.subtitles = self.subtitles
        self.chapters = self.chapters
        self.summary = self.summary

    num_chapters: str = rx.LocalStorage("5 Chapters", name="num_chapters")
    transcript: str = rx.LocalStorage("", name="transcript")
    subtitles: str = rx.LocalStorage("", name="subtitles")
    chapters: str = rx.LocalStorage("", name="chapters")
    summary: str = rx.LocalStorage("", name="summary")
    btn_transcript: str = rx.LocalStorage("False", name="btn_transcript")
    btn_subtitles: str = rx.LocalStorage("False", name="btn_subtitles")
    btn_chapters: str = rx.LocalStorage("False", name="btn_chapters")
    btn_summary: str = rx.LocalStorage("False", name="btn_summary")

    def change_variant(self, button: str):
        self.variants[button] = "solid" if self.variants[button] == "outline" else "outline"
        if self.variants[button] == "solid":
            if button == "Transcript":
                self.btn_transcript = "True"
            elif button == "Subtitles":
                self.btn_subtitles = "True"
            elif button == "Chapters":
                self.btn_chapters = "True"
            elif button == "Summary":
                self.btn_summary = "True"
        else:
            if button == "Transcript":
                self.btn_transcript = "False"
            elif button == "Subtitles":
                self.btn_subtitles = "False"
            elif button == "Chapters":
                self.btn_chapters = "False"
            elif button == "Summary":
                self.btn_summary = "False"

    async def generate(self):
        self.transcribing_message = "Processing audio..."
        self.gen_start
        self.generate_button
        uploadState.handle_upload(
            rx.upload_files(
                upload_id="file_upload",
                on_upload_progress=uploadState.handle_upload_progress))
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
                    yield
                elif option == "Subtitles":
                    await self.subtitles_complete()
                    yield
                elif option == "Chapters":
                    await self.chapters_complete()
                    yield
                elif option == "Summary":
                    await self.summary_complete()
                    yield
        self.finished = True
        self.transcribing_message = "Processing complete!"
        yield

    async def transcript_complete(self):
        self.transcribing_message = "Transcribing complete!"
        self.complete["Transcript"] = True
        self.trigger_state_update()

    async def subtitles_complete(self):
        self.transcribing_message = "Subtitles complete!"
        self.subtitles = self.grab_subs
        self.complete["Subtitles"] = True
        self.trigger_state_update()

    async def chapters_complete(self):
        self.transcribing_message = "Chapters complete!"
        self.chapters = await generate_chapters(self.transcript, self.num_chapters)
        self.complete["Chapters"] = True
        self.trigger_state_update()

    async def summary_complete(self):
        self.transcribing_message = "Summary complete!"
        self.summary = await generate_summary(self.transcript)
        self.complete["Summary"] = True
        self.trigger_state_update()

    def trigger_state_update(self):
        """Trigger a state update to ensure UI reflects changes."""
        # This method should be implemented to trigger a state update in your framework.
        pass


    def download_srt(self):
        return rx.download(
            data=self.subtitles,
            filename=self.file + ".en.srt"
        )
    
class ResetState(ClickState):
    def reset_state(self):
        # Don't reset variants as we want to keep user preferences
        self.processing = {key: False for key in self.processing}
        self.disable = {key: False for key in self.disable}
        self.generate_button = False
        self.gen_start = False
        self.uploading = False
        self.up_progress = 0
        self.total_bytes = 0
        self.transcribing_message = ""

class InitState(ClickState):
    def init_state(self):
        self.processing = {key: False for key in self.processing}
        self.disable = {key: False for key in self.disable}
        self.complete = {key: False for key in self.complete}
        self.generate_button = False
        self.gen_start = False
        self.initialize_button_variants()
        self.initialize_storage()
        self.file_loaded = "False"
        self.uploading = False
        self.up_progress = 0
        self.total_bytes = 0
        self.finished = False
        self.transcribing_message = ""
