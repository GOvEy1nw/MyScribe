import reflex as rx
from ..states.state import ClickState, uploadState

def options() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.cond(
                ClickState.complete["Transcript"],
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Transcript", variant=ClickState.variants["Transcript"], size="4", on_click=ClickState.change_variant("Transcript"), loading=ClickState.processing["Transcript"], disabled=ClickState.disable["Transcript"]),
            ),
            rx.cond(
                ClickState.complete["Subtitles"],
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Subtitles", variant=ClickState.variants["Subtitles"], size="4", on_click=ClickState.change_variant("Subtitles"), loading=ClickState.processing["Subtitles"], disabled=ClickState.disable["Subtitles"]),
            ),
            rx.cond(
                ClickState.complete["Chapters"],
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Chapters", variant=ClickState.variants["Chapters"], size="4", on_click=ClickState.change_variant("Chapters"), loading=ClickState.processing["Chapters"], disabled=ClickState.disable["Chapters"]),
            ),
            rx.cond(
                ClickState.complete["Summary"],
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Summary", variant=ClickState.variants["Summary"], size="4", on_click=ClickState.change_variant("Summary"), loading=ClickState.processing["Summary"], disabled=ClickState.disable["Summary"]),
            ),
            width="100%",
            justify="center",
            spacing="5",
        ),

        rx.cond(
            ~ClickState.gen_start,
            rx.hstack(
                rx.flex(
                    rx.text(
                        "Original Language",
                        size="2",
                        mb="1",
                        color_scheme="gray",
                    ),
                    rx.cond(
                        (ClickState.variants["Transcript"] == "solid") | 
                        (ClickState.variants["Subtitles"] == "solid") | 
                        (ClickState.variants["Chapters"] == "solid") | 
                        (ClickState.variants["Summary"] == "solid"),
                        rx.select(
                            ["Auto Detect", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Japanese", "Chinese"],
                            default_value="Auto Detect"
                        ),
                        rx.select(
                            ["Auto Detect", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Japanese", "Chinese"],
                            default_value="Auto Detect", disabled=True
                        ),
                    ),
                    justify_content="center",
                    flex_direction="column",
                    align="center",
                ),
            ),
        ),

        rx.cond(
            ClickState.finished,
                rx.vstack(
                    rx.text(ClickState.transcribing_message),
                    rx.button(
                        "View",
                        on_click=rx.redirect(   
                            "/output",
                            ),
                        size="4",
                    ),
                    width="100%",
                    spacing="4",
                    align="center",
                    justify_content="center",
                ),
                rx.cond(
                    (ClickState.variants["Transcript"] == "solid") | 
                    (ClickState.variants["Subtitles"] == "solid") | 
                    (ClickState.variants["Chapters"] == "solid") | 
                    (ClickState.variants["Summary"] == "solid"),
                    rx.vstack(
                        rx.text(ClickState.transcribing_message),
                        rx.button("Generate", variant="solid", disabled=ClickState.generate_button, size="4", on_click=ClickState.generate),
                    ),
                    rx.vstack(
                        rx.text(ClickState.transcribing_message),
                        rx.button("Generate", variant="solid", disabled=True, size="4"),
                    ),
                ),
        ),
        width="100%",
        spacing="4",
        align="center",
        justify_content="center",
        )