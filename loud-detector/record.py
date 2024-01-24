import pyaudio #i think this has a yellow squiggle for me because i installed python when i already use python3 -> still works though
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
recordedData = []
#if you take this from me change this to where you want to save the recordings
saveDirectory = "/Users/liamrogers/Documents/recordings"

def saveRecording(recordedData, startTime):

    endTime = time.time()
    print("Recording ended at", time.ctime(endTime))
    #convert time_t object to readable time
    datetimeObj = datetime.fromtimestamp(startTime)
    readableTime = datetimeObj.strftime("%Y-%m-%d %H-%M-%S")
    fileName = os.path.join(saveDirectory, f"{readableTime}.wav")
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(struct.pack('h', samp) for samp in recordedData))
    wf.close()

    print(f"Recording saved as {fileName}")

try:
    while True:
        #read audio data from mic
        data = stream.read(1024)
        samples = struct.unpack('h' * 1024, data)

        #rms is apparently better than taking the max sample for this
        #also max sample didnt even work properly but this does
        rms = max(0, int((sum([(samp ** 2) for samp in samples]) / len(samples)) ** 0.5))

        if rms > threshold and not recording:
            recording = True
            startTime = time.time()
            print("Recording started at", time.ctime(startTime))
            recordedData = []  #start a new buffer

        if recording:
            recordedData.extend(samples)

            #once the audio goes below threshold again, end recording
            if rms <= threshold:
                recording = False
                saveRecording(recordedData, startTime)

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
        saveRecording(recordedData, startTime)
