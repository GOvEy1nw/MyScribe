import reflex as rx
from ..ui.base import base_page
from .options import options
from ..states.state import uploadState

def index() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Generate Subtitles, Chapters & Summaries from videos in", rx.text(" seconds", as_="span", color_scheme="indigo"), size="8", align="center"),
            rx.container(
                rx.cond(
                    uploadState.file == "",
                    rx.upload(
                        rx.text("Drag and drop files here or click to select files"),
                        multiple=False,
                        on_drop=uploadState.handle_upload(rx.upload_files(upload_id="upload1")),
                        id="file_upload",
                        width="100%",
                        border="none",
                        padding="5em",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(f"{uploadState.file}", weight="bold"),
                            rx.button(
                                "X",
                                on_click=uploadState.clear_file,
                                variant="ghost",
                                color_scheme="gray",
                            ),
                            align_items="center",
                        ),
                        rx.text(f"What would you like to generate?"),
                        options(),
                        spacing="3",
                        align_items="center",
                    ),
                ),
                width="100%",
                spacing="5",
                justify="center",
                justify_content="center",
                border="1px dashed rgb(107,99,246)",
                padding="5em",
                min_height="350px",
                border_radius="10px",
            ),
            align_items="center",
        ),
    )