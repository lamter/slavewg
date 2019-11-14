import wave
import pyaudio

# 定义数据流块
CHUNK = 1024
FORMAT = pyaudio.paInt16
# CHANNELS = 1 # 声卡
CHANNELS = 2  # 麦克风
RATE = 44100
# 录音时间
RECORD_SECONDS = 3
# 要写入的文件名
# WAVE_OUTPUT_FILENAME = "/Users/lamter/Downloads/背景音.wav"
WAVE_OUTPUT_FILENAME = "Y:\Downloads\win上钩.wav"
# 创建PyAudio对象
p = pyaudio.PyAudio()

# 打开数据流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

# 开始录音
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

# 停止数据流
stream.stop_stream()
stream.close()

# 关闭PyAudio
p.terminate()

# 写入录音文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
