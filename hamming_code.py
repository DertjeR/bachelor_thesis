import json
from collections import Counter
from queue import PriorityQueue
from typing import Dict, Tuple
import random

# Huffman Node Class
class HuffmanNode:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(hidden_message: str) -> HuffmanNode:
    freq = Counter(hidden_message)
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

# Generate Huffman Codes
def generate_huffman_codes(node: HuffmanNode, prefix: str = "", codebook: Dict[str, str] = None) -> Dict[str, str]:
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

# Huffman Encode
def huffman_encode(hidden_message: str) -> Tuple[str, Dict[str, str]]:
    tree = build_huffman_tree(hidden_message)
    codebook = generate_huffman_codes(tree)
    huffman_encoded = ''.join(codebook[char] for char in hidden_message)
    return huffman_encoded, codebook

# Huffman Decode
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

# Hamming Encode
def hamming_encode(data: str) -> str:
    n = len(data)
    r = 0
    while (2**r < n + r + 1):
        r += 1

    hamming_code = [''] * (n + r)
    j = 0
    for i in range(1, len(hamming_code) + 1):
        if i & (i - 1) == 0:
            hamming_code[i - 1] = '0'
        else:
            hamming_code[i - 1] = data[j]
            j += 1

    for i in range(r):
        pos = 2**i
        parity = 0
        for j in range(1, len(hamming_code) + 1):
            if j & pos and hamming_code[j - 1] == '1':
                parity ^= 1
        hamming_code[pos - 1] = str(parity)

    return ''.join(hamming_code)

# Hamming Decode
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

    if error_pos > 0:
        error_pos -= 1
        data = data[:error_pos] + ('1' if data[error_pos] == '0' else '0') + data[error_pos + 1:]

    original_data = ''
    for i in range(1, n + 1):
        if i & (i - 1) != 0:
            original_data += data[i - 1]

    return original_data

# Dynamic Mapping
def dynamic_mapping(seed: int) -> Dict[str, str]:
    random.seed(seed)
    invisible_characters = ['\u200C', '\u200B']
    random.shuffle(invisible_characters)
    return {'0': invisible_characters[0], '1': invisible_characters[1]}

# Encode Message
def encode_message(cover_text: str, hidden_message: str, inv_chars: Dict[str, str]) -> str:
    huffman_encoded, codebook = huffman_encode(hidden_message)
    serialized_codebook = json.dumps(codebook)
    codebook_binary = ''.join(format(ord(char), '08b') for char in serialized_codebook)
    encoded_codebook = ''.join(inv_chars[bit] for bit in codebook_binary)
    hamming_encoded = hamming_encode(huffman_encoded)
    encoded_message = ''.join(inv_chars[bit] for bit in hamming_encoded)
    separator = '\u200D'
    return cover_text + encoded_codebook + separator + encoded_message

# Decode Message
def decode_message(stego_object: str, inv_chars: Dict[str, str]) -> str:
    invisible_chars = ''.join(c for c in stego_object if c in inv_chars.values() or c == '\u200D')
    separator = '\u200D'
    if separator not in invisible_chars:
        raise ValueError("Separator for codebook and message not found.")
    encoded_codebook, encoded_message = invisible_chars.split(separator)
    inverted_mapping = {v: k for k, v in inv_chars.items()}
    codebook_binary = ''.join(inverted_mapping[c] for c in encoded_codebook)
    serialized_codebook = ''.join(chr(int(codebook_binary[i:i+8], 2)) for i in range(0, len(codebook_binary), 8))
    codebook = json.loads(serialized_codebook)
    hamming_encoded = ''.join(inverted_mapping[c] for c in encoded_message)
    huffman_encoded = hamming_decode(hamming_encoded)
    return huffman_decode(huffman_encoded, codebook)

# Main Function
def main():
    file_path = "cover_texts/small_covertext.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        cover_text = file.read()

    hidden_message = "Hallootjes woehoeeeeeeeee!"
    seed = 42
    invisible_characters = dynamic_mapping(seed)

    stego_object = encode_message(cover_text, hidden_message, invisible_characters)
    decoded_hidden_message = decode_message(stego_object, invisible_characters)

    print("Cover text:", cover_text)
    print("Stego text:", stego_object)
    print("Decoded message:", decoded_hidden_message)

    if hidden_message == decoded_hidden_message:
        print("Message successfully hidden and retrieved!")
    else:
        print("Error: Message not successfully hidden and retrieved.")

if __name__ == "__main__":
    main()
