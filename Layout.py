import PySimpleGUI as psg

pagination_font = "Arial 16 bold"
DEFAULT_SIMILARITY_METHOD = "Intensity"


class Layout:
    def __init__(self, MAX) -> None:
        self.curr_page = 1
        self.image_selected = None
        self.MAX = MAX
        self.similarity_method = DEFAULT_SIMILARITY_METHOD

    def generate_image_gallery(
        self, image_list, size=(152, 152), page_length=18, cols=6
    ):
        start = (self.curr_page - 1) * page_length
        if start >= self.MAX:
            self.curr_page -= 1
        elif self.curr_page <= 0:
            self.curr_page += 1

        cur = start
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
        while cur < min(start + page_length, self.MAX):
            temp = []
            for _ in range(cols):
                temp.append(
                    psg.Column(
                        [
                            [
                                psg.Image(
                                    "{path}".format(path=image_list[cur]["path"]),
                                    pad=(16, 4 / 2),
                                    size=size,
                                    key="-IMAGE_{id}-".format(id=cur + 1),
                                    enable_events=True,
                                )
                            ],
                            [
                                psg.Text(
                                    "{name}".format(name=image_list[cur]["name"]),
                                    expand_x=True,
                                    justification="center",
                                )
                            ],
                        ]
                    )
                )
                cur += 1
                if cur >= self.MAX:
                    break
            image_gallery_layout.append(temp)
        image_gallery_layout.append(
            [
                psg.Column(
                    [pagination_element],
                    expand_x=True,
                    element_justification="center",
                )
            ]
        )
        image_gallery_layout = [
            psg.Column(
                image_gallery_layout,
                expand_x=True,
                expand_y=True,
                pad=(16),
                element_justification="center",
                vertical_alignment="center",
            )
        ]
        return image_gallery_layout

    def createWindow(self, image_list):
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
                        size=(300, 240),
                        pad=(0, 36/4),
                    )
                ],
                [
                    psg.Text(
                        "{id}".format(id=self.image_selected),
                        expand_x=True,
                        justification="center",
                    )
                ],
                [
                    psg.Combo(
                        ["Intensity", "Color", "Energy"],
                        default_value=self.similarity_method,
                        pad=(8, 36),
                        expand_x=True,
                        enable_events=True,
                        readonly=True,
                        key="-METHOD-",
                    )
                ],
                [
                    psg.Column(
                        [
                            [
                                psg.Button(
                                    "Retrieve Images",
                                    key="-RETRIEVE-",
                                    expand_x=True,
                                )
                            ],
                            [
                                psg.Button(
                                    "Reset",
                                    key="-RESET-",
                                    expand_x=True,
                                )
                            ],
                        ],
                        key="-OPERATIONS_CONTROL-",
                        pad=((0, 0), (48, 0)),
                        expand_x=True,
                        element_justification="center",
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
                                        pad=(16, 16),
                                    ),
                                    psg.Frame(
                                        "Similar Images",
                                        [
                                            self.generate_image_gallery(
                                                image_list, (120, 120), 20, 5
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
                        [default_text_element, self.generate_image_gallery(image_list)],
                        key="-PARENT-",
                    )
                ]
            ]
        return psg.Window(
            "Image Retrieval System", layout, size=(1280, 786), margins=(16, 16)
        )

    image_selected = None
    curr_page = 1
