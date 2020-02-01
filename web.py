# importing speech recognition package from google api 
import speech_recognition as sr  
import playsound # to play saved mp3 file 
from gtts import gTTS # google text to speech 
import os, sys # to save/open files 
import wolframalpha # to calculate strings into formula 
#from selenium import webdriver # to control browser operations
from googlesearch import search as gsearch
import webbrowser
import googletrans
import requests
from bs4 import BeautifulSoup

languages = googletrans.LANGCODES

del languages["chinese (simplified)"]
del languages["chinese (traditional)"]
languages["chinese"] = "zh-cn"
  
num = 1
def assistant_speaks(output, lang='fr'):
    global num 
  
    # num to rename every audio file  
    # with different name to remove ambiguity b
    num += 1
    print("Mrs Nobody : ", output) 
  
    toSpeak = gTTS(text = output, lang =lang, slow = False) 
    # saving the audio file given by google text to speech 
    file = str(num)+".mp3  "
    toSpeak.save(file) 
      
    # playsound package is used to play the same file. 
    playsound.playsound(file, True)  
    os.remove(file) 
  

def scan_for_wake_up(): 
  
    rObject = sr.Recognizer() 
    audio = '' 
  
    with sr.Microphone() as source: 
          
        # recording the audio using speech recognition 
        
        rObject.adjust_for_ambient_noise(source)
        audio = rObject.listen(source)  

        text = rObject.recognize_google(audio, language ='fr-FR') 
        return text 

  
def get_audio(): 
  
    rObject = sr.Recognizer() 
    audio = '' 
  
    with sr.Microphone() as source: 
        print("Je vous écoute...") 
          
        # recording the audio using speech recognition 
        
        rObject.adjust_for_ambient_noise(source)
        audio = rObject.listen(source)  
    print("Stop.") # limit 5 secs 
  
    try: 
  
        text = rObject.recognize_google(audio, language ='fr-FR') 
        print("Vous avez dit : ", text) 
        return text 
  
    except: 
  
        assistant_speaks("Je n'ai pas compris, réessayez !") 
        return 0

def traduire(text="", src="", dest=""):
    translator = googletrans.Translator() # Create object of Translator.
    translated = translator.translate(str(text), src=src, dest=dest) 
    return(translated.text)


def get_answer(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    print(soup)
    return (soup)

def search(text=''):

    client = wolframalpha.Client("Y3UAYV-J5KAG7RULW")
    shortquery = text.strip().replace(" ", "+")
    url = 'https://api.wolframalpha.com/v1/result?i=' + str(shortquery) + '%3F&appid=Y3UAYV-J5KAG7RULW'
    res = client.query(text)
    print(shortquery)

    # Wolfram cannot resolve the question
    if res['@success'] == 'false':
        print("success : no")
        #for keys,values in res.items():
        #    print(str(keys) + " : " + str(values))
        try:
        	shortquery = (str(mean['didyoumean']['#text']))
        	shortquery = shortquery.strip().replace(" ", "+")
        	url = 'https://api.wolframalpha.com/v1/result?i=' + str(shortquery) + '%3F&appid=Y3UAYV-J5KAG7RULW'
        	print(url)
        	result=get_answer(str(url))
        except Exception as e:
        	assistant_speaks("Je crois que je n'ai pas bien compris ce que vous vouliez.")
        	pass
        else:
        	mean = res['didyoumeans']
           
    else:
        print("success : yes")
        result=get_answer(str(url))

    try:
        print(result)
        result = traduire(result, 'en', 'fr')
        assistant_speaks(str(result))
        
    except Exception as e:
        print("Pas de résultat")

def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']


def removeBrackets(variable):
    return variable.split('(')[0]


def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']

def removeBrackets(variable):
    return variable.split('(')[0]


def process_text(voix_user): 
    if 'cherche' in voix_user or 'joue' in voix_user: 
        # a basic web crawler using selenium 
        search_web(voix_user) 
        return

    elif "qui es-tu" in voix_user: 
        speak = '''Je suis Madame Nobody, je suis là pour te servir.'''
        assistant_speaks(speak) 
        return

    # elif "calcul" in voix_user: 
    #     query = voix_user.split("calcul ")[1]
    #     res = client.query(query)
    #     output = next(res.results).text
    #     print(output)
    #     assistant_speaks("La réponse est " + output)
    #     return

    elif "traduire" in voix_user:
        txt_to_translate = voix_user.split("en ")[0]
        txt_to_translate = txt_to_translate.split("traduire ")[1]

        want = voix_user.split("en ")[1]

        want = traduire(text=want, src="fr", dest="en").lower()
        want=languages[want]
        translated = traduire(text=txt_to_translate, src="fr", dest=want)


        assistant_speaks(translated, lang=want)

    elif "traduis" in voix_user:
        txt_to_translate = voix_user.split("en ")[0]
        txt_to_translate = txt_to_translate.split("traduis ")[1]

        want = voix_user.split("en ")[1]

        want = traduire(text=want, src="fr", dest="en").lower()
        want=languages[want]
        translated = traduire(text=txt_to_translate, src="fr", dest=want)


        assistant_speaks(translated, lang=want)

    elif 'ouvre' in voix_user: 
          
        # another function to open  
        # different application availaible 
        open_application(voix_user)  
        return

    else: 
        query = traduire(voix_user, 'fr', 'en')
        search(query)

def search_web(voix_user): 

    for j in gsearch(voix_user, tld="fr", num=10, stop=5, pause=2): 
        if 'youtube' in j:
            if 'channel' in j or 'user' in j:
                assistant_speaks("J'ai trouvé une chaîne Youtube")
            elif 'watch' in j:
                assistant_speaks("J'ai trouvé une vidéo Youtube")
            else:
                assistant_speaks("J'ai trouvé quelque chose sur Youtube")
        elif 'wikipedia' in j:
            if 'en.' in j:
                assistant_speaks("J'ai trouvé un article Wikipédia anglais")
            elif 'fr.' in j:
                assistant_speaks("J'ai trouvé un article Wikipédia français")
            else:
                assistant_speaks("J'ai trouvé un article Wikipédia")

        else:
            print(str(j))
            url = j.split("//")[-1].split("/")[0].split('?')[0]
            assistant_speaks("J'ai trouvé le site " + str(url))

        assistant_speaks("Est-ce que c'est ce que vous cherchez ?")
        ans = get_audio() 

        if 'oui' in str(ans) or 'ouais' in str(ans):
            webbrowser.open(j, new=0, autoraise=True)
            sys.exit()
    sys.exit()

  
  
# function used to open application 
# present inside the system. 
def open_application(voix_user): 
  
    if "chrome" in voix_user: 
        assistant_speaks("Google Chrome") 
        try:
            os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        except FileNotFoundError:
            assistant_speaks("Chrome n'est pas installé sur votre ordinateur")
         
        return
  
    elif "firefox" in voix_user or "mozilla" in voix_user: 
        assistant_speaks("Ouverture de Mozilla Firefox") 
        try:
            os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe') 
        except FileNotFoundError:
            assistant_speaks("Firefox n'est pas installé sur votre ordinateur")
        return
  
    elif "word" in voix_user: 
        assistant_speaks("Ouverture de  Word") 
        try:
            os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Word 2013.lnk')
        except FileNotFoundError:
            assistant_speaks("Word n'est pas installé sur votre ordinateur")
        return
  
    elif "excel" in voix_user: 
        assistant_speaks("Ouverture d'Excel") 
        try:
            os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
        except FileNotFoundError:
            assistant_speaks("Excel n'est pas installé sur votre ordinateur")
        return
  
    else: 
  
        assistant_speaks("Je ne connais pas cette application") 
        return
  
# Driver Code 
if __name__ == "__main__": 
    name ='Humain'
      
    while(1):
        text0 = str(scan_for_wake_up()).lower() 
        if 'alexia' in text0:
            playsound.playsound('listen.mp3', True)
            text = str(get_audio()).lower() 

            if text == 0: 
                continue
      
            elif "stop" in str(text) or "bye" in str(text) or "quitte" in str(text): 
                playsound.playsound('close.mp3', True)
                break
            else:
                # calling process text to process the query 
                process_text(text) 
        break

