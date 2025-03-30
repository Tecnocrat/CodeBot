import base64

def encode_to_base64(input_string):
    """Encodes a string to Base64."""
    return base64.b64encode(input_string.encode()).decode()

def decode_from_base64(encoded_string):
    """Decodes a Base64 string."""
    return base64.b64decode(encoded_string.encode()).decode()

# Example usage
if __name__ == "__main__":
    original = "Hello, CodeBot!"
    encoded = encode_to_base64(original)
    decoded = decode_from_base64(encoded)

    print(f"Original: {original}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")

# CodeBot_Tracking
