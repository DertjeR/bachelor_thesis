# basic encoding with invisible characters

def encode_message(text, message, inv_chars):
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print("This is the message in binary:", binary_message)
    # Embed binary message in zero-width characters
    encoded_text = text + ''.join(inv_chars[bit] for bit in binary_message)

    return encoded_text

def decode_message(encoded_text, inv_chars):
    # Extract zero-width characters from the text
    invisible_chars = ''.join(c for c in encoded_text if c in inv_chars.values())
    # Convert back to binary
    binary_message = ''.join('0' if c == '\u200C' else '1' for c in invisible_chars)
    # Decode binary to string
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return decoded_message

def main():
    file_path = "input1.txt"  # TODO: Add command-line argument for file input
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    invisible_chars = {'0': '\u200C', '1': '\u200B'}
    hidden_message = "Hallootjes woehoeeeeeeeee!"  # TODO: Add command-line argument for hidden message input
    stego_text = encode_message(cover_text, hidden_message, invisible_chars)
    decoded_message = decode_message(stego_text, invisible_chars)

    print("Cover tekst:", cover_text)
    print("Stego text:", stego_text)
    print("Gedecodeerd bericht:", decoded_message)

if __name__ == "__main__":
    main()
