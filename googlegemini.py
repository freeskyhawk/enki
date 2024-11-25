from multipledispatch import dispatch
import google.generativeai as genai
import time
import PIL.Image
import pathlib
import markdown

from speechrecognition import SpeechRecognition

class Gemini:
  def __init__(self, gemini_api_key):
    self.name = "Gemini"
    self.description = "Google generative AI"
    self.gemini_api_key = gemini_api_key
    genai.configure(api_key=self.gemini_api_key)
    self.genai = genai
    self.model = genai.GenerativeModel("gemini-1.5-flash")
    audioCaptureDeviceIndex = 0
    self.sr = SpeechRecognition(audioCaptureDeviceIndex)

  def __str__(self):
    return f"{self.name}({self.description})"

  def answerQuestion(self, question):
    # print("Question: " + question)
    response = self.model.generate_content(question)
    # print("Answer: " + response.text)
    return response.text

  def answerQuestionAboutImage(self, question, image):
    # print("Question: " + question)
    img = PIL.Image.open(image)
    response = self.model.generate_content([question, img])
    # print("Answer: " + response.text)
    return response.text

  def answerQuestionAboutAudio(self, question, audio):
    # print("Question: " + question)
    response = self.model.generate_content([
      question,
      {
        "mime_type": "audio/mp3",
        "data": pathlib.Path(audio).read_bytes()
      }
    ])
    # print("Answer: " + response.text)
    return response.text
  
  def answerQuestionAboutVideo(self, question, video):
    # print("Question: " + question)
    video_file = self.genai.get_file(video)
    response = self.model.generate_content(
      [video_file, question],
      request_options={"timeout": 600})
    # print("Answer: " + response.text)
    return response.text
  
  def answerQuestionAboutVideoHtmlOutput(self, question, video, video_answer_file):
    # print("Question: " + question)
    video_file = self.genai.get_file(video)
    response = self.model.generate_content(
      [video_file, question],
      request_options={"timeout": 600})
    html = markdown.markdown(response.text)
    # print(html)
    # video_answer_file = "/Users/hallo/Desktop/media/video_answer.html"
    f = open(video_answer_file, "w")
    f.write(f"<p>Question: {question}</p>\n{html}")
    f.close()
    return html
    webbrowser.open(f"file:///C:{video_answer_file}")

  def uploadVideo(self, video):
    print(f"Uploading file...")
    video_file = self.genai.upload_file(path=video)
    print(f"Completed upload (file.uri): {video_file.uri}")
    print(f"Completed upload (file.name): {video_file.name}")
    # Check whether the file is ready to be used.
    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = self.genai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
      raise ValueError(video_file.state.name)
    return video_file.name
    
  def getSpeechText(self):
    print("\nListening...")
    speechText = ""
    while speechText == "":
      audio = self.sr.listen()
      response = self.model.generate_content(
        ["Please convert the audio to text",
         {"mime_type": "audio/wav",
          "data": audio.get_wav_data()
         }])
      speechText = response.text
    print(f"\nGemini recognized ({speechText}) as input")
    return speechText