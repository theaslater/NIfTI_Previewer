#!/home/thea/miniconda3/bin/python python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:47:17 2024

@author: thea
"""

import sys
import os
import time
import nibabel as nib
import matplotlib.pyplot as plt

class Interact:
    def __init__(self, data, dims, axes):
        # Initialize all nessessary variables
        self.data = data
        self.dims = dims
        self.axes = axes
        # Select middle slice on each axis as default
        self.image_index = [data.shape[0] // 2, data.shape[1] // 2, data.shape[2] // 2]
        self.last_clicked = 2  # Default movement in the Axial plane
        self.last_keypress_time = 0
        self.keypress_interval = 0.2 # Delay for preventing excessive key press input

        # Initial display and title setup
        self.update_images()

    def update_on_click(self, click):
        if click.inaxes == self.axes[0]:  # Sagittal slice clicked
            self.image_index[1] = int(click.xdata) # Change plane in Coronal
            self.image_index[2] = int(click.ydata) # Change plane in Axial
            self.last_clicked = 0 # Changes which view is changed upon an arrow key press
        elif click.inaxes == self.axes[1]:  # Coronal slice clicked
            self.image_index[0] = int(click.xdata) # Change plane is Sagittal
            self.image_index[2] = int(click.ydata) # Change plane is Axial
            self.last_clicked = 1 # Changes which view is changed upon an arrow key press
        elif click.inaxes == self.axes[2]: # Axial slice clicked
            self.image_index[0] = int(click.xdata) # Change plane in Sagittal
            self.image_index[1] = int(click.ydata) # Change plane in Coronal
            self.last_clicked = 2 # Changes which view is changed upon an arrow key press
        self.update_images()

    def update_on_key(self, event):
        # Drop out of update_on_key() if keys are pressed too rapidly
        current_time = time.time() 
        if current_time - self.last_keypress_time < self.keypress_interval:
            return
        self.last_keypress_time = current_time
        
        
        key_direction = (event.key, self.last_clicked) # Contains which key was last pressed and which view was last clicked
        if key_direction in DIRECTION_MAP: # If a valid direction within the dictionary
            idx, op = DIRECTION_MAP[key_direction] # idx contains which image needs updating, op contains the direction being changed
            self.image_index[idx] = max(0, min(self.image_index[idx] + op, self.data.shape[idx] - 1)) #update the image index for the relevant image
            self.update_images()# Update images

    def update_images(self): # Update all images - Could be made more efficient if only relevant images are updates
        self.axes[0].imshow(self.data[self.image_index[0], :, :].T, cmap='gray', origin='lower', aspect=self.dims[3]/self.dims[2])
        self.axes[1].imshow(self.data[:, self.image_index[1], :].T, cmap='gray', origin='lower', aspect=self.dims[3]/self.dims[1])
        self.axes[2].imshow(self.data[:, :, self.image_index[2]].T, cmap='gray', origin='lower', aspect=self.dims[2]/self.dims[1])
        self.update_titles()

    def update_titles(self):
        self.axes[0].set_title(f'Sagittal [{self.image_index[0]}]')
        self.axes[1].set_title(f'Coronal [{self.image_index[1]}]')
        self.axes[2].set_title(f'Axial [{self.image_index[2]}]')
        plt.draw()

def preview_nifti(filename):
    nii = nib.load(filename) # Load in NIfTI
    data = nii.get_fdata() # Extract main image data
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5)) # Define image area
    dims = nii.header['pixdim'] # Extract dimentions of pixels
    
    viewer = Interact(data, dims, axes) # Get initial values from Interact class
    
    # Display area settings
    plt.suptitle(f"{os.path.basename(filename)}")
    plt.tight_layout()
    axes[0].axis('off')
    axes[1].axis('off')
    axes[2].axis('off')

    # Update viewer values upon a click or button press
    fig.canvas.mpl_connect('button_press_event', viewer.update_on_click)
    fig.canvas.mpl_connect('key_press_event', viewer.update_on_key)
    plt.show()

# Dictionary loaded as global to prevent it being loaded every time the user interacts with the images
DIRECTION_MAP = {
    ('left', 0): (1, -1),
    ('left', 1): (0, -1),
    ('left', 2): (0, -1),
    ('right', 0): (1, 1),
    ('right', 1): (0, 1),
    ('right', 2): (0, 1),
    ('up', 0): (2, 1),
    ('up', 1): (2, 1),
    ('up', 2): (1, 1),
    ('down', 0): (2, -1),
    ('down', 1): (2, -1),
    ('down', 2): (1, -1),
}

# Check a file name was provided by command line arg
if len(sys.argv) > 1:
    filename = sys.argv[1]
    try:
        preview_nifti(filename) # Preview the NIfTI file
    except Exception as e:
        input(f"Error loading NIfTI file: {e}\n") # Error incase the preview goes wrong
else:
    input("No File Specified")
