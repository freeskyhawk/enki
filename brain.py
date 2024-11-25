import keyboard
import pyautogui
import webbrowser
from time import sleep
from threading import Thread
from threading import RLock

from openaigpt import ChatGpt
from openaiwhisper import Whisper
from googlegemini import Gemini
from openweather import Weather
from mouth import Mouth
from ears import Ears
from eyes import Eyes
from hands import Hands

class Brain:
  def __init__(self, creator, name: str, mouth: Mouth, ears: Ears, eyes: Eyes, hands: Hands, multiLinguistic: bool, whisper: Whisper, chatGpt: ChatGpt, gemini: Gemini, weather: Weather, pickupFolder: str):
    self.creator = creator
    self.name = name
    self.mouth = mouth
    self.ears = ears
    self.eyes = eyes
    self.hands = hands
    self.multiLinguistic = multiLinguistic
    self.whisper = whisper
    self.chatGpt = chatGpt
    self.gemini = gemini
    self.weather = weather
    self.pickupFolder = pickupFolder
    f = open(f"{self.pickupFolder}/uploaded_video_id.txt", "r")
    self.uploaded_video_id = f.read()
    f.close
    self.messages = [{"role": "system", "content": "You are a helpfull and loyal assistant."}]
    self.activationText = f"{self.name.lower()} "
    self.awake = True
    self.lock = RLock()

  def startProcessing(self):
    self.sightThread = Thread(target=self.eyes.watch, args=(self.lock,))
    self.sightThread.start()

    # self.handsThread = Thread(target=self.hands.captureHandsGestures, args=(self.lock,))
    # self.handsThread.start()

  def getSensessInput(self):
    speechText = self.getSpeechText()
    facesInSight = self.getFacesInView()
    return {"speechText": speechText, "facesInSight": facesInSight}
  
  def getFacesInView(self):
    self.lock.acquire()
    facesInSight = self.eyes.getInSightFaces().copy()
    print(f"I see the following faces {facesInSight}\n")
    self.lock.release()
    return facesInSight
  
  def isCreatorInSight(self, facesInSight):
    creatorInSight = False
    for face in facesInSight:
      n = face["name"]
      p = face["prediction"]
      if ((n == self.creator) & (p > 0.6)):
          creatorInSight = True
          break
    return creatorInSight

  def canProcessSensess(self):
    sensessInput = self.getSensessInput()
    originalText = sensessInput["speechText"]
    creatorInSight = self.isCreatorInSight(sensessInput["facesInSight"])
    print(f"creatorInSight({creatorInSight})\n")
    text = originalText.lower().strip()
    if (text.startswith(self.activationText)):
      questionText = text.replace(self.activationText, "")
      if self.isCommand(questionText):
          if creatorInSight:
              if ("terminate yourself" == questionText):
                  self.eyes.closeEyes()
                  self.hands.stopCaptureHandsGestures()
                  self.mouth.say("Oh No I Died")
                  return False
              elif (self.awake & ("sleep" == questionText)):
                  self.awake = False
                  print("\nI slept..Zzz.")
              elif ("wake up" == questionText):
                  if self.awake:
                      alreadyAwake = "I'm already awake..."
                      print(f"\n{alreadyAwake}")
                      self.mouth.say(alreadyAwake)
                  else:
                      self.awake = True
                      wookeUp = "I woke up, how can I help you?"
                      print(f"\n{wookeUp}")
                      self.mouth.say(wookeUp)
              elif (self.awake & ("start capture hands" == questionText)):
                  self.handsThread = Thread(target=self.hands.startCaptureHandsGestures, args=(self.lock,))
                  self.handsThread.start()
              elif (self.awake & ("stop capture hands" == questionText)):
                  self.hands.stopCaptureHandsGestures()
              elif (self.awake & ("upload the video" == questionText)):
                  self.uploaded_video_id = self.gemini.uploadVideo(f"{self.pickupFolder}/video_001.mp4")
                  f = open(f"{self.pickupFolder}/uploaded_video_id.txt", "w")
                  f.write(self.uploaded_video_id)
                  f.close()
              elif (self.awake & questionText.startswith("visit ")):
                  siteToVisit = questionText.replace("visit ", "")
                  postFix = ""
                  if siteToVisit.rfind(".") == -1:
                      postFix = ".com"
                  link = f"https://www.{siteToVisit}{postFix}"
                  webbrowser.open(link)
                  sleep(1)
              elif (self.awake & questionText.startswith("open ")):
                  programToOpen = questionText.replace("open ", "")
                  pyautogui.press("win")
                  sleep(1)
                  keyboard.write(programToOpen)
                  sleep(1)
                  keyboard.press("enter")
                  sleep(1)
          else:
            self.mouth.say(f"My creator ({self.creator}) is not in sight, therefore I will not perform any commands, I will answer questions though!")
      elif (self.awake):
          if self.canHandleAsWeatherQuestion(questionText):
              return True
          elif (questionText.startswith("image question ")):
              imageQuestion = questionText.replace("image question ", "")
              answer = self.gemini.answerQuestionAboutImage(imageQuestion, f"{self.pickupFolder}/image.jpg")
              print(answer)
              self.mouth.say(answer)
          elif (questionText.startswith("audio question ")):
              audioQuestion = questionText.replace("audio question ", "")
              answer = self.gemini.answerQuestionAboutAudio(audioQuestion, f"{self.pickupFolder}/audio.mp3")
              print(answer)
              self.mouth.say(answer)
          elif (questionText.startswith("video question ")):
              audioQuestion = questionText.replace("video question ", "")
              answer = self.gemini.answerQuestionAboutVideo(audioQuestion, self.uploaded_video_id)
              print(answer)
              self.mouth.say(answer)
          elif (questionText.startswith("summary video question ")):
              videoQuestion = questionText.replace("summary video question ", "")
              video_answer_file = f"{self.pickupFolder}/video_answer.html"
              self.gemini.answerQuestionAboutVideoHtmlOutput(videoQuestion, self.uploaded_video_id, video_answer_file)
              webbrowser.open(f"file:{video_answer_file}")
          else:
            #  response = self.chatGpt.askChatGpt(questionText, self.messages)
            answer = self.gemini.answerQuestion(questionText)
            print(answer)
            self.mouth.say(answer)
    return True
  
  def canHandleAsWeatherQuestion(self, questionText):
    if (questionText.startswith("tell me the weather in ")):
        weatherQuestion = questionText.replace("tell me the weather in ", "")
        self.processWeatherQuestion(weatherQuestion)
        return True
    elif (questionText.startswith("what is the weather in ")):
        weatherQuestion = questionText.replace("what is the weather in ", "")
        self.processWeatherQuestion(weatherQuestion)
        return True
    elif (questionText.startswith("how is the weather in ")):
        weatherQuestion = questionText.replace("how is the weather in ", "")
        self.processWeatherQuestion(weatherQuestion)
        return True
    elif (questionText.startswith("describe the weather today in ")):
        weatherQuestion = questionText.replace("describe the weather today in ", "")
        self.processWeatherPartQuestion(weatherQuestion, "description")
        return True
    elif (questionText.startswith("what is the temperature in ")):
        weatherQuestion = questionText.replace("what is the temperature in ", "")
        self.processWeatherPartQuestion(weatherQuestion, "temperature")
        return True
    elif (questionText.startswith("what is the humidity in ")):
        weatherQuestion = questionText.replace("what is the humidity in ", "")
        self.processWeatherPartQuestion(weatherQuestion, "humidity")
        return True
    elif (questionText.startswith("what is the wind speed in ")):
        weatherQuestion = questionText.replace("what is the wind speed in ", "")
        self.processWeatherPartQuestion(weatherQuestion, "wind speed")
        return True
    else:
        return False

  def processWeatherQuestion(self, weatherQuestion):
    city = weatherQuestion.replace(".", "")
    weatherCast = self.weather.retrieveWeatherForecast(city)
    print(weatherCast)
    self.mouth.say(weatherCast)

  def processWeatherPartQuestion(self, weatherQuestion, weatherPart):
    city = weatherQuestion.replace(".", "")
    weatherCast = self.weather.retrieveWeatherForecastPart(city, weatherPart)
    print(weatherCast)
    self.mouth.say(weatherCast)

  def isCommand(self, questionText):
    return ("terminate yourself" == questionText) | \
           ("sleep" == questionText) | \
           ("wake up" == questionText) | \
           ("start capture hands" == questionText) | \
           ("stop capture hands" == questionText) | \
           ("upload the video" == questionText) | \
           questionText.startswith("visit ") | \
           questionText.startswith("open ")
  
  def getSpeechText(self):
      print("\nListening...")
      speechText = ""
      while speechText == "":
          audio = self.ears.listen()
          speechText = self.audioToText(audio)
      print(f"\nUsing ({speechText}) as input")
      return speechText

  def audioToText(self, audio):
    text = ""
    if self.multiLinguistic:
        result = self.whisper.audioToTextLocalWhisper(audio)
        language = result["language"]
        text = result["text"]
        if (text != "") & (language != "en"):
            audioFile = result["audioFile"]
            translatedText = self.whisper.audioToTranslatedTextLocalWhisper(audioFile)
            print(f"\nTranslated ({text}) in ({language}) to ({translatedText}) in (en)")
            text = translatedText
    else:
      text = self.ears.speechrecognition.audioToText_recognize_google(audio)
    return text
    
    # return self.whisper.audioToText_local_whisper(audio)
    # return self.whisper.audioToText_remote_whisper(audio)