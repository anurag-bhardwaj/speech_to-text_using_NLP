from tkinter import *
import speech_recognition as sr
from PIL import ImageTk,Image
import webbrowser as wb
from gtts import gTTS
import playsound
import os
import wikipedia
from googletrans import Translator
r=sr.Recognizer()
translator=Translator()


def speak_func(audio_val,lang_val):
    tts=gTTS(text=audio_val, lang=lang_val)
    audio_file='audio'+'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)

def speak_trans_text(event):
    global variable_for_trans
    voiceData=TextArea2.get(1.0,END)
    if(variable_for_trans.get()=="English"):
        lang_dest='en'
    elif(variable_for_trans.get()=="Hindi"):
        lang_dest='hi'
    elif(variable_for_trans.get()=="French"):
        lang_dest='fr'
    elif(variable_for_trans.get()=="German"):
        lang_dest='de'
    speak_func(voiceData, lang_dest)
    
    
def Translate_text(voice_data,lang):
    global TextArea2
    global variable_for_trans
    global variable_for_detect
    if(variable_for_detect.get()!="None"):
        if(variable_for_detect.get()=="English"):
            lang='en'
        elif(variable_for_detect.get()=="Hindi"):
            lang='hi'
        elif(variable_for_detect.get()=="French"):
            lang='fr'
        elif(variable_for_detect.get()=="German"):
            lang='de'
        if(variable_for_trans.get()=="English"):
            lang_dest='en'
        elif(variable_for_trans.get()=="Hindi"):
            lang_dest='hi'
        elif(variable_for_trans.get()=="French"):
            lang_dest='fr'
        elif(variable_for_trans.get()=="German"):
            lang_dest='de'
        translated_sentence=translator.translate(voice_data,src=lang,dest=lang_dest)
        TextArea2.insert(END,translated_sentence.text)
    else:
        speak_func("please choose a language",'en')
        


def record_audio(event):
    global TextArea
    global variable_for_detect
    if(variable_for_detect.get()!="None"):
        if(variable_for_detect.get()=="English"):
            lang='en'
        elif(variable_for_detect.get()=="Hindi"):
            lang='hi'
        elif(variable_for_detect.get()=="French"):
            lang='fr'
        elif(variable_for_detect.get()=="German"):
            lang='de'
        TextArea.delete('1.0', END)
        TextArea.update()
        TextArea2.delete('1.0', END)
        TextArea2.update()
        voice_data=' '
        speak_func("speak now",'en')
        with sr.Microphone() as source:
            audio=r.listen(source)
            try:
                voice_data=r.recognize_google(audio,language=lang)
            except Exception as e:
                speak_func("i did not get that sir",'en')
        TextArea.insert(END,voice_data)
        Translate_text(voice_data,lang)
    else:
        speak_func("please choose a language",'en')
    


def record_audio_Bot():
    voice_data=' '
    with sr.Microphone() as source:
        audio=r.listen(source)
        try:
            voice_data=r.recognize_google(audio)
        except Exception as e:
            speak_func("i did not get that sir",'en')
    return voice_data
    
def Bot_func(event):
    speak_func('Hello Sir! what you want to search. I can give you the best results available on wikipedia.', 'en')
    audio_data=record_audio_Bot()
    if("search" in audio_data):
        speak_func("what you want to search",'en')
        search=record_audio_Bot()
        url="https://www.google.co.in/search?client=opera&q="+search
        wb.get().open(url)
    
    elif("what is" in audio_data):
        wiki_search=audio_data.replace("what is",'')
        wiki_result=wikipedia.summary(wiki_search, sentences=3)
        speak_func('According to wikipedia','en')
        speak_func(wiki_result,'en')

    elif("who is" in audio_data):
        wiki_search=audio_data.replace("who is",'')
        wiki_result=wikipedia.summary(wiki_search, sentences=3)
        speak_func('According to wikipedia','en')
        speak_func(wiki_result,'en')

root=Tk()
root.title("Speech_Reco")
root.geometry("400x600")

f1=Frame(root,bg="ghostwhite")
Label(f1,text="Translate your text here",font="BELLMT 18 bold",fg="green",bg="ghostwhite").pack(padx="50",fill=X,pady="60")
f1.pack(fill=X)

f2=Frame(root,bg="white")
Label(f2,text="choose language",font="BELLMT 18 bold",fg="black",bg="white").pack(side=LEFT,padx="10",pady="5")


OptionList = [
"None",
"English",
"Hindi",
"French",
"German"
]

variable_for_detect = StringVar(f2)
variable_for_detect.set(OptionList[0])

choose_opt =OptionMenu(f2, variable_for_detect, *OptionList)
choose_opt.config(width=6,height=1, font=('Helvetica', 12),bg="white")
choose_opt.pack(side=LEFT)

f2.pack(fill=X,ipady="20")

f3=Frame(root,bg="white")

phot=PhotoImage(file="spk.png")
photo=phot.subsample(10,10)
spk_button=Button(f3,image=photo, height=50,width=55)
spk_button.bind("<Button-1>", record_audio)
spk_button.pack(side=LEFT,padx=20)

slide=Scrollbar(f3)
slide.pack(side=RIGHT,fill=Y)
TextArea=Text(f3,font="Ariana 10",height="3",yscrollcommand=slide.set)
TextArea.pack(padx="5")
slide.config(command=TextArea.yview)

f3.pack(fill=X)


f4=Frame(root,bg="white")
Label(f4,text="translate to         ",font="BELLMT 18 bold",fg="black",bg="white").pack(side=LEFT,padx="10",pady="5")


OptionList = [
"None",
"English",
"Hindi",
"French",
"German"
]

variable_for_trans = StringVar(root)
variable_for_trans.set(OptionList[0])

detect_opt =OptionMenu(f4, variable_for_trans, *OptionList)
detect_opt.config(width=6,height=1, font=('Helvetica', 12),bg="white")
detect_opt.pack(side=LEFT)

f4.pack(fill=X,ipady="40")


f5=Frame(root,bg="white")


spk_button2=Button(f5,image=photo, height=50,width=55)
spk_button2.bind("<Button-1>", speak_trans_text)
spk_button2.pack(side=LEFT,padx=20)

slide=Scrollbar(f5)
slide.pack(side=RIGHT,fill=Y)
TextArea2=Text(f5,font="Ariana 10",height="3",yscrollcommand=slide.set)
TextArea2.pack(padx="5")
slide.config(command=TextArea2.yview)

f5.pack(fill=X)


f6=Frame(root,bg="white")
Label(f6,text="                   ",font="BELLMT 18 bold",fg="black",bg="white").pack(side=LEFT,fill=X)
f6.pack(fill=X)

f7=Frame(root)
Bot_phot=PhotoImage(file="bot.png")
Bot_photo=Bot_phot.subsample(12,12)
Bot_button=Button(f7,image=Bot_photo, height=100,width=60)
Bot_button.bind("<Button-1>", Bot_func)
Bot_button.pack(side=RIGHT,padx=20,pady=20)
f7.pack(fill=X)

root.mainloop()
