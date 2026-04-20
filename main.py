from deep_translator import GoogleTranslator
import yt_dlp
import requests
import whisper 
import os 
import sys

model = whisper.load_model("medium")

def translate(text):
    translated = GoogleTranslator(source="korean", target="english").translate(text=text)
    return translated

def translate_ytsubtitle(info):
        captions = info["subtitles"]
        captions_auto = info["automatic_captions"]   #automatic_captions ist ein dict mit allen Sprachen - ich brauche "ko" -> "ko" hat verschiedene Formate -> ich brauche "srt"
        if "ko" in captions.keys():
            ko_captions = captions["ko"]
        elif "ko" in captions_auto.keys():
            ko_captions = captions_auto["ko"]
        subtitles = [sub for sub in ko_captions if sub["ext"] == "srt"] #srt holen 
        r = requests.get(subtitles[0]["url"])
        lines = r.text.split("\n\n") #r.text gibt wegen srt zeilen aus, deshalb in list holen
        timestamp = []
        for l in lines:
            parts = l.split("\n")
            if len(parts) >= 3:
                timestamp.append({"timestamp":parts[1], "text":parts[2]})
        text = ""
        for t in timestamp:
            text = text + t
            #print(f"{t["timestamp"]}: \n{translate(t["text"])}\n")
        translated_full = translate(text)
        print(translated_full)

def smart_translate(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)   #dict mit ALLEN Video-infos (Titel, Dauer, ...) - auch mit "automatic_captions"
        if "ko" in info["subtitles"] or "ko" in info["automatic_captions"]:
            print("\nUntertitel gefunden, starte Übersetzung\n")
            translate_ytsubtitle(info)
        else:
            print("\nKeine Untertitel gefunden, verwende AI um Audio zu übersetzen\n")
            translate_audio(url)

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
    result = model.transcribe("audio.mp3", task="translate", verbose=True)
    print(result["text"])

def translate_audio(url):
    download_audio(url)
    transcribe_audio()
    os.remove("audio.mp3")

def select():
    while True:
        print("Was willst du machen?\n1. Übersetzen\n2. YouTube Video Übersetzen\n3. Beenden")
        choice = int(input())

        if choice == 1:
            text = input("Zu übersetzenden Text hier einfügen\n > ")
            print(translate(text))
        elif choice == 2:
            url = input("Hier URL einfügen:\n> ")
            smart_translate(url)
        elif choice == 3:
            break
        else:
            print("Keine gültige Eingabe")

if __name__ == "__main__":
    select()




