import openai

class ChatGpt:
  def __init__(self, openai_api_key):
        self.openai = openai
        self.openai.api_key = openai_api_key
         
  def askChatGpt(self, question, conversation):
        conversation.append({"role": "user", "content": question})
    
        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.8
            )
    
        response = completion.choices[0].message.content
        conversation.append({"role": "assistant", "content": response})
        print(f"\n{response}\n")
        return response