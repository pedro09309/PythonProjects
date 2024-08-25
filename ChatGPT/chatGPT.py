# # Libraries
import openai

from openai import get 
# import time
import os
from dotenv import load_dotenv, find_dotenv

# Read local open ai api key
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['OPENAI_API_KEY']

# Set ChatGPT key
openai.api_key = openai_api_key

# Request to generate response using openAI API
def generateResponse(prompt):
        for i in range(3): # retries to connect
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                         {"role": "system", "content": "You are a helpful assistant."},
                         {"role": "user", "content": prompt}
                    ],
                    max_tokens=200, # around 150 words
                    n=1,
                    stop=None,
                    temperature=0.7
                )
                return response['choices'][0]['message']['content']
            
            except:
                print("\n Trying to connect ...\n")
                time.sleep(0.5)

# Talking to chatGPT-3
if __name__ == "__main__":
    print("\n----------------- ChatGPT 3.5 Turbo -----------------\n")

    while(1):
        inputMessage = input("  Input: ")

        if (inputMessage != ""): print("ChatGPT: " + str(generateResponse(inputMessage)) + " \n")
        else                   : break

    print("\n------------------------------------------------------\n")