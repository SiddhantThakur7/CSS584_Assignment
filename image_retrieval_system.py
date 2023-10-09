import PySimpleGUI as psg
from Layout import Layout
from ImageProcessor import ImageProcessor

psg.theme("LightGrey1")
psg.set_options(font='Arial 14')
if __name__ == '__main__':
    image_processor = ImageProcessor()
    current_layout = Layout(len(image_processor.images))
    image_order = list(image_processor.images.values())

    window = current_layout.createWindow(image_order)

    window_prev = None
    # Event Loop
    while True:
        event, values = window.read(timeout=100)
        event_parameters = event.split("_") if event else None
        if event == psg.WIN_CLOSED:
            break
        if window_prev:
            window_prev.close()
            window_prev = None

        if event_parameters and "-IMAGE" in event_parameters:
            current_layout.curr_page = 1
            current_layout.image_selected = event_parameters[1][:-1]
            window, window_prev = current_layout.createWindow(image_order), window

        if event == "-RESET-":
            current_layout.curr_page = 1
            current_layout.image_selected = None
            window, window_prev = current_layout.createWindow(image_order), window

        if event == '-RETRIEVE-':
            current_layout.similarity_method = values['-METHOD-']
            window, window_prev = current_layout.createWindow(image_processor.retrieve_similar_images(int(current_layout.image_selected), current_layout.similarity_method)), window

        if event == "-NEXT_PAGE-":
            current_layout.curr_page += 1
            window, window_prev = current_layout.createWindow(image_order), window

        if event == "-PREVIOUS_PAGE-":
            current_layout.curr_page -= 1
            window, window_prev = current_layout.createWindow(image_order), window

    window.close()
