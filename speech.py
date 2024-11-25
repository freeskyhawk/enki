import pyttsx3

class Speech:
  def __init__(self, gender):
    self.engine = pyttsx3.init()
    self.voices = self.engine.getProperty("voices")
    self.engine.setProperty("voice", self.voices[gender].id)

  def getEngine(self):
    return self.engine