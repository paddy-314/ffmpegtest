from moviepy.editor import VideoFileClip
from PIL import Image
import pytesseract
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

work_path = os.path.dirname(os.path.realpath(__file__))
results_file = os.path.join(work_path, "results.txt")

FPS = 24
PROTOCOL = 'webrtc'

def extract_frames(video_path, fps=FPS):
    clip = VideoFileClip(video_path)
    frames_dir = os.path.join(work_path, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    for i, frame in enumerate(clip.iter_frames(fps=fps)):
        frame_img = Image.fromarray(frame)
        frame_path = os.path.join(frames_dir, f"frame_{i:04d}.jpg")
        frame_img.save(frame_path)
    
    return frames_dir

def extract_timestamps_from_frame(frame_path):
    frame_img = Image.open(frame_path)    
    string = pytesseract.image_to_string(frame_img,config= '--psm 6 digits -c tessedit_char_whitelist=0123456789.:')
    timestamp_regex = r'\d{2}:\d{2}:\d{2}\.\d{3}'
    timestamps = re.findall(timestamp_regex, string)
    return timestamps

def print_diagram_timed(filename):
    with open(filename, 'r') as f:
        # Es wird angenommen, dass die Daten numerisch sind und konvertiert werden können.
        # Beachten Sie, dass für eine korrekte Konvertierung ggf. zusätzliche Schritte notwendig sein könnten,
        # wie z.B. das Entfernen von Newline-Zeichen und die Konvertierung in den entsprechenden Datentyp.
        data = [float(line.strip())*1000000 for line in f.readlines()]
        # data.sort()
        
    plt.plot(np.arange(len(data))/len(data)*30, data, linewidth=2, alpha=1)
    plt.title("WebRTC Latenz")
    plt.ylabel('Latenz in ms')
    plt.xlabel('Laufzeit in s')
    plt.grid()

    plt.savefig(os.path.join(work_path, f"timed_plot_{PROTOCOL}.pdf"))

def print_diagram(filename):
    with open(filename, 'r') as f:
        # Es wird angenommen, dass die Daten numerisch sind und konvertiert werden können.
        # Beachten Sie, dass für eine korrekte Konvertierung ggf. zusätzliche Schritte notwendig sein könnten,
        # wie z.B. das Entfernen von Newline-Zeichen und die Konvertierung in den entsprechenden Datentyp.
        data = [float(line.strip())*1000000 for line in f.readlines()]
        data.sort()
        
    plt.plot(data, np.arange(len(data))/len(data), linewidth=4, alpha=1)
    plt.title("WebRTC - WebRTC Latenz")
    plt.ylabel('CDF')
    plt.xlabel('Zeit in ms')
    plt.ylim([0, 1])
    plt.grid()

    plt.savefig(os.path.join(work_path, f"cdf_plot_{PROTOCOL}.pdf"))

def main(video_path):
    """
    Main function to extract and print timestamps from all frames.
    """
    frames_dir = extract_frames(video_path, fps=FPS)
    frames = sorted(os.listdir(frames_dir))
    
    with open(results_file, 'w') as f:
        middle = 0
        i = 0
        for frame in frames:
            frame_path = os.path.join(frames_dir, frame)
            try:
                timestamp_browser, timestamp_sent = extract_timestamps_from_frame(frame_path)
            except ValueError:
                continue
            format_str = "%H:%M:%S.%f"  # Format including hours, minutes, seconds, and microseconds
            dt_browser = datetime.strptime(timestamp_browser, format_str)
            dt_sent = datetime.strptime(timestamp_sent, format_str)
            time_difference = dt_browser - dt_sent
            f.write(str(time_difference.total_seconds()/1000) + '\n')
            middle += time_difference.total_seconds()/1000
            i += 1
        print(middle/i)

if __name__ == "__main__":
    # video_path = os.path.join(work_path, f"{PROTOCOL}.mov")
    # main(video_path)
    print_diagram(results_file)
    # print_diagram_timed(results_file)
