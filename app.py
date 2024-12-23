from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cohere
import os
app = Flask(__name__)
CORS(app)
cohere_api_key = os.environ.get("COHERE_API_KEY")

# Set your Cohere API key
cohere_client = cohere.Client(cohere_api_key)  # Replace with your API key

# Load resume text
with open("data/resume.txt", "r") as file:
    resume_text = file.read()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Cohere Chatbot API!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the question from the request
        data = request.json
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "A question is required!"}), 400

        # Define the prompt
        prompt = f"""
        You are Ayushkumar Variyava, a software developer. Answer the user's questions strictly based on the following resume.
        Keep the responses short, direct, and within the context of the resume. Avoid giving suggestions or professional advice.
        You are allowed to engage in friendly greetings like "hi" or "hello", but for unrelated questions, reply with:
        'I can only answer questions related to the resume provided.'

        Resume:
        {resume_text}

        Question:
        {question}

        Answer:
        """

        # Generate response
        def generate_stream():
            stream = cohere_client.chat_stream(
                model="command-r-08-2024",
                message=prompt,
                temperature=0.3,  # Focused and concise responses
                chat_history=[],
                prompt_truncation="AUTO"
            )
            for event in stream:
                if event.event_type == "text-generation":
                    yield event.text

        # Return a streaming response
        return Response(generate_stream(), content_type="text/plain")

    except Exception as e:
        # Return error as JSON
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
