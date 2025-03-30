import re
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment

def readFLOW(filename):
    # File path
    #file_path = "backend/unit.FLOW"
    file_path = filename

    # Pattern to match frame header
    frame_pattern = re.compile(r"Frame (\d+):")
    # Initialize list to store frame data
    frames_data = []

    # Open and read the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Variables to hold frame data
    frame_data = {}

    # Loop through each line
    for line in lines:
        line = line.strip()

        # Check for a new frame
        frame_match = frame_pattern.match(line)
        if frame_match:
            # Save the previous frame data if available
            if frame_data:
                frames_data.append(frame_data)
            
            # Start a new frame
            frame_data = {"Frame": int(frame_match.group(1))}
            continue

        # Parse key-value pairs
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            # Try to convert value to float if possible
            try:
                value = float(value)
            except ValueError:
                pass
            
            # Store key-value pair
            frame_data[key] = value

    # Append the last frame data
    if frame_data:
        frames_data.append(frame_data)

    # Print the parsed data
    num_frames = int(frames_data[0]['Number of frames'])
    output_amp = []
    amplitude = []
    f_slope = []
    time_0 = []
    for frame in frames_data[1:]:  # Show first 5 frames for testing
        # add min, mult by max, add min
        sc_amp = frame['Amplitude'] * 32767
        amplitude.append(sc_amp)
        f_slope.append(frame['Frame Slope'])
        time_0.append(frame['Times 0'])
        tsc = frame['Times 0'] * 40
        chunks = int(800/(tsc+1))
        for i in range(chunks):
            unit = sc_amp
            for j in range(int(tsc)):
                output_amp.append(unit/(j+1))
    print("Number of amps:", len(output_amp))   
    #print(amplitude)         

    sample_rate = 8000

    # Save as a WAV file
    wav_file_path = "output_waveform.wav"
    write(wav_file_path, sample_rate, np.int16(output_amp))

    # Convert WAV to MP3
    mp3_file_path = "output_waveform.mp3"
    audio = AudioSegment.from_wav(wav_file_path)
    audio.export(mp3_file_path, format="mp3")

    print(f"MP3 file saved as '{mp3_file_path}'!")