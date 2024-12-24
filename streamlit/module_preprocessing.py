import os
import google.generativeai as genai
import sys

def configure_api(api_key):
    genai.configure(api_key="AIzaSyBPprZiNSgAKuWeUqqE56kml1248z4dsTY")

def create_model():
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    return model

def get_user_input():
    print("Paste your code and press Ctrl+D (or Ctrl+Z on Windows) to finish:")
    user_input = sys.stdin.read()
    return user_input

def start_chat_session(model, user_input):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Extract the pure Solidity code from the following text, removing all comments, explanations, and non-code content:\n\n" + user_input,
                ],
            }
        ]
    )
    return chat_session
# Gửi tin nhắn tới API
def send_message(chat_session, user_input):
    response = chat_session.send_message(user_input)
    return response

# Xử lý đầu ra
def process_response(response):
    response_text = response.text.strip()

    # Loại bỏ markdown ` ```solidity` và ` ``` `
    if response_text.startswith("```solidity"):
        response_text = response_text[len("```solidity"):].strip()
    if response_text.endswith("```"):
        response_text = response_text[:-3].strip()

    # Định dạng lại đầu ra để có dạng giống như mong muốn
    formatted_response = response_text.replace("\n", " \\n\\n\\").replace(" \\n\\n\\", " \\n\\\n")
    return formatted_response

def save_response(formatted_response, folder_path="solidity", file_name="streamlit_clean_prompt_from_user.txt"):
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Save the response into a text file
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(formatted_response)

    print("\n -------- \n ")
    print(f"Response saved to {file_path}")