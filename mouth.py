
class Mouth:
  def __init__(self, engine):
    self.engine = engine

  def say(self, text):
    self.engine.say(text)
    self.engine.runAndWait()