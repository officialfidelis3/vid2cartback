import cv2
import os
from moviepy.editor import ImageSequenceClip
from utils.video_utils import extract_frames, recompile_video

def cartoonize_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def cartoonize_video(video_path, filename):
    frames_dir = f"temp_frames/{filename.split('.')[0]}"
    os.makedirs(frames_dir, exist_ok=True)
    
    frames = extract_frames(video_path, frames_dir)
    cartoonized = []

    for f in frames:
        img = cv2.imread(f)
        cartoon = cartoonize_frame(img)
        out_path = f.replace('temp_frames', 'cartoon_frames')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        cv2.imwrite(out_path, cartoon)
        cartoonized.append(out_path)

    result_video = f"results/{filename}"
    recompile_video(cartoonized, result_video)
    return result_video
