import numpy as np

def w_FLOW(filename, frames):
    num_frames = len(frames)

    with open(str(filename) + ".FLOW", 'w') as file:
         # Write header metadata
        file.write("WAVEFORM FLOW\n")
        file.write(f"Number of frames: {num_frames}\n")
        u = 0
        for frame in frames:
            # Write frame metadata
            file.write(f"Frame {u}:\n")
            points = [sample.points for sample in frame.samples]
            combined_array = np.concatenate(points, axis=0)
            #file.write(f"  Samples: ")
            # write all samples to file
            #file.write(f"[")
            #rr = 1
            #for pair in combined_array:
            #    if rr == len(combined_array):
            #        file.write(f"{pair}")
            #    else:
            #        file.write(f"{pair}, ")
            #    rr += 1
            #file.write(f"]")
            file.write(f"\n  Amplitude: {frame.amplitude}\n")
            file.write(f"  Left/Right: {frame.left_right}\n")
            file.write(f"  Inc/Dec: {frame.inc_dec}\n")
            file.write(f"  Times 0: {frame.times_0}\n")
            file.write(f"  Flat/Spike: {frame.flat_spike}\n")
            file.write(f"  Slope: {frame.slope}\n")
            file.write(f"  Count per Frame: {frame.count_per_frame}\n")
            file.write(f"  Frame Slope: {frame.frame_slope}\n")
            file.write("\n")
            u += 1
