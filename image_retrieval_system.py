import PySimpleGUI as psg

psg.theme("LightGrey1")
# psg.set_options()
pagination_font = "Arial 16 bold"


class Layout:
    def __init__(self) -> None:
        self.curr_page = 1
        self.image_selected = None
        self.MAX = 100

    def generate_image_gallery(self, size=(160, 160), page_length=18, cols=6):
        start = (self.curr_page - 1) * page_length
        if start >= self.MAX:
            self.curr_page -= 1
        elif self.curr_page <= 0:
            self.curr_page += 1

        cur = start + 1
        pagination_element = [
            psg.Button(
                "<",
                font=pagination_font,
                key="-PREVIOUS_PAGE-",
                disabled=True if start == 0 else False,
            ),
            psg.Text(f"{self.curr_page}", font=pagination_font, key="-PAGE_POSITION-"),
            psg.Button(
                ">",
                font=pagination_font,
                key="-NEXT_PAGE-",
                disabled=True if start + page_length >= 100 else False,
            ),
        ]

        image_gallery_layout = []
        while cur <= min(start + page_length, self.MAX):
            temp = []
            for _ in range(cols):
                temp.append(
                    psg.Image(
                        ".\\images\\png\\{id}.png".format(id=cur),
                        pad=16,
                        size=size,
                        key="-IMAGE_{id}-".format(id=cur),
                        enable_events=True,
                    )
                )
                cur += 1
                if cur > self.MAX:
                    break
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

    def createWindow(self):
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
        if self.image_selected:
            image_operations_layout = [
                [
                    psg.Image(
                        ".\\images\\png\\{id}.png".format(id=self.image_selected),
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
                [
                    psg.Button(
                        "Reset", key="-RESET-", expand_x=True, pad=((0, 0), (32, 0))
                    )
                ],
            ]
            layout = [
                [
                    [
                        psg.Column(
                            [
                                [
                                    psg.Column(
                                        image_operations_layout,
                                        size=(296, 1200),
                                        element_justification="center",
                                        pad=(16, 96),
                                    ),
                                    psg.Column(
                                        [
                                            self.generate_image_gallery(
                                                (128, 128), 20, 5
                                            )
                                        ],
                                        expand_y=True,
                                        expand_x=True,
                                    ),
                                ]
                            ],
                            key="-PARENT-",
                        )
                    ]
                ]
            ]
        else:
            layout = [
                [
                    psg.Column(
                        [default_text_element, self.generate_image_gallery()],
                        key="-PARENT-",
                    )
                ]
            ]
        return psg.Window(
            "Image Retrieval System", layout, size=(1280, 786), margins=(16, 16)
        )

    image_selected = None
    curr_page = 1


current_layout = Layout()
window = current_layout.createWindow()
window2 = None
# Event Loop
while True:
    event, values = window.read(timeout=100)
    event_parameters = event.split("_") if event else None
    if event == psg.WIN_CLOSED:
        break
    if window2:
        window2.close()
        window2 = None

    if "-IMAGE" in event.split("_"):
        current_layout.curr_page = 1
        current_layout.image_selected = event_parameters[1][:-1]
        window, window2 = current_layout.createWindow(), window

    if event == "-RESET-":
        current_layout.curr_page = 1
        current_layout.image_selected = None
        window, window2 = current_layout.createWindow(), window

    if event == "-NEXT_PAGE-":
        current_layout.curr_page += 1
        window, window2 = current_layout.createWindow(), window

    if event == "-PREVIOUS_PAGE-":
        current_layout.curr_page -= 1
        window, window2 = current_layout.createWindow(), window

window.close()
