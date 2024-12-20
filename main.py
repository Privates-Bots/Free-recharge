from fastapi import FastAPI, Query
from transformers import AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

# Load a pre-trained model from Hugging Face
model_name = "gpt2"  # You can use larger models like GPT-Neo for better responses
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.get("/gpt4")
async def chat_gpt4(id: str = Query(...), question: str = Query(...)):
    """
    Handles user queries using an open-source GPT model.
    """
    try:
        # Tokenize the input
        inputs = tokenizer.encode(question, return_tensors="pt")

        # Generate response
        outputs = model.generate(inputs, max_length=200, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {"id": id, "question": question, "answer": answer}

    except Exception as e:
        return {"error": str(e)}
