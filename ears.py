from speechrecognition import SpeechRecognition

class Ears:
  def __init__(self, speechrecognition: SpeechRecognition):
    self.speechrecognition = speechrecognition

  def listen(self):
    return self.speechrecognition.listen()