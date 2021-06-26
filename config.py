# from google import PrintAllContacts
import speech_recognition as sr
import pywhatkit as kit 
import pyttsx3
from myGoogleApi import getContacts
from datetime import datetime


engine = pyttsx3.init()

# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
# engine.setProperty('rate', 195)  

voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male

name = 'alexa'

def talk (text):
    engine.say(text)
    engine.runAndWait()


listener = sr.Recognizer()
def listen(title, firstCall = True):
  try:
      with sr.Microphone() as source:
          source.RECORD_SECONDS = 5
          talk(title)
          listener.adjust_for_ambient_noise(source)
          voices = listener.listen(source)
          rec = listener.recognize_google(voices, language="es-Es")
          rec = rec.lower()
          if name in rec and firstCall:
              rec = rec.replace(name,'')
              return {'err': False, 'text': rec}
          elif not firstCall:
              return {'err': False, 'text': rec} 
  except:
    # talk('No comprendi lo que dijistes')
    pass
  return {'err': True, 'text': ''} 



def sendWhat(person):

  phoneNumber = person['number'].replace(' ', '-').replace('-', '')
  menssage = listen('Que mensaje quieres mandar?')
  date = datetime.now().strftime('%H %M')
  date = date.split()
  kit.sendwhatmsg(phoneNumber, menssage, int(date[0]), int(date[1])+2)


def run():
    rec = listen('Escuchando')
    if rec['err']:
      talk('No pude comprender Saliendo del programa')
      return


    if('reproduce' in rec['text']):
    
        music = rec['text'].replace('reproduce', '')
        talk('reproduciendo'+ music)
        kit.playonyt(music)         
    elif 'manda' in rec:
        rec = rec['text'].replace('manda un mensaje a ', '')
        contacts = getContacts()
        possiblePerson = []

        for contact in contacts:
          personName = contact['name'].lower()
          if personName in rec:
            print(contact['name'], contact['number'])
            possiblePerson.append(contact)

        if len(possiblePerson) <= 0:
          talk('No encontre resultados para ese nombre')
        elif len(possiblePerson) > 1:

          talk('Tus contactos disponibles son: ')
          for person in possiblePerson:
            talk(person['name'])

          personToSend = listen('A cual de tus contactos se lo quieres enviar?', False)
          
          if personToSend['err']:
            talk('No pude comprender Saliendo del programa')
            return

          for person in possiblePerson['text']:
            name = person['name'].lower()
            print(personToSend)
            if name == personToSend:
              sendWhat(person)
              
        else:
          talk('mandando mensaje a ' + possiblePerson[0]['name'])
          sendWhat(possiblePerson[0])

        
        

run()