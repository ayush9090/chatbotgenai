import cohere

co = cohere.Client("1JpCmhM5pMBKMkW3TfvERkbprpNw8JDEGD7S8uJm")  # Replace with your API key
models = co.list_models()

print("Available Models:")
for model in models:
    print(model.name)
