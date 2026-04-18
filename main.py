from deep_translator import GoogleTranslator
import yt_dlp
import requests 

def translate(text):
    translated = GoogleTranslator(source="korean", target="english").translate(text=text)
    return translated

def ydl():
    url = "https://youtu.be/b5818MUdMs4?si=ZJhs0bovRNiy2WuC"  #input("Hier URL einfügen:\n> ")
    ydl_opts = {
    "skip_download" : True,
    }

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
            
        
        
    
def select():
    print("Was willst du machen?\n1. Übersetzen\n2.ydl")
    choice = int(input())

    if choice == 1:
        text = input("Zu übersetzenden Text hier einfügen\n > ")
        print(translate(text))
    elif choice == 2:
        ydl()
    else:
        print("Keine gültige Eingabe")
    return choice

select()



