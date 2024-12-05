from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the Llama model and tokenizer

# model_name = "meta-llama/Llama-3.2-1B-Instruct"
# tokenizer = AutoTokenizer.from_pretrained(model_name, token = llama_token)
# model = AutoModelForCausalLM.from_pretrained(model_name, token = llama_token)


def load_story_model():
    
    """Loads and returns the Llama story generation model."""
    llama_token = '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'
    model_name = "meta-llama/Llama-3.2-1B-Instruct"
    print(f"Loading story model: {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, token = llama_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, token = llama_token, device_map="auto")
    
    print("Story model loaded successfully!")
    return {"model": model, "tokenizer": tokenizer}


def generate_story(data, model):

    tokenizer = model["tokenizer"]
    lm = model["model"]

    prompt = (
        f"Write a short story readable by a 6 yearsl old child in 4 paragraphs of 50 words each:\n\n"
        f"Characters description: {', '.join(data['characters'])}.\n"
        f"World: {data['setting']}.\n"
        f"Action: {data['action']}.\n"
        f"Ending: {data['ending']}.\n\n"
        f"Story:\n"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt").to(lm.device)
    outputs = lm.generate(
        inputs["input_ids"],
        max_length=250,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        temperature=0.5,
        top_p=0.9,
    )
    
    story = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Split the story into 4 pages (1 sentence per page)
    sentences = story.split(". ")
    pages = [{"text": sentence.strip()} for sentence in sentences[:4]]
    return pages

if __name__ == "__main__":
    model = load_story_model()
    print(generate_story({
        "characters": ["Nael", "Naim"],
        "setting": "space",
        "action": "fighting",
        "ending": "happy"
    }, model))