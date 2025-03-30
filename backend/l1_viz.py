import cairo
import os
from PIL import Image
import random
import math
import numpy as np


def frame_viz(frames):
    # Canvas dimensions
    width, height = 250, 250

    # Create surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    # draw background
    gradient = cairo.LinearGradient(0, 0, 0, height)
    gradient.add_color_stop_rgb(0, 0, 0.7, 0.6)  # Top teal
    gradient.add_color_stop_rgb(1, 0, 0.4, 0.7)  # Bottom blue
    context.rectangle(0, 0, width, height)
    context.set_source(gradient)
    context.fill()

    ' CURVE PEAK WIDTH '
    # Range: 
    curve_peak_width = 0.1

    ' CURVE AMPLITUDE '
    # Range: 
    curve_amplitude = 20

    ' CURVE SPACING '
    # Range: 
    curve_spaceing = 20

    ' CURVE THICKNESS '
    # Range: 
    curve_thickness = 4

    ' LINE COUNT '
    # Range: 
    line_count = 50

    ' LINE AMPLITUDE '
    # Range: 
    line_amplitude = 10

    ' LINE SPACING '
    # Range: 
    line_spacing = 5

    ' LINE THICKNESS'
    # Range: 
    line_thickness = 2

    # Draw wavy lines with random vertical lines
    num_lines = 20  # Number of wavy lines
    wavvy = curve_peak_width
    for i in range(num_lines):
        y = height / 2 + i * curve_spaceing - (num_lines * curve_spaceing / 3)
        points = [(x, y + curve_amplitude * np.sin(wavvy * x + i)) for x in range(0, width+5, 5)]
        
        # Draw the wavy line
        context.set_source_rgb(1, 1, 0.8)  # Light yellowish line
        context.set_line_width(curve_thickness)
        context.move_to(*points[0])
        for point in points[1:]:
            context.line_to(*point)
        context.stroke()

        # Draw random vertical lines intersecting the waves
        context.set_line_width(line_thickness)
        for _ in range(line_count):
            x_pos = random.choice(range(0, width, line_spacing))
            context.move_to(x_pos, y - line_amplitude)
            context.line_to(x_pos, y + line_amplitude)
            context.stroke()

    # Save the final image
    surface.write_to_png("generated_lines.png")
    print("Image created and saved as 'generated_lines.png'")


def make_gif(dir, output_gif):
    # Define the directory containing the PNG images
    png_folder = dir
    fps = 10  # Set the desired frames per second

    # Get the list of PNG files in the folder and sort them
    png_files = sorted([f for f in os.listdir(png_folder) if f.endswith('.png')])

    # Load the images into a list
    images = []
    for png_file in png_files:
        image_path = os.path.join(png_folder, png_file)
        img = Image.open(image_path)
        images.append(img)

    # Convert the list of images to a GIF with the specified FPS
    images[0].save(output_gif, save_all=True, append_images=images[1:], optimize=True, duration=1000/fps, loop=0)

    print(f"GIF saved as {output_gif} with {fps} FPS.")

    # clear frame image folder
    img_dir = "backend/l1_img"  # Replace with your folder path
    # Loop through the files in the directory
    for filename in os.listdir(img_dir):
        file_path = os.path.join(img_dir, filename)
        # Check if it's a file (not a subdirectory)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Remove the file
