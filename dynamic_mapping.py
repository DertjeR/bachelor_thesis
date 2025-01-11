from typing import Dict
import random


# For better security
def dynamic_mapping(seed: int) -> Dict[str, str]:
    """Generate a dynamic mapping for invisible characters based on a seed.

    This function creates a mapping of bits ('0', '1') to zero-width characters, 
    which can be used to encode binary data invisibly.

    Args:
        seed (int): The seed for the random number generator to ensure consistent mapping.

    Returns:
        Dict[str, str]: A dictionary mapping '0' and '1' to zero-width characters.
    """
    random.seed(seed)
    invisible_characters = ['\u200C', '\u200B']  # ZWNJ and ZWSP
    random.shuffle(invisible_characters)

    return {'0': invisible_characters[0], '1': invisible_characters[1]}

def encode_message(text: str, message: str, inv_char: Dict[str, str]) -> str:
    """Encode a hidden message into cover text using zero-width characters.

    Converts the hidden message to binary and embeds it into the cover text using 
    zero-width characters defined in the mapping.

    Args:
        text (str): The cover text to embed the hidden message into.
        message (str): The message to be hidden.
        inv_char (Dict[str, str]): A dictionary mapping bits ('0', '1') to zero-width characters.

    Returns:
        str: The resulting stego text containing the hidden message.
    """
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    encoded_text = text + ''.join(inv_char[bit] for bit in binary_message)

    return encoded_text

def decode_message(encoded_text: str, inv_char: Dict[str, str]) -> str:
    """Decode a hidden message from stego text using zero-width character mapping.

    Extracts the binary message from the zero-width characters embedded in the 
    stego text and converts it back to the original string.

    Args:
        encoded_text (str): The stego text containing the hidden message.
        inv_char (Dict[str, str]): A dictionary mapping bits ('0', '1') to zero-width characters.

    Returns:
        str: The decoded hidden message.
    """
    invisible_chars = ''.join(c for c in encoded_text if c in inv_char.values())
    binary_message = ''.join('0' if c == '\u200C' else '1' for c in invisible_chars)
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return decoded_message

def main():
    file_path = "input_texts/smallest_covertext.txt" # TODO Add condition where if a txt file is given in the command line to use that
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
