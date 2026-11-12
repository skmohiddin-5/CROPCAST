from gtts import gTTS

text = (
    "Rainfall probability in Gudlavalleru "
    "is 16 percent. No rain is predicted."
)

tts = gTTS(
    text=text,
    lang="en"
)

tts.save("audio/test_alert.mp3")

print("Voice notification created successfully!")