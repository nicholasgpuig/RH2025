import cairo
import os
from PIL import Image
import random
import math
import numpy as np
#import cairosvg

<<<<<<< HEAD

def frame_viz(frames, plt):
=======
def frame_viz(frames, coors):
>>>>>>> 422631397da581b70082ffb415e46a3506a53077
    # Canvas dimensions
    width, height = 250, 250

    # Create surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    cnt = 0
    for frame in frames:
<<<<<<< HEAD
        plt.savefig(f"test.png{cnt}", format="png", dpi=100)
        image_surface = cairo.ImageSurface.create_from_png(f"test.png{cnt}")
        pattern = cairo.SurfacePattern(image_surface)
        pattern.set_extend(cairo.EXTEND_REPEAT)
        # draw background
        # gradient = cairo.LinearGradient(0, 0, 0, height)
        # gradient.add_color_stop_rgb(0, 0, 0.7, 0.6)  # Top teal
        # gradient.add_color_stop_rgb(1, 0, 0.4, 0.7)  # Bottom blue
        context.set_source(pattern)
=======
        # Create the gradient
        gradient = cairo.LinearGradient(0, 0, 0, height)

        # Add color stops for the 3 colors
        gradient.add_color_stop_rgb(random.uniform(0, 0.33), coors[0][0], coors[0][1], coors[0][2])  # First color (top)
        gradient.add_color_stop_rgb(random.uniform(0.33, 0.66), coors[1][0], coors[1][1], coors[1][2])  # Second color (middle)
        gradient.add_color_stop_rgb(random.uniform(0.66, 1), coors[2][0], coors[2][1], coors[2][2])  # Third color (bottom)

        # Apply the gradient to the context and fill the rectangle
>>>>>>> 422631397da581b70082ffb415e46a3506a53077
        context.rectangle(0, 0, width, height)
        context.fill()

        ' CURVE PEAK WIDTH '
        # Range: [0.01, 0.11]   - Slope
        curve_peak_width = (1-frame.slope) * 0.1 + 0.01

        ' CURVE AMPLITUDE '
        # Range: [1, 21]    - Count perFrame
        curve_amplitude = frame.count_per_frame * 20 + 1

        ' CURVE SPACING '
        # Range: [20, 30]
        curve_spaceing = ((frame.left_right + 1) / 2) * 10 + 20

        ' CURVE THICKNESS '
        # Range: [1, 6] - Frame Slope
        curve_thickness = frame.slope * 5 + 1

        ' LINE COUNT '
        # Range: [10, 60]   - Inc/Dec
        line_count = int(frame.inc_dec * 50 + 10)

        ' LINE AMPLITUDE '
        # Range: [1,21]
        line_amplitude = (frame.amplitude * 20) + 1

        ' LINE SPACING '
        # Range: [1,21]  - Flat/Spike
        line_spacing = int(frame.flat_spike * 20 + 1)

        ' LINE THICKNESS'
        # Range: [1, 5] - Times 0
        line_thickness = frame.times_0 * 4 + 1

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
        surface.write_to_png(f"backend/l1_img/frame{cnt}.png")
        #print("Image created and saved as 'generated_lines.png'")
        cnt += 1


def make_gif(dir, output_gif, fps):
    # Define the directory containing the PNG images
    png_folder = dir
    #fps = 10  # Set the desired frames per second

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
