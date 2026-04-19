from deep_translator import GoogleTranslator
import yt_dlp
import requests
import whisper 
import os 

model = whisper.load_model("medium")

def translate(text):
    translated = GoogleTranslator(source="korean", target="english").translate(text=text)
    return translated

def translate_ytsubtitle(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False) #dict mit ALLEN Video-infos (Titel, Dauer, ...) - auch mit "automatic_captions"
        captions = info["automatic_captions"]   #automatic_captions ist ein dict mit allen Sprachen - ich brauche "ko" -> "ko" hat verschiedene Formate -> ich brauche "srt"
        ko_captions = captions["ko"]    #ko_captions ist ein dict mit nur koreanisch, aber verschiedenen Formaten
        subtitles = [sub for sub in ko_captions if sub["ext"] == "srt"] #srt holen 
        r = requests.get(subtitles[0]["url"])
        lines = r.text.split("\n\n") #r.text gibt wegen srt zeilen aus, deshalb in list holen
        timestamp = []
        for l in lines:
            parts = l.split("\n")
            if len(parts) >= 3:
                timestamp.append({"timestamp":parts[1], "text":parts[2]})
        for t in timestamp:
            print(f"{t["timestamp"]}: \n{translate(t["text"])}\n")

def download_audio(link):
    ydl_opts = {
        "extract_audio": True,
        "outtmpl": "audio",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as video:
        video.download(link)


def transcribe_audio():
    result = model.transcribe("audio.mp3", language="ko", task="translate", verbose=True)
    print(result["text"])

def translate_audio(url):
    download_audio(url)
    transcribe_audio()

def select():
    while True:
        print("Was willst du machen?\n1. Übersetzen\n2.ydl\n3. Audio herunterladen\n4. Audio transkript erstellen\n5. Beenden")
        choice = int(input())

        if choice == 1:
            text = input("Zu übersetzenden Text hier einfügen\n > ")
            print(translate(text))
        elif choice == 2:
            url = input("Hier URL einfügen:\n> ")
            translate_ytsubtitle(url)
        elif choice == 3:
            link = input("Hier URL einfügen:\n> ")
            download_audio(link)
        elif choice == 4:
            transcribe_audio()
        elif choice == 5: 
            break
        else:
            print("Keine gültige Eingabe")

select()



