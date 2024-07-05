import reflex as rx
from ..ui.base import base_page
from ..states.state import uploadState, ResetState, ClickState

@rx.page(on_load=ResetState.reset_state)
def output() -> rx.Component:
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
            rx.heading("Generate Subtitles, Chapters & Summaries from videos in", rx.text(" seconds", as_="span", color_scheme="indigo"), size="8", align="center"),
            rx.container(
                rx.heading(f"{uploadState.file}", weight="bold"),
            ),
                rx.cond(
                    (ClickState.btn_transcript == "True") & (ClickState.transcript != ""),
                    rx.vstack(
                        rx.button(
                            "Download SRT",
                            on_click=ClickState.download_srt,
                            variant="solid",
                            color_scheme="blue",
                            margin_top="1em",
                        ),
                        width="100%",
                        align_items="center",
                    ),
                ),
                rx.cond(
                    (ClickState.btn_chapters == "True") & (ClickState.chapters != ""),
                    rx.scroll_area(
                        rx.flex(
                            rx.heading("Chapters", padding_bottom="10px"),
                            rx.text(f"{ClickState.chapters}", white_space="pre-line"),
                            direction="column",
                            align_items="center",
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
                    (ClickState.btn_summary == "True") & (ClickState.summary != ""),
                    rx.scroll_area(
                        rx.flex(
                            rx.heading("Summary", padding_bottom="10px"),
                            rx.text(f"{ClickState.summary}"),
                            direction="column",
                            align_items="center",
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
                    (ClickState.btn_transcript == "True") & (ClickState.transcript != ""),
                    rx.scroll_area(
                        rx.flex(
                            rx.heading("Transcript", padding_bottom="10px"),
                            rx.text(f"{ClickState.transcript}", white_space="pre-line", size="2"),  # Use pre-line to preserve line breaks
                            direction="column",
                            align_items="center",
                            ),
                        type="auto",
                        scrollbars="vertical",
                        text_align="justify",
                        width="50rem",
                        max_height="600px",
                        padding="1em",
                        ),
                    ),
            rx.box(height="100px"),
            align_items="center",
            ),
        ),