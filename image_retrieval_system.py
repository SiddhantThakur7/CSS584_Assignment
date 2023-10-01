import os
import PySimpleGUI as psg

psg.theme("LightGrey1")
# psg.set_options()
pagination_font = "Arial 16 bold"


def generate_image_gallery(size=(160, 160), page_length=18, cols=6):
    pagination_element = [
        psg.Button("<", font=pagination_font),
        psg.Text("1", font=pagination_font),
        psg.Button(">", font=pagination_font),
    ]
    image_gallery_layout = []
    start = 0
    cur = 1
    while cur <= start + page_length:
        temp = []
        for _ in range(cols):
            temp.append(
                psg.Image(
                    "{path}\\images\\png\\{id}.png".format(path=os.getcwd(), id=cur),
                    pad=16,
                    size=size,
                    key="-IMAGE_{id}-".format(id=cur),
                    enable_events=True,
                )
            )
            cur += 1
        image_gallery_layout.append(temp)

    image_gallery_layout.append(
        [
            psg.Frame(
                "",
                [pagination_element],
                expand_x=True,
                element_justification="center",
                border_width=0,
            )
        ]
    )
    image_gallery_layout = [
        psg.Frame(
            "",
            image_gallery_layout,
            expand_x=True,
            expand_y=True,
            pad=(16),
            element_justification="center",
            vertical_alignment="center",
        )
    ]
    return image_gallery_layout


def createWindow(image_selected):
    layout = None
    default_text_element = [
        psg.Text(
            "Please select an image",
            font="Arial 20",
            expand_x=True,
            justification="center",
            pad=(16, 8),
        ),
    ]
    if image_selected:
        image_operations_layout = [
            [
                psg.Image(
                    "{path}\\images\\png\\{id}.png".format(
                        path=os.getcwd(), id=image_selected
                    ),
                    size=(320, 320),
                )
            ],
            [
                psg.Combo(
                    ["Intensity", "Color", "Energy"],
                    default_value="Intensity",
                    expand_x=True,
                    enable_events=True,
                    readonly=True,
                    key="-METHOD-",
                )
            ],
            [psg.Button("Retrieve Images", expand_x=True)],
            [psg.Button("Reset", key="-RESET-", expand_x=True, pad=((0, 0), (32, 0)))],
        ]
        layout = [
            [
                psg.Column(
                    image_operations_layout,
                    size=(296, 1200),
                    element_justification="center",
                    pad=(16, 96),
                ),
                psg.Column(
                    [generate_image_gallery((128, 128), 20, 5)],
                    expand_y=True,
                    expand_x=True,
                ),
            ]
        ]
    else:
        layout = [default_text_element, generate_image_gallery()]
    return psg.Window(
        "Image Retrieval System", layout, size=(1280, 786), margins=(16, 16)
    )


window = createWindow(None)

# Event Loop
while True:
    event, values = window.read()
    event_parameters = event.split("_") if event else None
    if event == psg.WIN_CLOSED:
        break

    if "-IMAGE" in event.split("_"):
        window, window2 = createWindow(event_parameters[1][:-1]), window
        window2.close()

    if event == "-RESET-":
        window, window2 = createWindow(None), window
        window2.close()

window.close()
