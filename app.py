from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
import time
from kivy.uix.videoplayer import VideoPlayer
from moviepy.editor import concatenate_audioclips, AudioFileClip, VideoFileClip

from moviepy.editor import ImageSequenceClip
from PIL import Image
import io
import numpy as np
import gtts  
from playsound import playsound
from mutagen.mp3 import MP3
from decouple import config
import requests








Builder.load_file('app.kv')

class ScreenOne(Screen):
    def query(self, payload, API_URL, headers):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    def create_video_from_images(self, imgs, times, output_filename, fps=30):
        if len(imgs) != len(times):
            raise ValueError("Number of images and times must be the same.")

        frame_durations = [int(time * fps) for time in times]
        frames = []

        for img in imgs:
            frames.extend([img] * frame_durations.pop(0))

        video = ImageSequenceClip(frames, fps=fps)

        video.write_videofile(output_filename, codec='libx264')


    def concatenate_audio_moviepy(self, audio_clip_paths, output_path):
        """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)    


    def generate(self):
        txt = self.ids.txtid.text
        API_URL = config('API_URL')
        headers = {"Authorization": str(config("AUTH"))}
        
        imgList = txt.split("\n")

        imgs = []
        clipLens = []
        i = 0
        for x in imgList:
            image_bytes = self.query({"inputs": f"{x}"}, API_URL, headers)
            imgs.append(image_bytes)
            t1 = gtts.gTTS(f"{x}")
            t1.save(f"audioclips/{i}.mp3")
            audio = MP3(f"audioclips/{i}.mp3")
            clipLens.append(audio.info.length)   
            i+=1

        imgList = [np.array(Image.open(io.BytesIO(x))) for x in imgs] 
        self.create_video_from_images(imgList, clipLens, "output.mp4", fps = 30)

        
        paths = [f"audioclips/{x}.mp3" for x in range(i)]
        self.concatenate_audio_moviepy(paths, "audio.mp3")

        video_clip = VideoFileClip("output.mp4")
        audio_clip = AudioFileClip("audio.mp3")

        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("Video.mp4")

        app = App.get_running_app()
        second_screen = app.root.get_screen('second')
        second_screen.update_video('Video.mp4')
        app.root.current = 'second'
        

    
class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        path = ''
        # Create a VideoPlayer widget and set its source
        self.video = VideoPlayer(source=path)
        self.add_widget(self.video)    
    
    def update_video(self, source_path):
        self.video.source = source_path        

class AiVideoGenerator(App):
    def build(self):
        sm = ScreenManager()
        one = ScreenOne(name = "first")
        two = VideoScreen(name = "second")
        sm.add_widget(one)
        sm.add_widget(two)
        return sm

AiVideoGenerator().run()    