import whisper
from moviepy.editor import *
import os
from pathlib import Path

RAW_FILES_FOLDER_NAME = 'raw'


def get_text_zone_size(height, width) -> tuple[float, float]:
    if height < width:
        return .8 * height, .15 * width
    else:
        return .8 * width, .15 * height


class SubtitleGenerator:
    __original_clip_name = str

    def __init__(self, original_clip_name):
        self.__original_clip_name = original_clip_name

    @staticmethod
    def __create_clip_by_file_name(self) -> VideoFileClip:
        video = VideoFileClip
        file_name = str
        flag = True

        while flag:
            print("> Write the file name and press [Enter]:")
            file_name = 'video.mp4' # input() !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if len(file_name) == 0:
                print("> ERROR! The name is empty. Check your answer and try again.")
                continue

            try:
                video = VideoFileClip(file_name)
            except IOError:
                print("> ERROR! No such file or directory. Check your answer and try again.")
                continue
            flag = False

        self.__original_clip_name = file_name
        return video

    def start_processing(self):
        video = self.__create_clip_by_file_name(self)
        video_name = str(video.filename).split(".")[0]
        audio = video.audio
        audio.write_audiofile(f'audio.mp3')

        model = whisper.load_model("base")
        transcribe_result = model.transcribe("audio.mp3")
        segments_list = transcribe_result['segments']

        with open(f'{video_name}_transcription.txt', 'w+') as file:
            for e in segments_list:
                file.write(f'id: {e["id"]}, \tstart: {e["start"]}, \tend: {e["end"]}, \ttext: {e["text"]}\n')

        clip_size = video.size
        clip_h = clip_size[0]
        clip_w = clip_size[1]

        txt_list = []
        clips_list = []

        os.getcwd()
        for element in segments_list:
            start = element["start"]
            end = element["end"]
            if end > video.duration:
                end += (video.duration - end)
            vid = video.subclip(start, end)

            txt = TextClip(
                element["text"], font='Courier-BoldOblique', fontsize=30, color='black',
                bg_color='gray', method='caption', size=(get_text_zone_size(clip_h, clip_w))
            )

            txt = txt.set_duration(end - start)
            txt = txt.set_pos('bottom', 'center')
            txt_list.append(txt)

            composite_video_clip = CompositeVideoClip([vid, txt])
            clips_list.append(composite_video_clip)

        audio_clip = AudioFileClip("audio.mp3")
        new_video = concatenate_videoclips(clips_list)
        new_video.audio = audio_clip
        new_video.write_videofile(f'red_{self.__original_clip_name}')

        folder_name = f'result_{self.__original_clip_name}'
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        os.rename(f'red_{self.__original_clip_name}', f'{folder_name}/red_{self.__original_clip_name}')
        os.rename(f'{video_name}_transcription.txt', f'{folder_name}/{video_name}_transcription.txt')
        os.rename(f'audio.mp3', f'{folder_name}/audio.mp3')

    def create_clip_list(self) -> list:
        clip_list = list()
        print(f"> Put video/-s to the folder '{RAW_FILES_FOLDER_NAME}' and press [Enter]:")
        input()

        for path in list(Path(f'{RAW_FILES_FOLDER_NAME}/').rglob('*.mp4')):
            try:
                file = VideoFileClip(f'{RAW_FILES_FOLDER_NAME}/{path.name}')
                clip_list.append(file)
            except IOError:
                print(f"> ERROR! There aren't files in the folder. Check '{RAW_FILES_FOLDER_NAME}' folder.")
                return list()

        return clip_list

    def create_sub_list(self, clip_list):
        for clip in clip_list:
            self.start_processingV2(clip)

    def start_processingV2(self, clip):
        video_name = str(clip.filename).split(".")[0].split('/')[1]
        audio = clip.audio
        audio.write_audiofile(f'{video_name}_audio.mp3')

        model = whisper.load_model("base")
        transcribe_result = model.transcribe(f'{video_name}_audio.mp3')
        segments_list = transcribe_result['segments']

        with open(f'{video_name}_transcription.txt', 'w+') as file:
            for e in segments_list:
                file.write(f'id: {e["id"]}, \tstart: {e["start"]}, \tend: {e["end"]}, \ttext: {e["text"]}\n')

        clip_size = clip.size
        clip_h = clip_size[0]
        clip_w = clip_size[1]

        txt_list = []
        clips_list = []

        os.getcwd()
        for element in segments_list:
            start = element["start"]
            end = element["end"]
            if end > clip.duration:
                end += (clip.duration - end)
            vid = clip.subclip(start, end)

            txt = TextClip(
                element["text"], font='Courier-BoldOblique', fontsize=30, color='black',
                bg_color='gray', method='caption', size=(get_text_zone_size(clip_h, clip_w))
            )

            txt = txt.set_duration(end - start)
            txt = txt.set_pos('bottom', 'center')
            txt_list.append(txt)

            composite_video_clip = CompositeVideoClip([vid, txt])
            clips_list.append(composite_video_clip)

        audio_clip = AudioFileClip(f'{video_name}_audio.mp3')
        new_video = concatenate_videoclips(clips_list)
        new_video.audio = audio_clip
        new_video.write_videofile(f'red_{video_name}.mp4')

        folder_name = f'result_{video_name}'
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        os.rename(f'red_{video_name}.mp4', f'{folder_name}/red_{video_name}.mp4')
        os.rename(f'{video_name}_transcription.txt', f'{folder_name}/{video_name}_transcription.txt')
        os.rename(f'{video_name}_audio.mp3', f'{folder_name}/{video_name}_audio.mp3')


def print_greetings():
    print('''
                  _      _    _  _    _                                                   _               
                 | |    | |  (_)| |  | |                                                 | |              
      ___  _   _ | |__  | |_  _ | |_ | |  ___        __ _   ___  _ __    ___  _ __  __ _ | |_  ___   _ __ 
     / __|| | | || '_ \ | __|| || __|| | / _ \      / _` | / _ \| '_ \  / _ \| '__|/ _` || __|/ _ \ | '__|
     \__ \| |_| || |_) || |_ | || |_ | ||  __/     | (_| ||  __/| | | ||  __/| |  | (_| || |_| (_) || |   
     |___/ \__,_||_.__/  \__||_| \__||_| \___|      \__, | \___||_| |_| \___||_|   \__,_| \__|\___/ |_|   
                                                     __/ |                                                
                                                    |___/                                                           

        ''')
