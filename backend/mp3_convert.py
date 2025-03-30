import subprocess
import ffmpeg
import numpy as np

# importing packages
from pytubefix import YouTube
import os
from youtube_search import YoutubeSearch

def scrape(song):
  # handle output file if exists
  output_file = 'backend/scraped.mp3'
  try:
      os.remove(output_file)
      print(f"File {output_file} deleted successfully.")
  except FileNotFoundError:
      print(f"Error: File {output_file} not found.")
  except Exception as e:
        print(f"An error occurred: {e}")

  # url input from user
  yt = YouTube(str(song))
  video = yt.streams.filter(only_audio=True).first()

  # Save file
  destination = 'backend/'
  out_file = video.download(output_path=destination, filename='scraped.mp3')
  base, ext = os.path.splitext(out_file)
  new_file = base + '.mp3'
  os.rename(out_file, new_file)

  # result of success
  print(yt.title + " has been successfully downloaded.")

def getYouTube(song, artist):
  results = YoutubeSearch(str(song) + " " + str(artist), max_results=1).to_dict()
  for v in results:
    scrape('https://www.youtube.com' + v['url_suffix'])

def change_sample_rate(input_file, output_file, sample_rate):
    try:
      subprocess.run(['ffmpeg', '-i', input_file, '-ar', str(sample_rate), output_file], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
      print(f"Successfully converted {input_file} to {output_file} with sample rate {sample_rate} Hz")
    except subprocess.CalledProcessError as e:
      print(f"Error during conversion: {e}")
    except FileNotFoundError:
      print("ffmpeg is not installed or not in your system's PATH.")

def decode_output(input_file):
  # Use ffmpeg to decode MP3 to raw PCM data (stereo, 44.1 kHz, 16-bit)
  try:
      process = (
          ffmpeg.input(input_file)
          .output('pipe:', format='s16le', acodec='pcm_s16le', ac=2, ar=8000)  # Stereo, 44.1kHz, 16-bit PCM
          .run(capture_stdout=True, capture_stderr=subprocess.DEVNULL)
      )

      # Convert raw audio data to a NumPy array (int16 format)
      audio_data = np.frombuffer(process[0], np.int16)

      # Reshape to (num_samples, 2) where 2 represents [Left, Right] channels
      audio_data = audio_data.reshape(-1, 2)

      #print(f"Audio shape: {audio_data.shape}")  # (num_samples, 2)
      #print(audio_data[:10])  # Print first 10 samples (L, R)
      return audio_data
  except ffmpeg.Error as e:
      print(f"Error: {e.stderr.decode()}")


