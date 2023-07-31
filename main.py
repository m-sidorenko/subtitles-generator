from subtitle_generator import SubtitleGenerator

if __name__ == '__main__':

    generator = SubtitleGenerator(" ")
    clips = generator.create_clip_list()
    generator.create_sub_list(clips)

    generator.start_processing()

    # video = VideoFileClip('video.mp4')
    # audio = video.audio
    # audio.write_audiofile("audio.mp3")
    #
    # model = whisper.load_model("base")
    # transcribe_result = model.transcribe("audio.mp3")
    #
    # segments_list = transcribe_result['segments']
    # for e in segments_list:
    #     print(f'id: {e["id"]}, start: {e["start"]}, end: {e["end"]}, text: {e["text"]}\n')
    #
    # clip_size = video.size
    # clip_h = clip_size[0]
    # clip_w = clip_size[1]
    #
    # txt_list = []
    # clips_list = []
    #
    # for element in segments_list:
    #     start = element["start"]
    #     end = element["end"]
    #     if end > video.duration:
    #         end += (video.duration - end)
    #     vid = video.subclip(start, end)
    #
    #     txt = TextClip(
    #         element["text"], font='Courier-BoldOblique', fontsize=30, color='black',
    #         bg_color='gray', method='caption', size=(get_text_zone_size(clip_h, clip_w))
    #     )
    #
    #     txt = txt.set_duration(end - start)
    #     txt = txt.set_pos('bottom', 'center')
    #     txt_list.append(txt)
    #
    #     x = CompositeVideoClip([vid, txt])
    #     clips_list.append(x)
    #
    # audio_clip = AudioFileClip("audio.mp3")
    # new_video = concatenate_videoclips(clips_list)
    # new_video.audio = audio_clip
    # new_video.write_videofile("red_video.mp4")
