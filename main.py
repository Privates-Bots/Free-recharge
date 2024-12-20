from fastapi import FastAPI, Query
import openai

app = FastAPI()

# Set your OpenAI API Key (not recommended to hardcode!)
openai.api_key = "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"

@app.get("/gpt4")
async def chat_gpt4(id: str = Query(...), question: str = Query(...)):
    """
    ChatGPT-4 API endpoint to process user questions.
    """
    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )
        answer = response["choices"][0]["message"]["content"]

        return {"id": id, "question": question, "answer": answer}

    except Exception as e:
        return {"error": str(e)}
