import ffmpeg
import numpy as np
import matplotlib.pyplot as plt

timeframe = 0.01  # 10ms

class Sample:
    def __init__(self, time, points):
        self.time = time
        self.points = points

class Frame:
    def __init__(self, samples):
        self.samples = samples

def l1_collect(audio_data):
    # break up audio data into chunks of 80 samples (each sample = 0.01s)
      # pad the audio data to ensure it is divisible by 80
    num_samples = len(audio_data)
    print("datapoints: ",num_samples)

    # Create an array breaking down audio_data into 80 sample chunks
    num_chunks = num_samples // 80
    samples = []
    for i in range(num_chunks):
        start = i * 80
        end = start + 80
        if(end > num_samples):  # Pad the last chunk if necessary
            # Pad the chunk with zeros to make it 80 samples long
            end = num_samples
            chunk = audio_data[start:end]
            chunk = np.pad(chunk, ((0, 80 - len(chunk)), (0, 0)), mode='constant')
        else:
            chunk = audio_data[start:end]
        # Create a Sample object for each chunk
        sample = Sample(timeframe, chunk)
        # Append the sample to a list of samples
        samples.append(sample)
    print("total samples: ", len(samples))

    # Create a Frame for every 10 samples
    frames = []
    for i in range(0, len(samples), 10):
        frame_samples = samples[i:i + 10]
        frame = Frame(frame_samples)
        frames.append(frame)
    print("total frames: ", len(frames))

    # Collect data for each sample
    for sample in samples:
        setattr(sample, 'amplitude', l1_amplitude(sample))
        setattr(sample, 'left_right', l1_left_right(sample))
        setattr(sample, 'inc_dec', l1_inc_dec(sample))
        setattr(sample, 'times_0', l1_times_0(sample))
        setattr(sample, 'flat_spike', l1_flat_spike(sample))
        setattr(sample, 'slope', l1_slope(sample))

    #print("sample 11 amplitude: ", samples[10].amplitude)
    #print("frame 2 sample 1 amplitude: ", frames[1].samples[0].amplitude)

    for frame in frames:
        setattr(frame, 'count_per_frame', l1_countperframe(frame))
        setattr(frame, 'frame_slope', l1_frame_slope(frame))
        setattr(frame, 'amplitude', max([sample.amplitude for sample in frame.samples]))
        setattr(frame, 'left_right', max([sample.left_right for sample in frame.samples]))
        setattr(frame, 'inc_dec', max([sample.inc_dec for sample in frame.samples]))
        setattr(frame, 'times_0', max([sample.times_0 for sample in frame.samples]))
        setattr(frame, 'flat_spike', max([sample.flat_spike for sample in frame.samples]))
        setattr(frame, 'slope', max([sample.slope for sample in frame.samples]))

    #plots(frames)

    # Normalize the data for each frame
    for frame in frames:
        frame.amplitude = (frame.amplitude - np.min([f.amplitude for f in frames])) / (np.max([f.amplitude for f in frames]) - np.min([f.amplitude for f in frames]))
        frame.left_right = (frame.left_right - np.min([f.left_right for f in frames])) / (np.max([f.left_right for f in frames]) - np.min([f.left_right for f in frames]))
        # Scale l/r mean to be 0.5
        frame.left_right = (frame.left_right - 0.5) / (1 - 0.5)
        frame.inc_dec = (frame.inc_dec - np.min([f.inc_dec for f in frames])) / (np.max([f.inc_dec for f in frames]) - np.min([f.inc_dec for f in frames]))
        frame.times_0 = (frame.times_0 - np.min([f.times_0 for f in frames])) / (np.max([f.times_0 for f in frames]) - np.min([f.times_0 for f in frames]))
        frame.flat_spike = (frame.flat_spike - np.min([f.flat_spike for f in frames])) / (np.max([f.flat_spike for f in frames]) - np.min([f.flat_spike for f in frames]))
        frame.slope = (frame.slope - np.min([f.slope for f in frames])) / (np.max([f.slope for f in frames]) - np.min([f.slope for f in frames]))
        frame.count_per_frame = (frame.count_per_frame - np.min([f.count_per_frame for f in frames])) / (np.max([f.count_per_frame for f in frames]) - np.min([f.count_per_frame for f in frames]))
        frame.frame_slope = (frame.frame_slope - np.min([f.frame_slope for f in frames])) / (np.max([f.frame_slope for f in frames]) - np.min([f.frame_slope for f in frames]))
        
    #plots(frames)
    return frames


"# --- LAYER 1 SAMPLE-PARSING FUNCTIONS --- #"

# TIME-INDEPENDENT FUNCTIONS
def l1_amplitude(sample):
    # Calculate the largest amplitude of the sample
    left_channel = sample.points[:, 0]
    right_channel = sample.points[:, 1]
    l_max = np.max(np.abs(left_channel))
    r_max = np.max(np.abs(right_channel))
    if(l_max > r_max):
        return l_max
    else:
        return r_max

def l1_left_right(sample):
    # Calculate the largest ratio of left to right channel
    left_channel = sample.points[:, 0]
    right_channel = sample.points[:, 1]
    l_mean = np.mean(left_channel)
    r_mean = np.mean(right_channel)
    if(r_mean == 0):
        return 1  # Avoid division by zero
    else:
        return l_mean / r_mean
    
def l1_inc_dec(sample):
    # Calculate biggest absolute value of difference between points in each channel
    left_channel = sample.points[:, 0]
    right_channel = sample.points[:, 1]
    l_max = np.max(np.abs(np.diff(left_channel)))
    r_max = np.max(np.abs(np.diff(right_channel)))
    if(l_max > r_max):
        return l_max
    else:
        return r_max

# TIME-DEPENDENT FUNCTIONS
def l1_times_0(sample):
    # Calculate the number of times the signal crosses zero in each channel
    left_channel = sample.points[:, 0]
    right_channel = sample.points[:, 1]
    l_crossings = np.sum(np.diff(np.sign(left_channel)) != 0)
    r_crossings = np.sum(np.diff(np.sign(right_channel)) != 0)
    if(l_crossings > r_crossings):
        return l_crossings
    else:
        return r_crossings

def l1_flat_spike(sample):
    # Calculate the number of times the signal is flat or spiked in each channel
    left_channel = sample.points[:, 0]
    right_channel = sample.points[:, 1]
    l_spk_cnt = 0
    r_spk_cnt = 0
    for i in range(len(left_channel)):
        if(i != len(left_channel) - 1):
            if(left_channel[i+1] != 0):
                if(left_channel[i]/(left_channel[i+1]) > 0.9):
                    l_spk_cnt += 1
    for i in range(len(right_channel)):
        if(i != len(right_channel) - 1):
            if(right_channel[i+1] != 0):
                if(right_channel[i]/right_channel[i+1] > 0.9):
                    r_spk_cnt += 1

    return l_spk_cnt if l_spk_cnt > r_spk_cnt else r_spk_cnt

def l1_slope(sample):
    # Calculate the signed slope of the signal in each channel
    left_channel = sample.points[:, 0]
    right_channel = sample.points[:, 1]
    l_slope = np.mean(np.diff(left_channel))
    r_slope = np.mean(np.diff(right_channel))
    if(abs(l_slope) > abs(r_slope)):
        return l_slope
    else:
        return r_slope

# Based on the time frame, calculate the spacing between samples
def l1_countperframe(frame):
    # Calculate number of similar average sample amplitudes in the frame
    l_amps = []
    r_amps = []
    for sample in frame.samples:
        l_amps.append(sample.amplitude)
        r_amps.append(sample.amplitude)
    l_avg = np.mean(l_amps)
    r_avg = np.mean(r_amps)
    l_count = np.sum(np.abs(l_amps - l_avg) < 0.1*l_avg)  # Flat threshold
    r_count = np.sum(np.abs(r_amps - r_avg) < 0.1*r_avg)  # Flat threshold
    if(l_count > r_count):
        return l_count
    else:
        return r_count
    
def l1_frame_slope(frame):
    # Calculate the signed slope of the signal in each channel
    left = []
    right = []
    for sample in frame.samples:
        left.append(sample.points[:, 0])
        right.append(sample.points[:, 1])
    # calculate slope of left and right channels
    left = np.array(left)
    right = np.array(right)
    l_slope = np.mean(np.diff(left))
    r_slope = np.mean(np.diff(right))
    if(abs(l_slope) > abs(r_slope)):
        return l_slope
    else:
        return r_slope

        
def plots(frames):
    plt.figure(figsize=(15, 10))

    # First subplot (1st row, 1st column)
    plt.subplot(4, 2, 1)
    plt.plot([frame.amplitude for frame in frames])
    plt.title('Amplitude')
    plt.ylabel('Amplitude Value')

    # Second subplot (1st row, 2nd column)
    plt.subplot(4, 2, 2)
    plt.plot([frame.left_right for frame in frames])
    plt.title('Left-Right')
    plt.ylabel('Left-Right Value')

    # Third subplot (2nd row, 1st column)
    plt.subplot(4, 2, 3)
    plt.plot([frame.inc_dec for frame in frames])
    plt.title('Inc-Dec')
    plt.ylabel('Inc-Dec Value')

    # Fourth subplot (2nd row, 2nd column)
    plt.subplot(4, 2, 4)
    plt.plot([frame.times_0 for frame in frames])
    plt.title('Times 0')
    plt.ylabel('Times 0 Value')

    # Fifth subplot (3rd row, 1st column)
    plt.subplot(4, 2, 5)
    plt.plot([frame.flat_spike for frame in frames])
    plt.title('Flat Spike')
    plt.ylabel('Flat Spike Value')

    # Sixth subplot (3rd row, 2nd column)
    plt.subplot(4, 2, 6)
    plt.plot([frame.slope for frame in frames])
    plt.title('Slope')
    plt.ylabel('Slope Value')

    # Seventh subplot (4th row, 1st column)
    plt.subplot(4, 2, 7)
    plt.plot([frame.count_per_frame for frame in frames])
    plt.title('Count per Frame')
    plt.ylabel('Count Value')

    # Eighth subplot (4th row, 2nd column)
    plt.subplot(4, 2, 8)
    plt.plot([frame.frame_slope for frame in frames])
    plt.title('Frame Slope')
    plt.ylabel('Frame Slope Value')

    # Apply tight_layout to avoid overlapping labels and titles
    plt.tight_layout()

    # Show the plots
    plt.show()