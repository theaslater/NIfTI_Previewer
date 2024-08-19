#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:47:17 2024

@author: thea
"""

import sys
import os
import nibabel as nib
import matplotlib.pyplot as plt

class Interact:
    def __init__(self, data, dims, axes):
        self.data = data
        self.dims = dims
        self.axes = axes
        self.sagittal_index = data.shape[0] // 2
        self.coronal_index = data.shape[1] // 2
        self.axial_index = data.shape[2] // 2

    def update_on_click(self, click):
        if click.inaxes == self.axes[0]:  # Sagittal slice clicked
            self.coronal_index = int(click.xdata)
            self.axial_index=int(click.ydata)
        elif click.inaxes == self.axes[1]:  # Coronal slice clicked
            self.sagittal_index = int(click.xdata)
            self.axial_index=int(click.ydata)
        elif click.inaxes == self.axes[2]:  # Axial slice clicked
            self.sagittal_index=int(click.xdata)    
            self.coronal_index = int(click.ydata)
        # Update the images
        self.axes[0].imshow(self.data[self.sagittal_index, :, :].T, cmap='gray', origin='lower', aspect=self.dims[3]/self.dims[1])
        self.axes[1].imshow(self.data[:, self.coronal_index, :].T, cmap='gray', origin='lower', aspect=self.dims[3]/self.dims[2])
        self.axes[2].imshow(self.data[:, :, self.axial_index].T, cmap='gray', origin='lower', aspect=self.dims[1]/self.dims[2]) # If image is ever squashed, reverse this first!
        plt.draw()

def preview_nifti(filename):
    nii = nib.load(filename)
    data = nii.get_fdata()
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    dims = nii.header['pixdim']
    
    print(nii.header)
    viewer = Interact(data, dims, axes)
    
    # Initial display
    axes[0].imshow(data[viewer.sagittal_index, :, :].T, cmap='gray', origin='lower', aspect=dims[3]/dims[1])
    axes[1].imshow(data[:, viewer.coronal_index, :].T, cmap='gray', origin='lower', aspect=dims[3]/dims[2])
    axes[2].imshow(data[:, :, viewer.axial_index].T, cmap='gray', origin='lower', aspect=dims[1]/dims[2])
    
    plt.suptitle(f"{os.path.basename(filename)}")
    plt.tight_layout()
    
    # Turn off axes and set titles
    axes[0].axis('off')
    axes[0].set_title('Sagittal')
    axes[1].axis('off')
    axes[1].set_title('Coronal')
    axes[2].axis('off')
    axes[2].set_title('Axial')
    # Connect the click event to the viewer's update method
    fig.canvas.mpl_connect('button_press_event', viewer.update_on_click)
    
    plt.show()


if len(sys.argv) > 1:
    filename = sys.argv[1]
    try:
        preview_nifti(filename)

    except Exception as e:
        input(f"Error loading NIfTI file: {e}\n")
else:
    with open("/home/thea/SCRIPTS/test_log.txt", "a") as log_file:
        input("No file specified.\n")
