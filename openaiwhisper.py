import openai
import whisper

from mouth import Mouth

class Whisper:
  def __init__(self, openai_api_key):
        self.openai = openai
        self.openai.api_key = openai_api_key
        self.wmodel = whisper.load_model("base")
        # self.speek = Mouth(1)

  def audioToTextLocalWhisper(self, audio):
      text = ""
      audioFile = "audio.wav"
      try:
          with open(audioFile, "wb") as f:
              f.write(audio.get_wav_data())
  
          result = self.wmodel.transcribe(audioFile) #, verbose = True)
  
          text = result["text"]
          language = result["language"]
          print(f"\n({text}) detected language ({language})\n")
      except Exception as e:
          print(e)
      return {"text": text, "language": language, "audioFile": audioFile}
  
  def audioToTranslatedTextLocalWhisper(self, audioFile):
      try:
        task = "translate" # Default is "transcribe"
        result = self.wmodel.transcribe(audioFile, task = task)
        translatedText = result["text"]
        # translation_feedback = f"Sir I have translated ({user_input}) into ({translated_user_input})"
        # print(f"\n{translation_feedback}\n")
        # self.speek.say(translation_feedback)
      except Exception as e:
          print(e)
      return translatedText
  
  def audioToText_local_whisper(self, audio):
      user_input = ""
      try:
          with open("audio.wav", "wb") as f:
              f.write(audio.get_wav_data())
  
          result = self.wmodel.transcribe(
              "audio.wav") #, verbose = True)
  
          user_input = result["text"]
          user_input_language = result["language"]
          print(f"\n({user_input}) detected language ({user_input_language})\n")
  
          if user_input_language != "en":
              task = "translate" # Default is "transcribe"
              result = self.wmodel.transcribe("audio.wav", task = task)
              translated_user_input = result["text"]
              translation_feedback = f"Sir I have translated ({user_input}) into ({translated_user_input})"
              print(f"\n{translation_feedback}\n")
            #   self.speek.say(translation_feedback)
      except Exception as e:
          print(e)
      return user_input
  
  def audioToText_remote_whisper(self, audio):
      user_input = ""
      try:
          with open("audio.wav", "wb") as f:
              f.write(audio.get_wav_data())
          audioFile = open("audio.wav", "rb")
  
          result = openai.Audio.transcribe(
              model = "whisper-1",
              file = audioFile
          )
  
          user_input = result["text"]
          user_input_language = result["language"]
          print(f"\n({user_input}) detected language ({user_input_language})\n")
  
          if user_input_language != "en":
              task = "translate" # Default is "transcribe"
              result = openai.Audio.transcribe(
                  "audio.wav",
                  task = task)
              
              translated_user_input = result["text"]
              print(f"\n({translated_user_input}) translation from ({user_input_language})\n")
            #   self.speek.say("Sir, you said " + translated_user_input + " in (" + user_input_language + ")")
      except Exception as e:
          print(e)
      return user_input