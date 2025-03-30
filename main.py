from backend.mp3_convert import change_sample_rate, decode_output, getYouTube
from backend.layer1 import l1_collect
from backend.l1_viz import frame_viz, make_gif
from backend.to_FLOW import w_FLOW
from backend.from_FLOW import readFLOW
from layer_2 import get_top_tags, client
import os

i_song = "pink diamond"
i_artist = "charli xcx"

# Function to convert hex to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

if __name__ == '__main__':
    #input_mp3_file = 'backend/input4.mp3'  
    output_file = 'backend/output.mp3'
    new_sample_rate = 8000  # Lowest supported sample rateL 8000 Hz
    img_dir = "backend/l1_img"  # Replace with your folder path

    # get mp3 file
    getYouTube(i_song, i_artist)
    input_mp3_file = 'backend/scraped.mp3'  # Update this path if needed

    # handle output file if exists
    try:
        os.remove(output_file)
        print(f"File {output_file} deleted successfully.")
    except FileNotFoundError:
        print(f"Error: File {output_file} not found.")
    except Exception as e:
         print(f"An error occurred: {e}")

    print("All frame images have been deleted.")

    change_sample_rate(input_mp3_file, output_file, new_sample_rate)
    audio_data = decode_output(output_file)

    frames = l1_collect(audio_data)
    w_FLOW("backend/unit", frames)  # Save the data to a .FLOW file
    readFLOW("backend/unit.FLOW")

    tags = get_top_tags(i_song, i_artist)
    colors = client(i_song, i_artist)
    print(colors)

    # Remove backticks and clean the string
    cleaned_colors = [color.strip('`') for color in colors]

    # Convert to RGB correctly
    rgb_colors = [
        tuple(int(cleaned_color[i:i+2], 16) / 255 for i in (1, 3, 5))
        for cleaned_color in cleaned_colors
    ]

    print(rgb_colors)

    frame_viz(frames, rgb_colors)
    make_gif(img_dir, "backend/l1_img.gif", 10)     # 10 FPS - only change for debug