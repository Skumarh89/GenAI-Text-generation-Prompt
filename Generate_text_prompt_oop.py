# Import necessary libraries and functions
import argparse
import logging
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set the device to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the prompt
prompt = "Discuss the advantages of object-oriented programming (OOP)."

# Generate text using the model
generated_text = model.generate(
    input_ids=tokenizer.encode(prompt, return_tensors="pt").to(device),
    max_length=200,  # Adjust the length as needed
    num_return_sequences=1
)

# Decode and print the generated text
decoded_text = tokenizer.decode(generated_text[0], skip_special_tokens=True)
print(decoded_text)
