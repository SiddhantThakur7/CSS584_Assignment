import PySimpleGUI as psg
from Layout import Layout
from ImageProcessor import ImageProcessor

psg.theme("LightGrey1")
psg.set_options(font="Arial 14")

if __name__ == "__main__":
    image_processor = ImageProcessor()
    current_layout = Layout(image_processor.default_image_list)

    window_prev = None
    window = current_layout.createWindow()

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
            current_layout.selected_image = event_parameters[1][:-1]
            window, window_prev = current_layout.createWindow(), window

        if event == "-RESET-":
            current_layout.curr_page = 1
            current_layout.selected_image = None
            current_layout.images = image_processor.default_image_list
            window, window_prev = current_layout.createWindow(), window

        if event == "-RETRIEVE-":
            current_layout.similarity_method = values["-METHOD-"]
            current_layout.images = image_processor.retrieve_similar_images(
                int(current_layout.selected_image),
                current_layout.similarity_method,
            )
            window, window_prev = current_layout.createWindow(), window
            

        if event == "-NEXT_PAGE-":
            current_layout.curr_page += 1
            window, window_prev = current_layout.createWindow(), window

        if event == "-PREVIOUS_PAGE-":
            current_layout.curr_page -= 1
            window, window_prev = current_layout.createWindow(), window

    window.close()
