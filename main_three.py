# encoding with invisible characters
from collections import Counter, PriorityQueue
from typing import Dict, Tuple
import random



# For better security
def dynamic_mapping(seed: int) -> Dict[str,str]:
    """Generate a dynamic mapping for invisible characters based on a seed.

    Args:
        seed (int): The seed for the random number generator.

    Returns:
        dict: A dictionary mapping bits ('0', '1') to invisible characters.
    """
    random.seed(seed)
    # Randomize the mapping
    invisible_characters = ['\u200C', '\u200B']  # ZWNJ and ZWSP
    random.shuffle(invisible_characters)

    return {'0': invisible_characters[0], '1': invisible_characters[1]}

# TODO to help prevent possible information loss 
def hamming_error_correction():
    pass


def encode_message(text: str, message: str, inv_char: Dict[str, str]) -> str:
    """Convert a string to binary and encode it with the invisible characters
    in the dictionary.

    Args:
        text (str): The cover text
        message (str): The hidden message
        inv_char (dict): Dictionary with bits mapped to invisible characters

    Returns:
        string: The stego text
    """
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print("This is the message in binary:", binary_message) # For debugging purposes

    # Embed binary message in zero-width characters
    encoded_text = text + ''.join(inv_char[bit] for bit in binary_message)

    return encoded_text

def decode_message(encoded_text: str, inv_char: Dict[str, str]) -> str:
    """Decode the stego text with the dictionary and retreive the hidden message

    Args:
        encoded_text (str): The stego text
        inv_char (dict): Dictionary with bits mapped to invisible characters

    Returns:
        string: The hidden message
    """
    # Extract zero-width characters from the text
    invisible_chars = ''.join(c for c in encoded_text if c in inv_char.values())

    # Convert back to binary
    binary_message = ''.join('0' if c == '\u200C' else '1' for c in invisible_chars)

    # Decode binary to string
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return decoded_message

def main():
    file_path = "input1.txt" # TODO Add condition where if a txt file is given in the command line to use that
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()
    hidden_message = "Hallootjes woehoeeeeeeeee!" # TODO Add possibility for user to input hidden message in command line?

    seed = 11
    invisible_characters = dynamic_mapping(seed)
    stego_text = encode_message(cover_text, hidden_message, invisible_characters)
    decoded_message = decode_message(stego_text, invisible_characters)

    print("Cover tekst:", cover_text)
    print("Stego text:", stego_text)
    print("Gedecodeerd bericht:", decoded_message)

if __name__ == "__main__":
    main()

