import pyttsx3


class Voice:
    def __init__(self):
        self.engine = pyttsx3.init("sapi5")
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)

        voices = self.engine.getProperty("voices")
        if voices:
            self.engine.setProperty("voice", voices[0].id)
            print(f"TTS actief: {voices[0].name}")

    def say(self, text: str):
        print(f"[Engineer]: {text}")
        self.engine.stop()
        self.engine.say(text)
        self.engine.runAndWait()