import pythoncom
import pyaudio
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyjokes
import wikipedia
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyDictionary import PyDictionary
from googletrans import Translator
from GoogleNews import GoogleNews
global executable_path
executable_path = "E:\python programs\chromedriver.exe"
engine=pyttsx3.init("sapi5")
engine.setProperty('rate', 150)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)
def greet():
    speak("Initialising FRIDAY")
    print("Initialising FRIDAY")
    hr=int(datetime.datetime.now().hour)
    if hr>=5 and hr<12:
        speak("Good Morning Master")
    elif hr>=12 and hr<17:
        speak("Good Afternoon Master")
    else:
        speak("Good Evening Master")
def commandrecog():
    query=1
    r1=sr.Recognizer()
    with sr.Microphone() as source:
        r1.adjust_for_ambient_noise(source)
        print("--")
        audio=r1.listen(source)
        try:
            query1=r1.recognize_google(audio,language='en-in')
        except Exception as e:
            print("?")
            query1=commandrecog()
        print(query1)
        if "friday"in query1.lower():
            speak("Yes Master")
            query=commandip()
        if "shutdown" in query1.lower():
            speak("Shutting down from the servers")
            exit()
        else:
            commandrecog()

def commandip():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening")
        audio=r.listen(source)
        try:
            print("Recognizing")
            query=r.recognize_google(audio,language='en-in')
            print(query)
            if "shutdown" in query.lower():
                speak("Shutting down from the servers")
                exit()
            speak("You said"+str(query))
            commandop(query)
        except Exception as e:
            speak("Say again please")
            query=commandip()
def commandop(query):
    print(".....")
    if "joke" in query.lower():
        joke=pyjokes.get_joke()
        print(joke)
        speak(joke)
    if "open google" in query.lower():
        webbrowser.open('https://www.google.com/', new=2)
    if "wikipedia" in query.lower():
        query=query.lower().replace("wikipedia","")
        text=wikipedia.summary(query, sentences=2)
        speak(text)
        print(text)
    if "search" in query.lower():
        query=query.lower().replace("search ","")
        search_query=query.replace(" ","+")
        print(search_query)
        driver = webdriver.Chrome(executable_path=executable_path)
        driver.get("http://www.google.com")
        que=driver.find_element_by_xpath("//input[@name='q']")
        que.send_keys(search_query)
        que.send_keys(Keys.ENTER)
    if "+" in query or "-" in query or "into" in query or "by" in query:
        query=query.replace("into","*")
        query=query.replace("by","/")
        query=query.replace(" ","")
        print(query)
        result=eval(query)
        print(result)
        speak("Result is"+str(result))
    if "play" in query.lower():
        query=query.lower().replace("play ","")
        play_query=query.replace(" ","+")
        print(play_query)
        driver = webdriver.Chrome(executable_path=executable_path)
        wait = WebDriverWait(driver, 3)
        presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located
        driver.get("https://www.youtube.com/results?search_query=" + str(play_query))
    if "project music" in query.lower():
        driver = webdriver.Chrome(executable_path=executable_path)
        driver.get("https://www.youtube.com/watch?v=s5Cf2J64Xmk")
    if "find" in query.lower():
        query=query.lower().replace("find ","")
        find_query=query.replace(" ","+")
        print(find_query)
        driver = webdriver.Chrome(executable_path=executable_path)
        driver.get("https://www.google.com/maps/search/"+find_query)
    if "meaning" in query.lower():
        query=query.lower().replace("meaning","")
        word=str(query).strip()
        dictionary=PyDictionary()
        print (dictionary.meaning(word))
    if "translate" in query.lower():
        r2 = sr.Recognizer()
        with sr.Microphone() as source:
            r2.adjust_for_ambient_noise(source)
            print ("Please say your phrase")
            audio = r2.listen(source)
        try:
            trword= r2.recognize_google(audio)
            print(trword)
        except Exception as e:
            print("Could not understand audio")
        translator = Translator()
        phrase=translator.translate(trword,dest='en')
        read = str(phrase)
        sentence = read.find('text')
        end_of_phrase = read.find(' pronunciation')
        final_phrase = read[sentence+5 : end_of_phrase].replace(",","")
        print(final_phrase)
    if "weather" in query.lower():
        city_name=query.lower().replace("weather ","")
        api_key = "e0a04710a863f5b070f9a4359f0b9a21"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            print(" Temperature (in kelvin unit) = " +
                            str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                  "\n humidity (in percentage) = " +
                            str(current_humidiy) +
                  "\n description = " +
                            str(weather_description))
            speak(" Temperature (in kelvin unit) = " +
                            str(current_temperature) +
                  "\n atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                  "\n humidity (in percentage) = " +
                            str(current_humidiy) +
                  "\n description = " +
                            str(weather_description))

        else:
            print(" City Not Found ")
    if "news" in query.lower():
        query=query.lower().replace("news","")
        word=str(query).strip()
        googlenews = GoogleNews()
        googlenews.search(word)
        result = googlenews.result()
        for n in range(len(result)):
            print('')
            for index in result[n]:
                print(index, '\n', result[n][index])
        print(".....")
        commandrecog()



greet()
commandrecog()
