#encoding with invisible characters, huffman ancoding,
#hamming code and dynamic mapping

from collections import Counter
from queue import PriorityQueue
from typing import Dict, Tuple
import random

# For better payload capacity
class HuffmanNode:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text: str) -> HuffmanNode:
    freq = Counter(text)
    pq = PriorityQueue()

    for char, count in freq.items():
        pq.put(HuffmanNode(char, count))

    while pq.qsize() > 1:
        left = pq.get()
        right = pq.get()
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        pq.put(merged)

    return pq.get()

def generate_huffman_codes(node: HuffmanNode, prefix: str = "", codebook: Dict[str, str] = None) -> Dict[str, str]:
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)

    return codebook

def huffman_encode(text: str) -> Tuple[str, Dict[str, str]]:
    tree = build_huffman_tree(text)
    codebook = generate_huffman_codes(tree)
    encoded_text = ''.join(codebook[char] for char in text)

    return encoded_text, codebook

def huffman_decode(encoded_text: str, codebook: Dict[str, str]) -> str:
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_text = ""
    buffer = ""

    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_codebook:
            decoded_text += reverse_codebook[buffer]
            buffer = ""

    return decoded_text

# For error correction
def hamming_encode(data: str) -> str:
    n = len(data)
    r = 0
    while (2**r < n + r + 1):  # Calculate number of parity bits
        r += 1

    hamming_code = [''] * (n + r)
    j = 0

    for i in range(1, len(hamming_code) + 1):
        if i & (i - 1) == 0:  # Positions for parity bits
            hamming_code[i - 1] = '0'
        else:
            hamming_code[i - 1] = data[j]
            j += 1

    # Set parity bits
    for i in range(r):
        pos = 2**i
        parity = 0
        for j in range(1, len(hamming_code) + 1):
            if j & pos and hamming_code[j - 1] == '1':
                parity ^= 1
        hamming_code[pos - 1] = str(parity)

    return ''.join(hamming_code)

def hamming_decode(data: str) -> str:
    n = len(data)
    r = 0
    while (2**r < n):
        r += 1

    error_pos = 0
    for i in range(r):
        pos = 2**i
        parity = 0
        for j in range(1, n + 1):
            if j & pos and data[j - 1] == '1':
                parity ^= 1
        if parity != 0:
            error_pos += pos

    if error_pos > 0:  # Correct the error
        print(f"Error detected at position: {error_pos}")
        error_pos -= 1
        data = data[:error_pos] + ('1' if data[error_pos] == '0' else '0') + data[error_pos + 1:]

    # Extract the original data (remove parity bits)
    original_data = ''
    for i in range(1, n + 1):
        if i & (i - 1) != 0:  # Ignore parity bits
            original_data += data[i - 1]

    return original_data

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

def encode_message(text: str, message: str, inv_char: Dict[str, str]) -> str:
    # Compress message using Huffman encoding
    huffman_encoded, codebook = huffman_encode(message)
    print("Huffman Encoded Message:", huffman_encoded)  # For debugging

    # Apply Hamming code to the Huffman-encoded message
    hamming_encoded = hamming_encode(huffman_encoded)
    print("Hamming Encoded Message:", hamming_encoded)  # For debugging

    # Embed Hamming-encoded binary message using invisible characters
    encoded_text = text + ''.join(inv_char[bit] for bit in hamming_encoded)

    return encoded_text, codebook

def decode_message(encoded_text: str, inv_char: Dict[str, str], codebook: Dict[str, str]) -> str:
    # Extract invisible characters
    invisible_chars = ''.join(c for c in encoded_text if c in inv_char.values())

    # Convert back to Hamming-encoded binary
    inverted_mapping = {v: k for k, v in inv_char.items()}
    hamming_encoded = ''.join(inverted_mapping[c] for c in invisible_chars)

    # Decode Hamming code to recover the Huffman-encoded binary
    huffman_encoded = hamming_decode(hamming_encoded)
    print("Decoded Huffman Binary:", huffman_encoded)  # For debugging

    # Decompress using Huffman decoding
    decoded_message = huffman_decode(huffman_encoded, codebook)
    return decoded_message

# Main function
def main():
    file_path = "input1.txt"  # TODO: Add command-line argument for file input
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    hidden_message = "Hallootjes woehoeeeeeeeee!"  # TODO: Add command-line argument for hidden message input

    # Generate dynamic mapping
    seed = 42  # TODO: Replace with user input or system-generated random seed
    invisible_characters = dynamic_mapping(seed)

    # Encode and decode message
    stego_text, codebook = encode_message(cover_text, hidden_message, invisible_characters)
    decoded_message = decode_message(stego_text, invisible_characters, codebook)

    print("Cover tekst:", cover_text)
    print("Stego text:", stego_text)
    print("Gedecodeerd bericht:", decoded_message)

if __name__ == "__main__":
    main()

