import PySimpleGUI as psg
from Layout import Layout
from ImageProcessor import ImageProcessor

# Set GUI theme and font
psg.theme("LightGrey1")
psg.set_options(font="Arial 14")

# Multiprocessing exclusion gate -- > Code within this block will only be present with 1 process
if __name__ == "__main__":
    # Instantiating the ImageProcessor module
    image_processor = ImageProcessor()
    # Instantiate the Layout module
    current_layout = Layout(image_processor.default_image_list)

    window_prev = None

    # Create window using default state layout
    window = current_layout.createWindow()

    # Event Loop
    while True:
        # Monitoring events and user (generated/selected) values
        event, values = window.read(timeout=100)
        event_parameters = event.split("_") if event else None

        # Window close button Event
        if event == psg.WIN_CLOSED:
            break
        if window_prev:
            window_prev.close()
            window_prev = None

        # Image select event
        if event_parameters and "-IMAGE" in event_parameters:
            current_layout.curr_page = 1
            current_layout.selected_image = event_parameters[1][:-1]
            window, window_prev = current_layout.createWindow(), window

        # State reset to default event
        if event == "-RESET-":
            current_layout.curr_page = 1
            current_layout.selected_image = None
            current_layout.images = image_processor.default_image_list
            window, window_prev = current_layout.createWindow(), window

        # Retrieve similar images event
        if event == "-RETRIEVE-":
            current_layout.similarity_method = values["-METHOD-"]
            current_layout.images = image_processor.retrieve_similar_images(
                current_layout.selected_image,
                current_layout.similarity_method,
            )
            window, window_prev = current_layout.createWindow(), window
            
        # Navigate to the next page event.
        if event == "-NEXT_PAGE-":
            current_layout.curr_page += 1
            window, window_prev = current_layout.createWindow(), window

        # Navigate to the previous page event.
        if event == "-PREVIOUS_PAGE-":
            current_layout.curr_page -= 1
            window, window_prev = current_layout.createWindow(), window

    window.close()
