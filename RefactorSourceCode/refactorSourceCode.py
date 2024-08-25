# Libraries
import openai
import time
import os
import subprocess
from dotenv import load_dotenv, find_dotenv

# ChatGPT credentials
# openai_version = "gpt-3.5-turbo"
openai_version = "gpt-4-turbo"
_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

# Setting rules
delimiter = "###"
rules  = "{delimiter} RULE 01 - Only C code refactoring is allowed. \n"
rules += "{delimiter} RULE 02 - Refactored code must be human readable as much as possible.\n"
rules += "{delimiter} RULE 03 - Best clean code pratices must be used.\n"
rules += "{delimiter} RULE 04 - Refactored code must NOT increase code complexity.\n"
rules += "{delimiter} RULE 05 - Data type must be defined to all variables.\n"
rules += "{delimiter} RULE 06 - Misleading variables name must be renamed.\n"
rules += "{delimiter} RULE 07 - Refactor code must NOT exceed 2000 characters.\n"
rules += "{delimiter} RULE 08 - Explain the refactor code. Keep it short.\n"
rules += "{delimiter} RULE 09 - Variables names must follow Camelcase format.\n"
rules += "{delimiter} RULE 10 - The indentation shall be 2 spaces per logical level.\n"
rules += "{delimiter} RULE 11 - The indentation of preprocessor directives shall be 2 spaces per logical level after the hash # symbol.\n \
                    The indentation shall start at column 0 and shall not follow the code indentation.\n"
rules += "{delimiter} RULE 12 - Always use spaces instead of tabs.\n"
rules += "{delimiter} RULE 13 - There shall be no space between ‘;’ and the code before it.\n"
rules += "{delimiter} RULE 14 - There shall be no space between the function name and the ‘(‘.\n"
rules += "{delimiter} RULE 15 - There shall be no space between variable pointer type and the asteris *.\n"
rules += "{delimiter} RULE 16 - There shall be no space between the asterisk and the function pointer name in the declaration.\n"
rules += "{delimiter} RULE 17 - All comments shall be written in English (en-US) language. \n"
rules += "{delimiter} RULE 18 - Return values must be compatible to the data type of the function. \n"
rules += "{delimiter} RULE 19 - Comments must NOT be removed. \n"
rules += "{delimiter} RULE 20 - Variables declaration not used by the code must be removed.\n"
rules += "{delimiter} RULE 21 - Function´s arguments not used by the code must be removed.\n"
rules += "{delimiter} RULE 22 - Functions must contain a short comment explanation.\n"
rules += "{delimiter} RULE 23 - Boolean variables must be hbl_bool type with HBL_FALSE or HBL_TRUE values.\n"
rules += "{delimiter} RULE 24 - Do not add or change any library.\n"


# system_message = f'''You are an expert embedded software engineer! \
#                      Your main goal is to refactor source code in C.
#                      There are restricts rules delimited by {delimiter} character \
#                      you must follow: {rules} \
#                      When you finish it, you must go throught your response \
#                      and check if it meet all the given rules. '''

system_message = f'''You are a expert to refactor source code in C.
                     Therefore, you must follow some rules delimited by {delimiter} characters: {rules} \
                     Write the refactor C code based on the rules. '''

# remove unused variables
def remove_unused_variables(code):
    with open('temp_code.c', 'w') as f:
        f.write(code)
    
    result = subprocess.run(['clang-tidy', 'temp_code.c', '--checks=-*,clang-analyzer-deadcode.DeadStores', '--', '-fno-color-diagnostics'], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    
    unused_vars = []
    for line in lines:
        if 'warning' in line and 'never read' in line:
            parts = line.split()
            var_name = parts[-1].strip('\'')
            unused_vars.append(var_name)
    
    os.remove('temp_code.c')
    return unused_vars

# Request to generate response using openAI API
def generateResponse(user_message):
        for i in range(3): # retries to connect
            try:
                response = openai.ChatCompletion.create(
                    model=openai_version,
                    messages=[
                         {"role": "system", "content": system_message},
                         {"role": "user", "content": user_message}
                    ],
                    max_tokens=2000, # around 1500 words
                    n=1,
                    stop=None,
                    temperature=0.9
                )
                refactored_code = response['choices'][0]['message']['content'].strip()
                return refactored_code.replace("```c", "").replace("```", "")
            
            except:
                print("\n Trying to connect ...\n")
                time.sleep(1)

def get_user_input():
        # Collect multi-line C code input from the user
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'GO':
                break
            lines.append(line)
        user_input = "\n".join(lines)

        return user_input

def run_c_code_refactor():
    # print("How to use it? ")
    # print("   1 - Enter the C source code to be refactored; ")
    # print("   2 - Type GO to start the process; \n")
    # print("...\n")
    print(">>> enter your C code, then type GO to start: \n\n")
    
    # Get original source code
    source_code = get_user_input()

    # # Remove unused variable
    # unused_vars = remove_unused_variables(source_code)
    # print(unused_vars)

    # Run AI process
    while(1):
        print("\n\n")
        print(">>> AI response: \n")
        refactored_code = str(generateResponse(source_code))

        print(refactored_code)
        print("\n")

        new_refactoring = input("Do it again? (y/n)")
        if (new_refactoring.lower() != "y"): break

# Talking to chatGPT-3
if __name__ == "__main__":

    print("\n----------------- AI Code Refactor -----------------\n")
    # print("Refactoring general rules: \n", rules)
    run_c_code_refactor()
    print("\n-----------------------------------------------------\n")
    
    while(1):
         pass # keep terminal open in order to keep the refactor code on the screen.




# static void OnEventChangedEvent(uint8_t event, uint8_t id)
# {
#   // Essa rotina atualiza novos limites sempre que necessario.
   
#    uint32_t test = 0;
#    hbl_bool isTrue;

#   if (HBL_TRUE == IsSignedValueInRange(event.data, 1, MAX_VALUE))
#   {
#     plugin.event = (uint8_t)event.data; // Copia o dado para o evento.
#     if (GetState(&plugin.state_machien ) == STATE_A) 
#     {
#             PublishNewLimits()  ; // Publish all the new limits
#     }
#   }
  
#   return False;
# }

