import reflex as rx
from rxconfig import config
from . import pages

app = rx.App(
    style={
        ".settings-button": {
            "position": "absolute",
            "bottom": "5em",
            "left": "2em",
            "color": "inherit",
            "z-index": "20",
            "background": "transparent",
            },
        ".settings-button:hover": {
            "cursor": "pointer",
            },
        }
)
app.add_page(pages.index)
app.add_page(pages.options, route="/options")