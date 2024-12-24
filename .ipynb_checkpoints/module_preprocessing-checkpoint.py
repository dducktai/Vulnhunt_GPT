import os
import google.generativeai as genai

def configure_api(api_key: str):
    genai.configure(api_key=api_key)

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

def extract_solidity_code(model, user_input: str) -> str:
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
    response = chat_session.send_message(user_input)
    response_text = response.text.strip()

    # Loại bỏ markdown
    if response_text.startswith("```solidity"):
        response_text = response_text[len("```solidity"):].strip()
    if response_text.endswith("```"):
        response_text = response_text[:-3].strip()
    
    return response_text

def save_to_file(content: str, folder_name="solidity", file_name="clean_prompt_from_user.txt"):
    folder_path = os.path.join(folder_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    return file_path
