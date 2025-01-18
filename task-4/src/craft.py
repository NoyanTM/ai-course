from llama_cpp import Llama

llm = Llama(
    model_path="Meta-Llama-3.1-8B-Instruct-Q6_K.gguf",
)

prompt = """
In the style of Infinite Craft, so you must combine these two elements to NEW WORD by rules bellow
Rules:
1. Result should be a single word or short compound word without punctuation marks merged in one word in PascalCase
2. Result should be logical and creative like "fire and lizard will be dragon"
3. Result should relate to both input elements
GENERATE ONLY THE RESULTING SHORT WORD AND NOTHING ELSE WITHOUT ANY EXPLANATION
"""

def generate_response(prompt: str, first_element: str, second_element: str):
    output = llm.create_chat_completion(
        messages = [
          {"role": "system", "content": prompt},
          {
              "role": "user",
              "content": f"Combine {first_element} and {second_element}"
          }
        ],
        temperature=0.9,
        max_tokens=256
    )
    return output['choices'][0]['message']['content']
    # return output
