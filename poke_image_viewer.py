"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import os
import poke_api
import image_lib
import ctypes
import inspect

# Get the script and images directory
script_name = inspect.getfile(inspect.currentframe())
script_dir = os.path.dirname(os.path.abspath(script_name))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")
root.geometry('600x600')
root.minsize(500, 600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
root.iconbitmap(os.path.join(script_dir, 'poke_ball.ico'))

# Create frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky=NSEW)

# TODO: Populate frames with widgets and define event handler functions
image_path = os.path.join(script_dir, 'poke_ball.png')
photo = PhotoImage(file=image_path)

# Create and place widgets
lbl_image = ttk.Label(frm, image=photo)
lbl_image.grid(row=0, column=0, padx=0)


# Populate frames with widgets and define event handler functions
def handle_set_desktop():
    """Sets the currently displayed image as the desktop background."""
    current_image_path = lbl_image.image_path
    if current_image_path:
        image_lib.set_desktop_background_image(current_image_path)

def handle_poke_sel(event):
    """Fetches and displays the selected Pokémon's artwork."""
    pokemon_name = cbox_poke_sel.get()
    if pokemon_name:
        image_path = poke_api.download_pokemon_artwork(pokemon_name, images_dir)
        if image_path:
            photo = PhotoImage(file=image_path)
            lbl_image.config(image=photo)
            lbl_image.image = photo  # Keep a reference to avoid garbage collection
            lbl_image.image_path = image_path
            btn_set_desktop.config(state=NORMAL)
        else:
            print(f'Failed to download artwork for {pokemon_name}.')


cbox_poke_sel = ttk.Combobox(frm)
cbox_poke_sel.grid(row=1, column=0, pady=10)
cbox_poke_sel.bind('<<ComboboxSelected>>', handle_poke_sel)

btn_set_desktop = ttk.Button(frm, text="Set as Desktop Image", command=handle_set_desktop, state=DISABLED)
btn_set_desktop.grid(row=2, column=0, padx=0, pady=10)

# Populate the Combobox with Pokémon names
def populate_pokemon_list():
    """Populates the Combobox with a list of Pokémon names."""
    pokemon_names = poke_api.get_pokemon_names(limit=100)  # Adjust limit as needed
    cbox_poke_sel['values'] = pokemon_names

populate_pokemon_list()

root.mainloop()
