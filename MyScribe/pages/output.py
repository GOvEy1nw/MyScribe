import reflex as rx
from ..ui.base import base_page
from ..states.state import uploadState, ResetState, ClickState

@rx.page(on_load=ResetState.reset_state)
def output() -> rx.Component:
    file_path = rx.get_upload_url(uploadState.file)
    return base_page(
        rx.vstack(
            rx.button(
                "Start Over",
                on_click=rx.redirect(
                    "/",
                ),
                class_name="startover-button",
                variant="solid",
            ),
            rx.heading("WOWVI", rx.text("Scribe", as_="span", color_scheme="pink"), size="8", align="center"),
            rx.container(
                rx.heading(f"{uploadState.file}", weight="bold"),
                rx.video(
                    url=file_path,
                    controls=True,
                    width="auto",
                    max_height="500px",
                    class_name="media-player",
                ),
            ),
                rx.cond(
                    (ClickState.btn_transcript == "True") & (ClickState.transcript != ""),
                    rx.vstack(
                        rx.button(
                            "Download SRT",
                            on_click=ClickState.download_srt,
                            variant="solid",
                            color_scheme="pink",
                            margin_top="1em",
                        ),
                        width="100%",
                        align_items="center",
                    ),
                ),
                rx.cond(
                    (ClickState.btn_summary == "True") & (ClickState.summary != ""),
                    rx.scroll_area(
                        rx.flex(
                            rx.heading("Summary", padding_bottom="10px"),
                            rx.text(f"{ClickState.summary}"),
                            direction="column",
                            align_items="center",
                            background_color="#f5f5f5",
                            padding="1em",
                            border_radius="1em",
                            ),
                        type="auto",
                        scrollbars="vertical",
                        text_align="justify",
                        width="50rem",
                        max_height="600px",
                        padding="1em",
                        ),
                    ),
                rx.cond(
                    (ClickState.btn_chapters == "True") & (ClickState.chapters != ""),
                    rx.flex(
                        rx.heading("Chapters", padding_bottom="10px"),
                        rx.text(f"{ClickState.chapters}", white_space="pre-line"),
                        direction="column",
                        align_items="center",
                        background_color="#f5f5f5",
                        padding="1em",
                        border_radius="1em",
                        ),
                    ),
                rx.cond(
                    (ClickState.btn_transcript == "True") & (ClickState.transcript != ""),
                        rx.flex(
                            rx.heading("Transcript", padding_bottom="10px"),
                            rx.scroll_area(
                                rx.text(f"{ClickState.transcript}", white_space="pre-line", size="2"),
                                type="auto",
                                scrollbars="vertical",
                                text_align="justify",
                                width="50rem",
                                max_height="800px",
                            ),  # Use pre-line to preserve line breaks
                            direction="column",
                            align_items="center",
                            background_color="#f5f5f5",
                            padding="1em",
                            border_radius="1em",
                            ),
                    ),
            rx.box(height="100px"),
            align_items="center",
            ),
        ),