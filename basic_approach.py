def encode_message(cover_text, hidden_message, inv_chars):
    """Embed a hidden message into the cover text using zero-width characters.

    Args:
        cover_text (str): The cover text to embed the hidden message into.
        hidden_message (str): The message to hide within the cover text.
        inv_chars (dict): A dictionary mapping bits ('0', '1') to zero-width characters.

    Returns:
        str: The resulting stego object containing the hidden message.
    """
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in hidden_message)
    # Embed binary message in zero-width characters
    stego_object = cover_text + ''.join(inv_chars[bit] for bit in binary_message)

    return stego_object

def decode_message(stego_object, inv_chars):
    """Extract and decode a hidden message from a stego object.

    Args:
        stego_object (str): The text containing the hidden message.
        inv_chars (dict): A dictionary mapping bits ('0', '1') to zero-width characters.

    Returns:
        str: The decoded hidden message.
    """
    # Extract zero-width characters from the text
    invisible_chars = ''.join(c for c in stego_object if c in inv_chars.values())
    # Convert back to binary
    binary_message = ''.join('0' if c == '\u200C' else '1' for c in invisible_chars)
    # Decode binary to string
    decoded_hidden_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return decoded_hidden_message

def main():
    file_path = "input_texts/smallest_covertext.txt"  # TODO: Add command-line argument for file input
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    invisible_chars = {'0': '\u200C', '1': '\u200B'}
    hidden_message = "Hallootjes woehoeeeeeeeee!"  # TODO: Add command-line argument for hidden message input
    stego_object = encode_message(cover_text, hidden_message, invisible_chars)
    decoded_hidden_message = decode_message(stego_object, invisible_chars)

    # For debugging purposes
    print("Cover tekst:", cover_text)
    print("Stego text:", stego_object)
    print("Gedecodeerd bericht:", decoded_hidden_message)

if __name__ == "__main__":
    main()
