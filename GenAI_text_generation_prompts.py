#!/usr/bin/env python
# coding=utf-8

import argparse
import logging
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MAX_LENGTH = int(10000)  # Hardcoded max length to avoid infinite loop

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        required=True,
        help="Path to pre-trained model or model name",
    )
    parser.add_argument("--prompt", type=str, default="")
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--stop_token", type=str, default=None)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--k", type=int, default=0)
    parser.add_argument("--p", type=float, default=0.9)
    args = parser.parse_args()

    # Initialize the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)
    model = AutoModelForCausalLM.from_pretrained(args.model_name_or_path)

    # Set the model to the right device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    prompt_text = args.prompt if args.prompt else input("Model prompt >>> ")

    encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=False, return_tensors="pt").to(device)

    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=len(encoded_prompt[0]) + args.length,
        temperature=args.temperature,
        top_k=args.k,
        top_p=args.p,
        repetition_penalty=1.0,
        do_sample=True,
        num_return_sequences=1,
    )

    generated_sequences = []

    for generated_sequence in output_sequences:
        generated_sequence = generated_sequence.tolist()
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)
        text = text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)):]

        if args.stop_token:
            text = text.split(args.stop_token)[0]

        total_sequence = prompt_text + text
        generated_sequences.append(total_sequence)
        print(total_sequence)

    return generated_sequences

if __name__ == "__main__":
    main()
