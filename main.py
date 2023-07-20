import whisper
from moviepy.editor import *

if __name__ == '__main__':

    video = VideoFileClip("video.mp4")
    audio = video.audio
    audio.write_audiofile("audio.mp3")

    model = whisper.load_model("base")
    transcribe_result = model.transcribe("audio.mp3")

    segments_list = transcribe_result['segments']
    for e in segments_list:
        print(f'id: {e["id"]}, start: {e["start"]}, end: {e["end"]}, text: {e["text"]}\n')

    clip = VideoFileClip("video.mp4")
    txt_list = []
    clips_list = []

    for element in segments_list:
        start = element["start"]
        end = element["end"]
        if end > clip.duration:
            end += (clip.duration - end)

        vid = clip.subclip(start, end)

        txt = TextClip(element["text"], fontsize=28, color='white', bg_color='black', method='caption', size=(400, 200),
                       stroke_width=4).set_duration(end - start)
        txt = txt.set_pos('bottom', 'center')
        txt_list.append(txt)

        x = CompositeVideoClip([vid, txt])
        clips_list.append(x)
        # x.write_videofile(f"{element['id']}.mp4")

    new_video = concatenate_videoclips(clips_list)
    audio_clip = AudioFileClip("video.mp4")
    new_video.audio = audio_clip
    new_video.write_videofile("red_video.mp4")


