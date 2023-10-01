import os
import tkinter as tk
from tkinter import ttk

# Constants
page_length = 18
cols = 6
size = (160, 160)
pagination_font = ("Arial", 16, "bold")

# Initial values
curr_page = 1
image_selected = None
root = tk.Tk()

def generate_image_gallery(curr_page):
    start = (curr_page - 1) * page_length
    if start >= 100:
        curr_page -= 1
    elif curr_page < 0:
        curr_page += 1

    cur = start + 1

    # Create pagination elements
    prev_button = tk.Button(root, text="<", font=pagination_font, state=tk.DISABLED if start == 0 else tk.NORMAL, command=lambda: update_page(curr_page - 1))
    page_label = tk.Label(root, text=str(curr_page), font=pagination_font)
    next_button = tk.Button(root, text=">", font=pagination_font, state=tk.DISABLED if start + page_length >= 100 else tk.NORMAL, command=lambda: update_page(curr_page + 1))

    pagination_frame = ttk.Frame(root)
    pagination_frame.grid(row=0, column=0, columnspan=cols)
    prev_button.grid(row=0, column=0)
    page_label.grid(row=0, column=1)
    next_button.grid(row=0, column=2)

    # Create image gallery
    image_gallery = []
    for i in range(page_length):
        row = []
        for j in range(cols):
            if cur <= 100:
                image_path = os.path.join(os.getcwd(), "images", "png", f"{cur}.png")
                image = tk.PhotoImage(file=image_path)
                image_button = tk.Button(root, image=image, command=lambda id=cur: image_clicked(id))
                image_button.image = image
                image_button.grid(row=i+1, column=j, padx=16, pady=16)
                row.append(image_button)
                cur += 1
        image_gallery.append(row)

def createWindow(image_selected, page_number):
    root = tk.Tk()
    root.title("Image Retrieval System")
    root.geometry("1280x786")

    if image_selected:
        # Implement the layout for the operations page when an image is selected
        pass
    else:
        default_text_label = tk.Label(root, text="Please select an image", font=("Arial", 20))
        default_text_label.pack(expand=True, fill="both", padx=16, pady=8)
        generate_image_gallery(page_number)

    root.mainloop()

def update_page(new_page):
    global curr_page
    curr_page = new_page
    createWindow(image_selected, curr_page)

def image_clicked(id):
    global image_selected
    image_selected = id
    createWindow(image_selected, curr_page)

# Initial window
createWindow(None, curr_page)
