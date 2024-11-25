from brain import Brain

class Human:
  def __init__(self, creator: str, name: str, gender: int, brain: Brain):
      self.creator = creator
      self.name = name
      self.gender = gender
      self.brain = brain
      print(f"\nI am a Human {self.intToGender(gender)} AI, my name is ({name}).\n{creator} created me as a loyal AI assistant")
  
  def intToGender(self, gender: int):
      if (gender == 0):
          return "male"
      else:
          return "female"
      
  def live(self):
      print("\nI'm alive")
      self.brain.startProcessing()
      while self.brain.canProcessSensess():
          continue
      self.die()
  
  def die(self):
      print("\nOh No I Died")
