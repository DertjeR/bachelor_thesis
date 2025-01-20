from typing import Dict


def encode_message(cover_text: str, hidden_message: str,
                   inv_chars: Dict[str, str]) -> str:
    """Embed a hidden message into the cover text using zero-width characters.

    Args:
        cover_text (str): The cover text to embed the hidden message into.
        hidden_message (str): The message to hide within the cover text.
        inv_chars (Dict[str, str]): A dictionary mapping bits ('0', '1') to
        zero-width characters.

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
    """Extract and decode a hidden message from a stego object.

    Args:
        stego_object (str): The text containing the hidden message.
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
    file_path = "./cover_texts/small_covertext.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    file_path = "./hidden_messages/800bits_message.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        hidden_message = file.read()

    invisible_chars = {'0': '\u200C', '1': '\u200B'}
    stego_object = encode_message(cover_text, hidden_message, invisible_chars)
    decoded_hidden_message = decode_message(stego_object, invisible_chars)

    # For debugging purposes
    print("Hidden message:", hidden_message)
    print("Cover text:", cover_text)
    print("Stego object:", stego_object)
    print("Gedecodeerd bericht:", decoded_hidden_message)

    if hidden_message == decoded_hidden_message:
        print("Message successfully hidden and retrieved!")
    else:
        print("Error: Message not successfully hidden and retrieved.")


if __name__ == "__main__":
    main()
