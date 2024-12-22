class HuffmanNode:
    def __init__(self, zero=None, one=None, data=None):
        self.zero = zero  # Left child
        self.one = one    # Right child
        self.data = data  # Character stored

    def is_leaf(self):
        """Check if the node is a leaf node."""
        return self.zero is None and self.one is None

    def is_valid_node(self):
        """Check if the node is valid for a Huffman coding tree."""
        return (self.is_leaf() and self.data is not None) or (self.data is None and self.zero is not None and self.one is not None)

    def is_valid_tree(self):
        """Check if the node and all its descendants are valid for a Huffman coding tree."""
        if not self.is_valid_node():
            return False
        left_valid = self.zero.is_valid_tree() if self.zero else True
        right_valid = self.one.is_valid_tree() if self.one else True
        return left_valid and right_valid
class HuffmanCodeBook:
    def __init__(self):
        self.code_book = {}  # Dictionary to store mappings of characters to binary sequences

    def add_sequence(self, char, seq):
        """Add a character and its binary sequence to the codebook."""
        self.code_book[char] = seq

    def contains(self, char):
        """Check if a character exists in the codebook."""
        return char in self.code_book

    def contains_all(self, text):
        """Check if all characters in the text exist in the codebook."""
        return all(char in self.code_book for char in text)

    def get_sequence(self, char):
        """Get the binary sequence associated with a character."""
        return self.code_book.get(char)

    def encode(self, text):
        """Encode a text string into its binary representation."""
        if not self.contains_all(text):
            raise ValueError("Codebook is missing one or more characters from the input text.")
        return "".join(self.get_sequence(char) for char in text)

    def all_sequences(self):
        """Get all character-to-sequence mappings."""
        return self.code_book.items()
class HuffmanCodeTree:
    def __init__(self, root=None):
        self.root = root  # Root node of the Huffman tree

    @classmethod
    def from_codebook(cls, codebook):
        """Construct a HuffmanCodeTree from a HuffmanCodeBook."""
        tree = cls(HuffmanNode())
        for char, seq in codebook.all_sequences():
            tree.put(seq, char)
        return tree

    def is_valid(self):
        """Check if the Huffman tree is valid."""
        return self.root and self.root.is_valid_tree()

    def put(self, seq, char):
        """Insert a character into the tree at the location specified by the binary sequence."""
        current = self.root
        for bit in seq:
            if bit == '0':
                if current.zero is None:
                    current.zero = HuffmanNode()
                current = current.zero
            elif bit == '1':
                if current.one is None:
                    current.one = HuffmanNode()
                current = current.one
            else:
                raise ValueError("Binary sequence must only contain '0' or '1'.")
        current.data = char

    def decode(self, binary_sequence):
        """Decode a binary sequence into a string."""
        decoded_text = []
        current = self.root
        for bit in binary_sequence:
            if bit == '0':
                current = current.zero
            elif bit == '1':
                current = current.one
            else:
                raise ValueError("Binary sequence must only contain '0' or '1'.")

            if current.is_leaf():
                decoded_text.append(current.data)
                current = self.root  # Reset to root for the next character
        return "".join(decoded_text)
# Example
if __name__ == "__main__":
    # Create a Huffman CodeBook
    codebook = HuffmanCodeBook()
    codebook.add_sequence('a', '00')
    codebook.add_sequence('b', '01')
    codebook.add_sequence('c', '10')
    codebook.add_sequence('d', '11')

    # Encode a string
    text = "abac"
    encoded = codebook.encode(text)
    print(f"Encoded: {encoded}")

    # Build the Huffman Tree
    huffman_tree = HuffmanCodeTree.from_codebook(codebook)

    # Decode the binary sequence
    decoded = huffman_tree.decode(encoded)
    print(f"Decoded: {decoded}")
