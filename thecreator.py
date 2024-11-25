import os

from speech import Speech
from speechrecognition import SpeechRecognition
from openaigpt import ChatGpt
from openaiwhisper import Whisper
from googlegemini import Gemini
from openweather import Weather

from mouth import Mouth
from ears import Ears
from eyes import Eyes
from hands import Hands
from brain import Brain
from human import Human

class TheCreator:
  def __init__(self):
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.gemini_api_key = os.environ["GEMINI_API_KEY"]
        self.openweather_api_key = os.environ["OPENWEATHER_API_KEY"]
        self.keras_model = os.environ["ENKI_KERAS_MODEL"]
        self.pickup_folder = os.environ["ENKI_PICKUP_FOLDER"]
        self.whisper = Whisper(self.openai_api_key)
        self.chatGpt = ChatGpt(self.openai_api_key)
        self.gemini = Gemini(self.gemini_api_key)
        self.weather = Weather(self.openweather_api_key)
  
  def createHuman(self):
    name = str(input("Enter Human AI Name: "))
    gender = int(input("Enter Human AI Gender (0 for male, 1 for female): "))
    multiLinguistic = bool(int(input("Human AI is multi linguistic (0 for No, 1 for Yes): ")))
    creator = "Hallo"
    audioCaptureDeviceIndex = 0
    faceVideoCaptureDeviceIndex = 1
    handsVideoCaptureDeviceIndex =0
    mouth = Mouth(Speech(gender).getEngine())
    ears = Ears(SpeechRecognition(audioCaptureDeviceIndex))
    eyes = Eyes(faceVideoCaptureDeviceIndex, self.keras_model)
    hands = Hands(handsVideoCaptureDeviceIndex)
    brain = Brain(creator, name, mouth, ears, eyes, hands, multiLinguistic, self.whisper, self.chatGpt, self.gemini, self.weather, self.pickup_folder)
    return Human(creator, name, gender, brain)

TheCreator().createHuman().live()