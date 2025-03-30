import cairo
import os
from PIL import Image
import random
import math
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
#import cairosvg

def frame_viz(frames, coors):
    # Canvas dimensions
    width, height = 250, 250

    # Create surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    cnt = 0
    for frame in frames:

        # Set the random seed based on L/R
        random.seed(frame.left_right)
        # Generate 800 unique random (x, y) pairs
        unique_pairs = set()

        # Keep generating until we have 800 unique pairs
        while len(unique_pairs) < 800:
            x, y = random.randint(1, 248), random.randint(1, 248)
            unique_pairs.add((x, y))

        # Convert the set to a list for easier access
        pairs = list(unique_pairs)

        # Create the gradient
        gradient = cairo.LinearGradient(0, 0, 0, height)

        # Add color stops for the 3 colors
        gradient.add_color_stop_rgb(random.uniform(0, 0.33), coors[0][0], coors[0][1], coors[0][2])  # First color (top)
        gradient.add_color_stop_rgb(random.uniform(0.33, 0.66), coors[1][0], coors[1][1], coors[1][2])  # Second color (middle)
        gradient.add_color_stop_rgb(random.uniform(0.66, 1), coors[2][0], coors[2][1], coors[2][2])  # Third color (bottom)

        # Apply the gradient to the context and fill the rectangle
        context.rectangle(0, 0, width, height)
        context.set_source(gradient)
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

        cnn = 0
        points = [sample.points for sample in frame.samples]
        combined_array = np.concatenate(points, axis=0)
        #print(len(combined_array))
        while cnn < len(combined_array):
            p = pairs[cnn]
            nx_pos = p[0]
            ny_pos = p[1]
            hex_color = combined_array[cnn][0]  # x = left position (can rescale later with ratio)
            #print(hex_color)

            # Convert hex to RGB values between 0 and 1
            r = (hex_color& 0xFF0000 >> 16) / 255.0
            g = (hex_color& 0x00FF00 >> 8) / 255.0
            b = (hex_color& 0x0000FF) / 255.0

            if 0 <= nx_pos < width and 0 <= ny_pos < height:
                context.set_source_rgb(r, g, b)  # White color
                context.rectangle(nx_pos, ny_pos, 1, 1)  # Draw pixel
                context.fill()

           # if(cnn == 100 and cnt == 10):
               # print(nx_pos, ny_pos)
            #if(cnn == 100 and cnt == 10):
                #print(r,g,b)
            #if(cnn == 100 and cnt == 10):
                #print(hex_color)

            cnn += 1

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

def from_gif(frames, filename, fps):
    amplitudes_L = []
    amplitudes_R = []

    # Load the GIF
    gif_path = filename
    gif = Image.open(gif_path)

    # Get the number of frames
    num_frames = gif.n_frames
    print(f"Total Frames: {num_frames}")

    # Loop through each frame
    f_idx = 0
    for frame_number in range(num_frames):
        # Select the current frame
        gif.seek(frame_number)

        # Convert the frame to RGB mode
        rgb_frame = gif.convert("RGB")

        frame = frames[f_idx]
        f_idx += 1
        
        # Set the random seed based on L/R
        random.seed(frame.left_right)
        # Generate 800 unique random (x, y) pairs
        unique_pairs = set()

        # Keep generating until we have 800 unique pairs
        while len(unique_pairs) < 800:
            x, y = random.randint(1, 248), random.randint(1, 248)
            unique_pairs.add((x, y))

        # Convert the set to a list for easier access
        pairs = list(unique_pairs)

        cnn = 0
        while(cnn < 800):
            nx_pos, ny_pos = pairs[cnn]
            #if(cnn == 100 and f_idx == 11):
                #print(nx_pos, ny_pos)
            r, g, b = rgb_frame.getpixel((nx_pos, ny_pos))
            #if(cnn == 100 and f_idx == 11):
                #print(r,g,b)

            # Get amplitude for L/R channels
            amp_x = (r + g + b) / (3 * 255)  # Normalize RGB to range [0, 1]
            amp_y = amp_x / (frame.left_right + 1e-6)  # Avoid division by zero

            #if(cnn == 100 and f_idx == 11):
                #print(amp_x, amp_y)

            amplitudes_L.append(amp_x)
            amplitudes_R.append(amp_y)

            cnn += 1      

    # TODO: Convert amplitudes to 8000 Hz mp3
    # Ensure both channels have the same length

    # Convert to NumPy arrays and scale to 16-bit PCM range
    amplitudes_L = np.array(amplitudes_L) * 32767
    amplitudes_R = np.array(amplitudes_R) * 32767

    # Interleave L and R for stereo format
    stereo_audio = np.column_stack((amplitudes_L, amplitudes_R)).astype(np.int16)

    # Save as a stereo WAV file
    wav_file_path = "BEANS.wav"
    sample_rate = 8000  # 8 kHz sample rate
    write(wav_file_path, sample_rate, stereo_audio)

    # Convert WAV to MP3
    mp3_file_path = "BEANS.mp3"
    audio = AudioSegment.from_wav(wav_file_path)
    audio.export(mp3_file_path, format="mp3")

    print(f"MP3 file saved as '{mp3_file_path}'!")