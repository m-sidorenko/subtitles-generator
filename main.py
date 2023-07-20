
import json
import whisper
from moviepy.editor import *
import math

if __name__ == '__main__':

    video = VideoFileClip("video.mp4") 
    audio = video.audio
    audio.write_audiofile("audio.mp3")
    
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")

    list = result['segments']
    for e in list:
        print(f'id: {e["id"]}, start: {e["start"]}, end: {e["end"]}, text: {e["text"]}\n')

    clip = VideoFileClip("video.mp4")
    txt_list = []
    vid_list = []
    clips_list = []

    for element in list:
        start = element["start"]
        end = element["end"]
        if end > clip.duration: 
            end += (clip.duration - end)

        vid = clip.subclip(start, end)

        vid_list.append(vid)

        txt = TextClip(element["text"], fontsize = 28, 
                       color = 'white', bg_color = 'black', 
                       method = 'caption', size = (400, 200),  
                       stroke_width = 4 )
        .set_duration(end - start)
        
        txt = txt.set_pos('bottom', 'center')
        txt_list.append(txt)
       
        x = CompositeVideoClip([vid, txt])
        clips_list.append(x)
        # x.write_videofile(f"{element['id']}.mp4")

    video = concatenate_videoclips(clips_list)
    # video = CompositeVideoClip(clips_list)
    video.write_videofile("red_video.mp4")


