# encoding with invisible characters

# Define mappings for binary to zero-width characters
ZERO_WIDTH_MAP = {'0': '\u200C', '1': '\u200B'}  # ZWNJ and ZWSP

def encode_message(text, message):
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    print("This is the message in binary:", binary_message)
    # Embed binary message in zero-width characters
    encoded_text = text + ''.join(ZERO_WIDTH_MAP[bit] for bit in binary_message)

    return encoded_text

def decode_message(encoded_text):
    # Extract zero-width characters from the text
    invisible_chars = ''.join(c for c in encoded_text if c in ZERO_WIDTH_MAP.values())
    # Convert back to binary
    binary_message = ''.join('0' if c == '\u200C' else '1' for c in invisible_chars)
    # Decode binary to string
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

    return decoded_message

def main():
    cover_text = "Dit is de cover tekst."
    hidden_message = "Hoi!"
    stego_text = encode_message(cover_text, hidden_message)
    decoded_message = decode_message(stego_text)

    print("Cover tekst:", cover_text)
    print("Stego text:", stego_text)
    print("Gedecodeerd bericht:", decoded_message)

if __name__ == "__main__":
    main()

