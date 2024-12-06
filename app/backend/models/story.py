from transformers import AutoTokenizer, AutoModelForCausalLM

llama_token = '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'

def load_story_model():
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct", token = llama_token)
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct", token = llama_token)
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = model.config.eos_token_id

    return tokenizer, model

# Generate text based on a prompt
def generate_text(prompt, model, tokenizer, max_new_tokens=200):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, add_special_tokens=True)
    output = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=max_new_tokens,
        num_return_sequences=1,
        no_repeat_ngram_size=3,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return output_text[len(prompt):].strip()

# Main story generator function
def generate_story(characters, environment, action, ending):
    tokenizer, model = load_story_model()
    
    # Generate story components
    story_parts = []
    
    # Characters introduction (25 words each)
    for character in characters:
        prompt = (f"Write a fun introduction for a children's story character named {character}. "
                  f"Use rhyme and make it descriptive, and include how they fit into the story.")
        story_parts.append(generate_text(prompt, model, tokenizer, max_new_tokens=50))
    
    # Environment description (50 words)
    prompt = (f"Describe the work of the {environment} in a funny way for kids. "
              f"Use rhymes, colorful details, and make it fun to read.")
    story_parts.append(generate_text(prompt, model, tokenizer, max_new_tokens=100))
    
    # Action description (100 words)
    prompt = (f"Describe an action-packed scene where {characters[0]} and {characters[1]} are involved in a {action} "
              f"at {environment}. Use rhymes, and keep it adventurous.")
    story_parts.append(generate_text(prompt, model, tokenizer, max_new_tokens=150))
    
    # Ending description (50 words)
    prompt = (f"Conclude the story with a {ending} ending for {characters[0]} and {characters[1]}. "
              f"Use rhymes and make it heartwarming for children.")
    story_parts.append(generate_text(prompt, model, tokenizer, max_new_tokens=100))
    
    return story_parts


if __name__ == "__main__":
    # Example test for generate_story
    characters = ["Venom", "Godzilla"]
    environment = "space"
    action = "fight"
    ending = "happy"
    
    story = generate_story(characters, environment, action, ending)
    print(type(story))
    for part in story:
        print(part)