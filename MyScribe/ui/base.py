import reflex as rx
from ..states.state import llm_selected

def base_page(child: rx.Component) -> rx.Component:
    return rx.container(
        child,
        rx.color_mode.button(position="bottom-left"),
        rx.popover.root(
            rx.popover.trigger(rx.icon_button(rx.icon("cog"), class_name="settings-button")),
            rx.popover.content(
                rx.flex(
                    rx.select(
                        llm_selected.llmOptions,
                        label="LLM", placeholder="Select an LLM",
                        value=llm_selected.llm,
                        on_change=llm_selected.set_llm
                        ),
                    rx.cond(
                        llm_selected.llm == "Ollama",
                        rx.flex(
                            rx.select(["Llama:8b"],
                                      label="Installed Models",
                                      placeholder="Select a Model",
                                      ),
                            rx.input(label="Model", placeholder="Enter Ollama Model"),
                            rx.button("download", variant="solid"),
                            direction="column",
                            spacing="3",
                        ),
                        rx.flex(
                            rx.input(
                                label="API Key",
                                placeholder="Enter your API key",
                                value=llm_selected.api_key,
                                on_change=llm_selected.set_api_key
                            ),
                            rx.button(
                                "Save",
                                variant="solid",
                                on_click=llm_selected.save_api_key
                            ),
                            rx.button(
                                "delete",
                                variant="solid",
                                on_click=llm_selected.delete_api_key
                            ),
                            direction="row",
                            spacing="3",
                        ),
                    ),
                    direction="column",
                    spacing="3",
                ),
            ),
        ),
        width="100%",
        min_height="85vh",
        align_items="center",
        padding_top="100px",
        size="4",
    )