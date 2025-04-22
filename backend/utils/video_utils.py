import cv2
import os
from moviepy.editor import ImageSequenceClip

def extract_frames(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    count = 0
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, frame)
        frames.append(frame_path)
        count += 1
    cap.release()
    return frames

def recompile_video(frames, output_path):
    clip = ImageSequenceClip(frames, fps=24)
    clip.write_videofile(output_path, codec='libx264')
