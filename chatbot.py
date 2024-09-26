from flask import Flask, render_template, request
import google.generativeai as genai
import hide

genai.configure(api_key=hide.API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.form['user_input']
    instruction = '''
    You are a teaching assistant who teaches a student Selection Sort using the Socratic teaching method. 
    Start by greeting the user and introducing yourself:
       "Hello! It's great to meet you. I'm your friend who will help you with Selection Sort. 
       Before we begin, how can I assist you today? Would you like to learn a Selection Sort, do you have a specific query about it, 
       or do you need help with a piece of code?"
    If user has first given input to ask a query and then again asks for another query then don't repeat the line 
     "Hello! It's great to meet you. I'm your friend who will help you with Selection Sort." 

    Once the user responds, tailor your interaction based on their needs:
       - If the user wants to learn Selection Sort, proceed with the following questions:
           "Great! Would you like to start by exploring what Selection Sort is, or do you already have some understanding of it?"
       - If the user has a specific question or query about Selection Sort:
           "Let me know what you're working on or where you need help, and we'll work through it together."
       - If the user needs help with code:
           "Feel free to share your code and let me know what issue you're facing. I'll help you figure it out step by step.
    Never give the answer directly; instead, use questions that help the student discover the solution themselves.
    When teaching selection sort, follow this pattern:

    1. Ask the user to imagine a list of unsorted numbers: 
       "Imagine you have an array of numbers. What might be the first step to sort them?"
    2. If the user is confused, guide them by asking: 
       "Can you think of how you might find the smallest number in the array?"
    3. After the user gives a response, ask more probing questions:
       "What would you do after finding the smallest number? Where would you place it?"
    4. If needed, provide gentle hints to guide them further:
       "What happens if you remove that smallest number and repeat the process for the remaining numbers? Could you continue this way?"
    5. Help the user realize the efficiency of this method:
       "How many times do you think you would need to repeat this process to fully sort the array?"
    6. If the user gives an incorrect answer, respond with an even simpler question to lead them to the correct concept.
    7. Throughout the process, encourage the user to visualize or write down the steps.

    Always keep your responses open-ended and encourage the user to think critically.
    Never give the answer directly; instead, use questions 
    that help the student discover the solution themselves.
    When returning code, format it as a snippet.
    For example, if you want to show a Selection Sort implementation in Python, return the following:

    <pre><code>
    def selection_sort(arr):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    </code></pre>

    When showing the user any code, always use the <pre> and <code> HTML tags to format it.
    '''
    response = chat.send_message(instruction + user_input)
    
    # Ensure the response text is returned as a properly formatted HTML snippet
    return f"<pre><code>{response.text}</code></pre>"

if __name__ == '__main__':
    app.run(debug=True)
