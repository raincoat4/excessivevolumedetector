import pyaudio
import time
import struct
import wave
import os
from datetime import datetime

threshold = 10000

#set up audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

recording = False
recorded_data = []
#if you take this from me change this to where you want to save the recordings
save_directory = "/Users/liamrogers/Documents/recordings"

def save_recording():
    global recorded_data
    global start_time

    end_time = time.time()
    print("Recording ended at", time.ctime(end_time))
    #convert time_t object to readable time
    datetimeObj = datetime.fromtimestamp(start_time)
    readableTime = datetimeObj.strftime("%H-%M-%S")
    file_name = os.path.join(save_directory, f"{readableTime}.wav")
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(struct.pack('h', samp) for samp in recorded_data))
    wf.close()

    print(f"Recording saved as {file_name}")

try:
    while True:
        #read audio data from mic
        data = stream.read(1024)
        samples = struct.unpack('h' * 1024, data)

        #rms is apparently better for this i dont really know why
        rms = max(0, int((sum([(samp ** 2) for samp in samples]) / len(samples)) ** 0.5))

        if rms > threshold and not recording:
            recording = True
            start_time = time.time()
            print("Recording started at", time.ctime(start_time))
            recorded_data = []  #start a new buffer

        if recording:
            recorded_data.extend(samples)

            #once the audio goes below threshold again, end recording
            if rms <= threshold:
                recording = False
                save_recording()

        #print messages as it goes over
        if recording:
            print(f"RMS: {rms}")

except KeyboardInterrupt:
    pass
finally:
    #close
    stream.stop_stream()
    stream.close()
    p.terminate()

    if recording:
        save_recording()
