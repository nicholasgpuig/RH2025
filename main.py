from backend.mp3_convert import change_sample_rate, decode_output, getYouTube
from backend.layer1 import l1_collect
from backend.l1_viz import frame_viz, make_gif
from backend.to_FLOW import w_FLOW
import os

i_song = "say it"
i_artist = "2hollis"

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
    w_FLOW("test_outy", frames)  # Save the data to a .FLOW file

    frame_viz(frames)
    make_gif(img_dir, "backend/l1_img.gif", 10)     # 10 FPS - only change for debug