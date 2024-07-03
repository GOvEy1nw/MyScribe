import reflex as rx
from ..ui.base import base_page

def processing() -> rx.Component:
    # Welcome Page (Index)
    return base_page(
        rx.vstack(
            rx.heading("Generate Subtitles, Chapters & Summaries from videos in", rx.text(" seconds", as_="span", color_scheme="indigo"), size="8", align="center"),
            rx.container(
                rx.hstack(
                    rx.chakra.circular_progress(is_indeterminate=True, id="Transcript"),
                    rx.chakra.circular_progress(is_indeterminate=True, id="Subtitles"),
                    rx.chakra.circular_progress(is_indeterminate=True, id="Chapters"),
                    rx.chakra.circular_progress(is_indeterminate=True, id="Summaries"),
                    width="100%",
                    justify="center",
                    spacing="5",
                ),
            width="100%",
            spacing="5",
            justify="center",
            border="1px dashed rgb(107,99,246)",
            padding="5em",
            ),
            rx.button("View", variant="solid"),
            align_items="center",
            ),
        )