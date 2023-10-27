import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip,vfx
import pysrt

# Set the paths to your video clip, audio file, and subtitle file
Background_clip = "background.mp4"  # Need to change path
audio_path = "temp_files/askreddit.mp3"
subtitle_path = "temp_files/subtitles.srt"  # Need to change path

# Load video clip and audio
clip2 = VideoFileClip(Background_clip)
audio = AudioFileClip(audio_path)

# Resize clip to compatible resolution (e.g., 1080x1920 for vertical video)
target_resolution = (760, 1080)  # Adjust as needed
clip2 = clip2.resize(target_resolution)

# Cut clip2 to the length of the audio file
if (clip2.duration > audio.duration):
    clip2 = clip2.subclip(0, audio.duration)
else:
    clip2 = clip2.loop(duration = audio.duration)

# Set the audio duration to match the minimum of the audio and the video
audio_duration = min(audio.duration, clip2.duration)

audio = audio.set_duration(audio_duration)

# Load the subtitles
subtitles = pysrt.open(subtitle_path)

# Function to create TextClips for each subtitle
def create_text_clips(subtitles):
    text_clips = []
    for s in subtitles:
        
        
        start_time = s.start.hours*3600 + s.start.minutes*60 + s.start.seconds
        end_time = s.end.hours*3600 + s.end.minutes*60 + s.end.seconds
        txt = s.text.replace('\n', ' ')

        text_clip = TextClip(txt, font="Arial-Bold", fontsize= 50, color='white', size=clip2.size, method='caption',
        align='center', print_cmd=True).set_start(start_time).set_duration(end_time - start_time)
        
        text_clips.append(text_clip)

    return text_clips

# Create TextClips from subtitles
text_clips = create_text_clips(subtitles)

# Set the clip's audio and add subtitles
final_clip = CompositeVideoClip([clip2] + text_clips).set_audio(audio)

# Set the output file path
output_path = "video_output/output.mp4"

# Write the final video with audio and subtitles
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Close the video and audio clips to release resources
clip2.close()
audio.close()
final_clip.close()
