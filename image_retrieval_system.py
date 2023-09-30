import PySimpleGUI as psg

psg.theme('LightGrey1')
# psg.set_options()
pagination_font = "Arial 16 bold"

default_text_element = [
    psg.Text("Please select an image", font="Arial 20", expand_x=True, justification="center", pad=(16, 8)),
]

pagination_element = [psg.Button('<', font=pagination_font), psg.Text("1", font=pagination_font), psg.Button('>', font=pagination_font)]

image_gallery_layout = []
for i in range(4):
    image_gallery_layout.append([psg.Button("Image", expand_x=True, expand_y=True, pad=16) for _ in range(5)])
image_gallery_layout.append([psg.Frame('', [pagination_element], expand_x=True, element_justification='center',border_width=0)])
image_gallery_layout = [psg.Frame('', image_gallery_layout, expand_x=True, expand_y=True, pad=(16))]

operation_selection_layout = psg.Frame('', [[psg.Combo(['Intensity', 'Color', 'Energy']), psg.Button('Retrieve Images')], [psg.Button('Retrieve Images')]], expand_x=True, border_width=0)
selected_image_layout = psg.Frame('', [[psg.Button("Selected Image", size=(32, 16))]], border_width=0)
image_operation_layout = [psg.Frame('', [[selected_image_layout, operation_selection_layout]], expand_x=True, border_width=0)]

imo_v = psg.Column([[psg.Button("Selected Image", size=(32, 16))], [psg.Combo(['Intensity', 'Color', 'Energy'], expand_x=True)], [psg.Button('Retrieve Images', expand_x=True)], [psg.Button('Retrieve Images', expand_x=True)]], size=(296, 1200), element_justification='center', vertical_alignment='center', pad=(16, 96))
img_v = psg.Column([image_gallery_layout], expand_y=True, expand_x=True)

def createWindow(imageSelected=False):
    defaultLayout = [
        default_text_element,
        image_gallery_layout
    ]

    operational_layout = [
        [imo_v, img_v]
    ]

    layout = defaultLayout

    return psg.Window("Image Retrieval System", layout, size=(1280, 786), margins=(16, 16))

window = createWindow()

# Event Loop
while True:
    event, values = window.read()
    if event == psg.WIN_CLOSED:
        break

    if event == "-B1-":
        # window['-T1-'].update(values['-INPUT-'])
        window["-T1-"].update(visible=not window["-T1-"].visible)
        window.layout = []
    if event == "-B2-":
        print("Test Button Pressed!")

window.close()