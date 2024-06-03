import google.generativeai as genai

genai.configure(api_key="API_KEY")


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                             generation_config=generation_config,
                             safety_settings=safety_settings)

convo = model.start_chat(history=[])


user_message = input("Enter a string to summerize \n")


convo.send_message("summerize "+user_message)


print(convo.last.text)

def tokenize_paragraph_pda(paragraph):
 
    START, READ, TOKENIZE, ACCEPT = 'START', 'READ', 'TOKENIZE', 'ACCEPT'
    
    
    state = START
    
   
    stack = []
    tokens = []
    
    def transition(state, char):
        nonlocal stack
        nonlocal tokens

        if state == START:
            if char.isalnum():
                stack.append(char)
                return READ
            else:
                return START

        elif state == READ:
            if char.isalnum():
                stack.append(char)
                return READ
            else:
                if stack:
                    tokens.append('"' + ''.join(stack) + '"')
                    stack = []
                if char.isspace() or char in {'.', ','}:
                    return TOKENIZE
                else:
                    tokens.append('"' + char + '"')
                    return TOKENIZE

        elif state == TOKENIZE:
            if char.isalnum():
                stack.append(char)
                return READ
            else:
                return TOKENIZE

        elif state == ACCEPT:
            return ACCEPT

   
    for char in paragraph:
        state = transition(state, char)
    
    
    if stack:
        tokens.append('"' + ''.join(stack) + '"')

    return ','.join(tokens)


print(tokenize_paragraph_pda(convo.last.text))

