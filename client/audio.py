from imp import is_builtin
import time
import pyaudio

from .client import Client

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2


class MicStream:
    def __init__(self,
        format=FORMAT, channels=CHANNELS, rate=RATE,
        chunk=CHUNK, record_seconds=RECORD_SECONDS
    ):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=format, channels=channels, rate=rate,
            input=True, stream_callback=self.process_mic_input,
            frames_per_buffer=chunk
        )
        self.client = Client()
        self.is_blocked = True

    def block(self):
        self.is_blocked = not self.is_blocked

    def send_audio(self, input_data):
        self.client.sendall(input_data)

    def stream_audio(self):
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.1)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


    def process_mic_input(self, input_data, frame_count, time_info, flags):
        
        return input_data, pyaudio.paContinue

