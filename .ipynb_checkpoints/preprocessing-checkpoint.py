import os
import google.generativeai as genai



# Configure the API
genai.configure(api_key="")

# Configure the model
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

# Prompt the user for the Solidity input
user_input = input("Nhập nội dung để phân tích: ")

# Start the chat session
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

# Gửi tin nhắn tới API
response = chat_session.send_message(user_input)

# Xử lý đầu ra
response_text = response.text.strip()

# Loại bỏ markdown ` ```solidity` và ` ``` `
if response_text.startswith("```solidity"):
    response_text = response_text[len("```solidity"):].strip()
if response_text.endswith("```"):
    response_text = response_text[:-3].strip()




# Create the folder if it doesn't exist
folder_path = "solidity"
os.makedirs(folder_path, exist_ok=True)

# Save the response into a text file
file_path = os.path.join(folder_path, "clean_prompt_from_user.txt")
with open(file_path, "w", encoding="utf-8") as file:
    file.write(response_text)



print("\n -------- \n ")
print(f"Response saved to {file_path}")