from typing import Dict
import random


# For better security
def dynamic_mapping(seed: int) -> Dict[str, str]:
    """Generate a dynamic mapping for invisible characters based on a seed.

    Args:
        seed (int): The seed for the random number generator.

    Returns:
        Dict[str, str]: A dict mapping '0' and '1' to invisible characters.
    """
    random.seed(seed)
    invisible_characters = ['\u200C', '\u200B']
    random.shuffle(invisible_characters)

    return {'0': invisible_characters[0], '1': invisible_characters[1]}


def encode_message(cover_text: str, hidden_message: str,
                   inv_chars: Dict[str, str]) -> str:
    """Encodes a hidden message into cover text using invisible characters
    and outputs the stego object.

    Args:
        cover_text (str): The cover text to embed the hidden message into.
        hidden_message (str): The message to be hidden.
        inv_char (dict): A dictionary mapping bits ('0', '1') to
        invisible characters.

    Returns:
        str: The resulting stego object containing the hidden message.
    """
    # Convert the hidden message to binary
    binary_message = ''.join(
        format(ord(char), '08b') for char in hidden_message)
    invisible_sequence = ''.join(inv_chars[bit] for bit in binary_message)

    # Split the cover text into words
    words = cover_text.split()
    stego_object = []

    # Distribute invisible characters after each word
    char_index = 0
    for word in words:
        stego_object.append(word)
        if char_index < len(invisible_sequence):
            stego_object.append(invisible_sequence[char_index])
            char_index += 1

    # Append remaining invisible characters at the end if there are any
    if char_index < len(invisible_sequence):
        stego_object.append(invisible_sequence[char_index:])

    return ' '.join(stego_object)


def decode_message(stego_obj: str, inv_chars: Dict[str, str]) -> str:
    """Extracts the binary message from the invisible characters embedded in
    the stego object and converts it back to the original hidden message.

    Args:
        stego_object (str): The stego object containing the hidden message.
        inv_chars (dict): A dictionary mapping bits ('0', '1') to invisible
        characters.

    Returns:
        str: The decoded hidden message.
    """
    # Extract invisible characters from the text
    invisible_chars = ''.join(c for c in stego_obj if c in inv_chars.values())

    # Convert back to binary
    binary_message = ''.join(
        '0' if c == '\u200C' else '1' for c in invisible_chars)

    # Decode binary to string
    decoded_hidden_message = ''.join(chr(int(binary_message[i:i+8], 2))
                                     for i in range(0, len(binary_message), 8))

    return decoded_hidden_message


def main():
    # TODO Add command-line argument for file input
    file_path = "cover_texts/small_covertext.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    # TODO Add possibility for user to input hidden message in command line?
    hidden_message = "Hallootjes woehoeeeeeeeee!"

    seed = 42
    invisible_chars = dynamic_mapping(seed)
    stego_object = encode_message(cover_text, hidden_message, invisible_chars)
    decoded_message = decode_message(stego_object, invisible_chars)

    print("Cover tekst:", cover_text)
    print("Stego text:", stego_object)
    print("Gedecodeerd bericht:", decoded_message)

    if hidden_message == decoded_message:
        print("Message successfully hidden and retrieved!")
    else:
        print("Error: Message not successfully hidden and retrieved.")


if __name__ == "__main__":
    main()
