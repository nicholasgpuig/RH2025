import re
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment

class Frame:
    def __init__(self, samples):
        self.samples = samples

def readFLOW(filename, convert):
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
    frames = []

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

    b_output = []

    for frame in frames_data[1:]:  # Show first 5 frames for testing
        uframe = Frame(0) # NULL
        
        # INIT ACTUALLY IMPORTANT DATA
        setattr(uframe, 'count_per_frame', frame['Count per Frame'])
        setattr(uframe, 'frame_slope', frame['Frame Slope'])
        setattr(uframe, 'amplitude', frame['Amplitude'])
        setattr(uframe, 'left_right', frame['Left/Right'])
        setattr(uframe, 'inc_dec', frame['Inc/Dec'])
        setattr(uframe, 'times_0', frame['Times 0'])
        setattr(uframe, 'flat_spike', frame['Flat/Spike'])
        setattr(uframe, 'slope', frame['Slope'])
        frames.append(uframe)

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

    if convert:
        sample_rate = 8000

        # Save as a WAV file
        wav_file_path = "screams_of_the_damned.wav"
        write(wav_file_path, sample_rate, np.int16(output_amp))

        # Convert WAV to MP3
        mp3_file_path = "screams_of_the_damned.mp3"
        audio = AudioSegment.from_wav(wav_file_path)
        audio.export(mp3_file_path, format="mp3")

        print(f"MP3 file saved as '{mp3_file_path}'!")

    return frames