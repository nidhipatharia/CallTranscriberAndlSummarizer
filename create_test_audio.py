"""Create a minimal test audio file for pipeline demo."""
import wave
import struct

# 2 seconds, 16kHz mono (Whisper-friendly)
sample_rate = 16000
duration = 2
n_frames = sample_rate * duration

with wave.open("sample_recording.wav", "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    wav.writeframes(struct.pack(f"<{n_frames}h", *([0] * n_frames)))

print("Created sample_recording.wav")
