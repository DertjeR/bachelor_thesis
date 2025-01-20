from strategies.hamming_code import *
import os
import random
import time
import json
from collections import Counter
from queue import PriorityQueue
from typing import Dict, Tuple


# Functions from the Huffman and Hamming implementation (abbreviated for brevity)
# Include all previously defined functions: build_huffman_tree, generate_huffman_codes,
# huffman_encode, huffman_decode, hamming_encode, hamming_decode, dynamic_mapping,
# encode_message, decode_message, etc.


def introduce_error(data: str) -> Tuple[str, int]:
    """Introduce a single random error in the Hamming-encoded binary string.

    Args:
        data (str): The original Hamming-encoded binary string.

    Returns:
        Tuple[str, int]: The corrupted binary string and the error position.
    """
    data = list(data)
    data_length = len(data)
    random.seed(time.time())  # Set seed for random error positions

    # Select a random position to flip
    error_position = random.randint(0, data_length - 1)
    data[error_position] = '1' if data[error_position] == '0' else '0'

    return ''.join(data), error_position


def pick_random_file(directory: str) -> str:
    """Randomly select a file from a directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        str: Path to the randomly selected file.
    """
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return random.choice(files)


def evaluate_runs(num_runs: int = 100):
    """Evaluate encoding/decoding with multiple runs and random error introduction."""
    results_file = "results/results_hamming.txt"
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    for i in range(1, num_runs + 1):
        print(f"Starting run number: {i}...")

        # Randomly select cover text and hidden message
        cover_text_file = pick_random_file("cover_texts")
        hidden_message_file = pick_random_file("hidden_messages")

        with open(cover_text_file, "r", encoding="utf-8") as cover_file:
            cover_text = cover_file.read()

        with open(hidden_message_file, "r", encoding="utf-8") as message_file:
            hidden_message = message_file.read()

        # Dynamic mapping seed
        seed = 42
        invisible_characters = dynamic_mapping(seed)

        # Encode the hidden message
        stego_object = encode_message(cover_text, hidden_message, invisible_characters)

        # Extract invisible characters and separator for error introduction
        separator = '\u200D'
        invisible_chars = ''.join(c for c in stego_object if c in invisible_characters.values() or c == separator)
        encoded_codebook, hamming_encoded = invisible_chars.split(separator)

        # Introduce an error in the Hamming-encoded part
        inverted_mapping = {v: k for k, v in invisible_characters.items()}
        hamming_binary = ''.join(inverted_mapping[c] for c in hamming_encoded)
        corrupted_hamming_binary, error_position = introduce_error(hamming_binary)

        # Reconstruct the corrupted stego object
        corrupted_hamming_encoded = ''.join(invisible_characters[bit] for bit in corrupted_hamming_binary)
        corrupted_stego_object = cover_text + encoded_codebook + separator + corrupted_hamming_encoded

        # Decode the corrupted message
        try:
            decoded_message = decode_message(corrupted_stego_object, invisible_characters)
            result = "Successfully retrieved message" if hidden_message == decoded_message else "Failed to retrieve correct message"
        except Exception as e:
            result = f"Decoding error: {e}"

        # Log results
        with open(results_file, "a", encoding="utf-8") as results:
            results.write(f"Run number: {i}\n")
            results.write("Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            results.write(f"Cover text file: {os.path.basename(cover_text_file)}\n")
            results.write(f"Hidden message file: {os.path.basename(hidden_message_file)}\n")
            results.write(f"Error position: {error_position}\n")
            results.write(f"Result: {result}\n")
            results.write("=" * 50 + "\n")

        print(f"Run number {i} completed. Result: {result}")




def main():
    evaluate_runs(num_runs=100)  # Run the evaluation 100 times


if __name__ == "__main__":
    main()



# import time
# import random
# import os


# def introduce_errors(data: str) -> str:
#     """Introduce random bit errors into the Hamming-encoded binary string.

#     Args:
#         data (str): The original Hamming-encoded binary string.
#         num_errors (int): The number of bit errors to introduce.

#     Returns:
#         str: The modified binary string with errors.
#     """
#     data = list(data)  # Convert to list for mutability
#     data_length = len(data)
#     random.seed(time.time()) # Set seed based on current time to ensure random error positions

#     # Randomly select one position to flip
#     error_position = random.randint(0, data_length - 1)
#     data[error_position] = '1' if data[error_position] == '0' else '0'

#     return ''.join(data), error_position

# def pick_random_file(directory: str) -> str:
#     """Randomly pick a file from a given directory.

#     Args:
#         directory (str): The directory to pick a file from.

#     Returns:
#         str: The path to the randomly selected file.
#     """
#     files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#     return random.choice(files)

# def main():
#     for i in range(1, 101):
#         print(f"Starting run number: {i}...")
#         # Randomly select a cover text and hidden message
#         cover_text_file = pick_random_file("cover_texts")
#         hidden_message_file = pick_random_file("hidden_messages")

#         # Load the cover text
#         with open(cover_text_file, "r", encoding="utf-8") as file:
#             cover_text = file.read()

#         # Load the hidden message
#         with open(hidden_message_file, "r", encoding="utf-8") as file:
#             hidden_message = file.read()

#         # Seed for dynamic mapping
#         seed = 42
#         invisible_characters = dynamic_mapping(seed)

#         # Encode the message
#         stego_object, codebook = encode_message(cover_text, hidden_message, invisible_characters)

#         # Extract the invisible characters part for error introduction
#         invisible_chars = ''.join(c for c in stego_object if c in invisible_characters.values())
#         inverted_mapping = {v: k for k, v in invisible_characters.items()}
#         hamming_encoded = ''.join(inverted_mapping[c] for c in invisible_chars)

#         # Introduce errors into the Hamming-encoded binary string
#         corrupted_hamming_encoded, error_position = introduce_errors(hamming_encoded)

#         # Reconstruct the corrupted stego object
#         corrupted_stego_object = (
#             cover_text + ''.join(invisible_characters[bit] for bit in corrupted_hamming_encoded)
#         )

#         # Decode the message from the corrupted stego object
#         decoded_message = decode_message(corrupted_stego_object, invisible_characters, codebook)

#         results_file = "results/results_hamming.txt"
#         with open(results_file, "a", encoding="utf-8") as results:
#             results.write(f"Run number: {i}\n")
#             results.write("Run Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
#             results.write(f"Covertext file: {os.path.basename(cover_text_file)}\n")
#             results.write(f"Hidden message file: {os.path.basename(hidden_message_file)}\n")
#             results.write(f"Error position: {error_position}\n")
#             results.write(f"Result: {'Successfully retrieved message' if hidden_message == decoded_message else 'Failure to retrieve correct message'}\n")
#             results.write("=" * 50 + "\n")
        
#         print(f"Run number {i} has finished.")

# if __name__ == "__main__":
#     main()
