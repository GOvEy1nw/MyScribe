import reflex as rx
from ..ui.base import base_page
from .options import options
from ..states.state import uploadState, InitState, ClickState


@rx.page(on_load=InitState.init_state)
def index() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Generate Subtitles, Chapters & Summaries from videos in", rx.text(" seconds", as_="span", color_scheme="indigo"), size="8", align="center"),
            rx.container(
                rx.cond(
                    uploadState.file_loaded == "False",
                    rx.vstack(
                        rx.upload(
                            rx.text("Drag and drop files here or click to select files"),
                        multiple=False,
                        id="file_upload",
                        on_drop=uploadState.handle_upload(
                            rx.upload_files(
                                upload_id="file_upload",
                                on_upload_progress=uploadState.handle_upload_progress)),
                        width="100%",
                        border="none",
                        padding="5em",
                        ),
                        rx.progress(value=uploadState.up_progress, max=100),
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text(uploadState.file, weight="bold"),
                            rx.button(
                                "X",
                                on_click=ClickState.clear_file,
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