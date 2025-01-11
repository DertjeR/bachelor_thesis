from dynamic_mapping import *
import os

def readability(cover_text, stego_text):
    chars = {'\u200C', '\u200B'}
    cover_text_content = ''.join(char for char in cover_text if char not in chars)
    stego_text_content = ''.join(char for char in stego_text if char not in chars)

    if cover_text_content == stego_text_content:
        return True
    else:
        # Show differences
        print("Differences found:")
        print(f"Cover Text: {repr(cover_text_content)}")
        print(f"Stego Text: {repr(stego_text_content)}")
        return False

def test_payload_capacity(cover_text, hidden_message, inv_chars):
    # Encode the message into the cover text
    stego_text = encode_message(cover_text, hidden_message, inv_chars)

    # Calculate payload capacity
    cover_size = len(cover_text) * 8  # Convert characters to bits
    hidden_size = len(hidden_message) * 8  # Convert characters to bits
    payload_capacity = hidden_size / cover_size  # Payload capacity as a ratio

    return payload_capacity, stego_text

def main():
    # Directories containing cover texts and hidden messages
    cover_dir = "cover_texts"
    message_dir = "hidden_messages"

    # Get all cover text files and hidden message files
    cover_files = [os.path.join(cover_dir, f) for f in os.listdir(cover_dir) if os.path.isfile(os.path.join(cover_dir, f))]
    message_files = [os.path.join(message_dir, f) for f in os.listdir(message_dir) if os.path.isfile(os.path.join(message_dir, f))]

    # Seed for dynamic mapping
    seed = 11
    invisible_chars = {'0': '\u200C', '1': '\u200B'}

    # Results directory
    results_dir = "evaluations/basic_approach"
    os.makedirs(results_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Iterate through all combinations of cover text and hidden message files
    for cover_file in cover_files:
        with open(cover_file, "r", encoding="utf-8") as cover_file_obj:
            cover_text = cover_file_obj.read()

        for message_file in message_files:
            with open(message_file, "r", encoding="utf-8") as message_file_obj:
                hidden_message = message_file_obj.read()

            # Calculate payload capacity and stego text
            _, stego_text = test_payload_capacity(cover_text, hidden_message, invisible_chars)

            # Check readability
            if readability(cover_text, stego_text):
                output_filename = f"{os.path.basename(cover_file).split('.')[0]}_{os.path.basename(message_file).split('.')[0]}.txt"
                output_file_path = os.path.join(results_dir, output_filename)

                # Save payload capacity to a file
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(stego_text)
                print(f"Stego text for {cover_file} and {message_file} saved to {output_file_path}")
            else:
                print(f"Stego text generated for {cover_file} and {message_file} has lost readability.")

if __name__ == "__main__":
    main()
