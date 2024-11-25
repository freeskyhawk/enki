import speech_recognition as sr

class SpeechRecognition:
  """ deviceIndex for example 0 to use the mic at index 0"""
  def __init__(self, deviceIndex):
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = False
        self.recognizer.energy_threshold = 4000 # 400
        self.mic = sr.Microphone(deviceIndex)

  def listen(self):
      with self.mic as source:
        self.recognizer.adjust_for_ambient_noise(source, duration = 1) #0.5
        while True:
            try:
                audio = self.recognizer.listen(source)
                return audio
            except:
                continue
          
  def audioToText_recognize_google(self, audio):
      text = ""
      try:
          text = self.recognizer.recognize_google(audio)
          return text
      except Exception as e:
          # print(e)
          return text