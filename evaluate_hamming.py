from hamming_code import *
import time
import random
import os


def introduce_errors(data: str) -> str:
    """Introduce random bit errors into the Hamming-encoded binary string.

    Args:
        data (str): The original Hamming-encoded binary string.
        num_errors (int): The number of bit errors to introduce.

    Returns:
        str: The modified binary string with errors.
    """
    data = list(data)  # Convert to list for mutability
    data_length = len(data)
    random.seed(time.time()) # Set seed based on current time to ensure random error positions

    # Randomly select one position to flip
    error_position = random.randint(0, data_length - 1)
    data[error_position] = '1' if data[error_position] == '0' else '0'

    return ''.join(data), error_position

def pick_random_file(directory: str) -> str:
    """Randomly pick a file from a given directory.

    Args:
        directory (str): The directory to pick a file from.

    Returns:
        str: The path to the randomly selected file.
    """
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return random.choice(files)

def main():
    for i in range(1, 101):
        print(f"Starting run number: {i}...")
        # Randomly select a cover text and hidden message
        cover_text_file = pick_random_file("cover_texts")
        hidden_message_file = pick_random_file("hidden_messages")

        # Load the cover text
        with open(cover_text_file, "r", encoding="utf-8") as file:
            cover_text = file.read()

        # Load the hidden message
        with open(hidden_message_file, "r", encoding="utf-8") as file:
            hidden_message = file.read()

        # Seed for dynamic mapping
        seed = 42
        invisible_characters = dynamic_mapping(seed)

        # Encode the message
        stego_object, codebook = encode_message(cover_text, hidden_message, invisible_characters)

        # Extract the invisible characters part for error introduction
        invisible_chars = ''.join(c for c in stego_object if c in invisible_characters.values())
        inverted_mapping = {v: k for k, v in invisible_characters.items()}
        hamming_encoded = ''.join(inverted_mapping[c] for c in invisible_chars)

        # Introduce errors into the Hamming-encoded binary string
        corrupted_hamming_encoded, error_position = introduce_errors(hamming_encoded)

        # Reconstruct the corrupted stego object
        corrupted_stego_object = (
            cover_text + ''.join(invisible_characters[bit] for bit in corrupted_hamming_encoded)
        )

        # Decode the message from the corrupted stego object
        decoded_message = decode_message(corrupted_stego_object, invisible_characters, codebook)

        results_file = "results/results_hamming.txt"
        with open(results_file, "a", encoding="utf-8") as results:
            results.write(f"Run number: {i}\n")
            results.write("Run Timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            results.write(f"Covertext file: {os.path.basename(cover_text_file)}\n")
            results.write(f"Hidden message file: {os.path.basename(hidden_message_file)}\n")
            results.write(f"Error position: {error_position}\n")
            results.write(f"Result: {'Successfully retrieved message' if hidden_message == decoded_message else 'Failure to retrieve correct message'}\n")
            results.write("=" * 50 + "\n")
        
        print(f"Run number {i} has finished.")

if __name__ == "__main__":
    main()
