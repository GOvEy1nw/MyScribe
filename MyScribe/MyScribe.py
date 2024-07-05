import reflex as rx
from rxconfig import config
from . import pages

app = rx.App(
    style={
        ".settings-button": {
            "position": "fixed",
            "bottom": "5em",
            "left": "2em",
            "color": "inherit",
            "z-index": "20",
            "background": "transparent",
            },
        ".settings-button:hover": {
            "cursor": "pointer",
            },
        ".startover-button": {
            "position": "fixed",
            "top": "2em",
            "left": "2em",
            "z-index": "20",
            },
        ".startover-button:hover": {
            "cursor": "pointer",
            },
        }
)
app.add_page(pages.index)
app.add_page(pages.options, route="/options")
app.add_page(pages.output, route="/output")