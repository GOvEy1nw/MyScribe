import reflex as rx
from ..states.state import ClickState

def options() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.cond(
                ClickState.complete["Transcript"] == True,
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Transcript", variant=ClickState.variants["Transcript"], size="4", on_click=ClickState.change_variant("Transcript"), loading=ClickState.processing["Transcript"], disabled=ClickState.disable["Transcript"]),
            ),
            rx.cond(
                ClickState.complete["Subtitles"] == True,
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Subtitles", variant=ClickState.variants["Subtitles"], size="4", on_click=ClickState.change_variant("Subtitles"), loading=ClickState.processing["Subtitles"], disabled=ClickState.disable["Subtitles"]),
            ),
            rx.cond(
                ClickState.complete["Chapters"] == True,
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Chapters", variant=ClickState.variants["Chapters"], size="4", on_click=ClickState.change_variant("Chapters"), loading=ClickState.processing["Chapters"], disabled=ClickState.disable["Chapters"]),
            ),
            rx.cond(
                ClickState.complete["Summary"] == True,
                rx.button("Done", variant="solid", size="4", color_scheme="green"),
                rx.button("Summary", variant=ClickState.variants["Summary"], size="4", on_click=ClickState.change_variant("Summary"), loading=ClickState.processing["Summary"], disabled=ClickState.disable["Summary"]),
            ),
            width="100%",
            justify="center",
            spacing="5",
        ),
        rx.hstack(
            rx.flex(
                rx.text(
                    "Original Language",
                    size="2",
                    mb="1",
                    color_scheme="gray",
                ),
                rx.select(
                    ["Auto Detect", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Japanese", "Chinese"],
                    default_value="Auto Detect",
                ),
                justify_content="center",
                flex_direction="column",
                align="center",
            ),
                rx.cond(
                    ClickState.variants["Chapters"] == "solid",
                    rx.flex(
                        rx.text(
                            "Number of Chapters",
                            size="2",
                            mb="1",
                            color_scheme="gray",
                        ),
                        rx.select(
                            ["2 Chapters", "3 Chapters", "4 Chapters", "5 Chapters", "6 Chapters", "7 Chapters", "8 Chapters", "9 Chapters", "10 Chapters"],
                            default_value="5 Chapters",
                        ),
                        justify_content="center",
                        flex_direction="column",
                        align="center",
                        ),
                    ),
                rx.cond(
                    (ClickState.variants["Chapters"] == "solid") | (ClickState.variants["Summary"] == "solid"),
                    rx.flex(
                        rx.text(
                            "LLM",
                            size="2",
                            mb="1",
                            color_scheme="gray",
                        ),
                        rx.select(
                            ["Ollama", "OpenAI", "Claude"],
                            default_value="Ollama",
                        ),
                        justify_content="center",
                        flex_direction="column",
                        align="center",
                    )
                ),
                ),
        rx.cond(
            (ClickState.variants["Transcript"] == "solid") | 
            (ClickState.variants["Subtitles"] == "solid") | 
            (ClickState.variants["Chapters"] == "solid") | 
            (ClickState.variants["Summary"] == "solid"),
            rx.button("Generate", variant="solid", size="4", on_click=ClickState.generate),
            rx.button("Generate", variant="solid", disabled=True, size="4"),
        ),
        width="100%",
        spacing="4",
        align="center",
        justify_content="center",
        )
