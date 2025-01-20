from strategies.huffman_encoding import *
import os

def readability(cover_text, stego_text):
    chars = {'\u200C', '\u200B'}
    cover_text_content = ''.join(char for char in cover_text if char not in chars)
    stego_text_content = ''.join(char for char in stego_text if char not in chars)

    return cover_text_content == stego_text_content

def test_payload_capacity(cover_text, hidden_message, inv_chars, use_huffman=False):
    """Calculate payload capacity and optionally compress the hidden message with Huffman encoding."""
    if use_huffman:
        # Huffman encode the message
        huffman_encoded_binary_message, _ = huffman_encode(hidden_message)
        compressed_message = huffman_encoded_binary_message
        compressed_size = len(compressed_message)  # Bits
    else:
        compressed_message = hidden_message
        compressed_size = len(hidden_message) * 8  # Bits

    # Encode the (compressed) message into the cover text
    stego_text = encode_message(cover_text, compressed_message, inv_chars)

    # Calculate payload capacity
    cover_size = len(cover_text) * 8  # Bits
    payload_capacity = compressed_size / cover_size  # Payload capacity as a ratio

    # Calculate compression ratio for Huffman encoding
    if use_huffman:
        original_size = len(hidden_message) * 8  # Bits
        compression_ratio = compressed_size / original_size
    else:
        compression_ratio = 1.0  # No compression

    return payload_capacity, compression_ratio, stego_text

def main():
    # Directories containing cover texts and hidden messages
    cover_dir = "cover_texts"
    message_dir = "hidden_messages"

    # Get all cover text files and hidden message files
    cover_files = [os.path.join(cover_dir, f) for f in os.listdir(cover_dir) if os.path.isfile(os.path.join(cover_dir, f))]
    message_files = [os.path.join(message_dir, f) for f in os.listdir(message_dir) if os.path.isfile(os.path.join(message_dir, f))]

    # Seed for dynamic mapping
    seed = 11
    invisible_chars = dynamic_mapping(seed)

    # Output file to store all results
    output_file_path = "results/huffman_encoding.txt"
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  # Create directory if it doesn't exist

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("Cover Text, Hidden Message, Payload Capacity (No Huffman), Payload Capacity (Huffman), Compression Ratio, Readable (No Huffman), Readable (Huffman)\n")

        # Iterate through all combinations of cover text and hidden message files
        for cover_file in cover_files:
            with open(cover_file, "r", encoding="utf-8") as cover_file_obj:
                cover_text = cover_file_obj.read()

            for message_file in message_files:
                with open(message_file, "r", encoding="utf-8") as message_file_obj:
                    hidden_message = message_file_obj.read()

                # Without Huffman Encoding
                payload_capacity_no_huffman, _, stego_text_no_huffman = test_payload_capacity(
                    cover_text, hidden_message, invisible_chars, use_huffman=False
                )

                # With Huffman Encoding
                payload_capacity_huffman, compression_ratio, stego_text_huffman = test_payload_capacity(
                    cover_text, hidden_message, invisible_chars, use_huffman=True
                )

                # Check readability
                readable_no_huffman = readability(cover_text, stego_text_no_huffman)
                readable_huffman = readability(cover_text, stego_text_huffman)

                # Write results to the output file
                output_file.write(f"{os.path.basename(cover_file)}, {os.path.basename(message_file)}, "
                                  f"{payload_capacity_no_huffman:.6f}, {payload_capacity_huffman:.6f}, "
                                  f"{compression_ratio:.6f}, {readable_no_huffman}, {readable_huffman}\n")

    print(f"All results saved to {output_file_path}")

if __name__ == "__main__":
    main()
