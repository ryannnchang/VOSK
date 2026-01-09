import os
import json
import subprocess
from vosk import Model, KaldiRecognizer

MODEL_PATH = "vosk-model-small-en-us-0.15"
AUDIO_DIR = "Test_Data"

model = Model(MODEL_PATH)

for filename in sorted(os.listdir(AUDIO_DIR)):
    if not filename.lower().endswith(".flac"):
        continue

    utterance_id = os.path.splitext(filename)[0]
    file_path = os.path.join(AUDIO_DIR, filename)

    recognizer = KaldiRecognizer(model, 16000)

    process = subprocess.Popen(
        [
            "ffmpeg",
            "-loglevel", "quiet",
            "-i", file_path,
            "-ar", "16000",
            "-ac", "1",
            "-f", "s16le",
            "-"
        ],
        stdout=subprocess.PIPE
    )

    while True:
        data = process.stdout.read(4000)
        if not data:
            break
        recognizer.AcceptWaveform(data)

    result = json.loads(recognizer.FinalResult())
    text = result.get("text", "").upper()
    with open("hypothesis.txt", "a") as f:
        f.write(f"{utterance_id} {text}\n")

