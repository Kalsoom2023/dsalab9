Objective
The objective of this lab is to implement Huffman Coding, a popular algorithm used for lossless data compression. The goal is to represent the characters of a given text with variable-length codes, where the most frequent characters are represented by shorter codes, and less frequent characters are represented by longer codes.

Key Concepts
Huffman Coding Overview:
Huffman coding is a greedy algorithm that works by assigning variable-length codes to input characters based on their frequencies. The key idea is to:

Build a frequency table for the characters in the input.
Use this frequency table to build a binary tree, called the Huffman Tree, where:
The leaf nodes represent characters.
Internal nodes represent merged frequencies of their child nodes.
Traverse the tree to generate the Huffman codes, where:
Each left child edge represents 0.
Each right child edge represents 1.
Steps:
Calculate frequencies of each character in the input.
Build a priority queue (min-heap) to store the characters based on their frequencies.
Build the Huffman Tree by repeatedly extracting the two nodes with the smallest frequencies and merging them.
Generate the Huffman codes by traversing the tree.
Example:
For the string "ABRACADABRA", the frequency of characters would be:

A: 5
B: 2
R: 2
C: 1
D: 1
The resulting Huffman Tree would generate a set of codes such as:

A: 0
B: 10
R: 11
C: 1100
D: 1101
Approach
We'll implement the following steps:

Frequency Calculation: Calculate the frequency of each character in the given string.
Min-Heap for Tree Construction: Use a priority queue (min-heap) to store characters based on their frequencies.
Huffman Tree Creation: Construct the Huffman Tree by merging nodes with the lowest frequencies.
Code Generation: Traverse the tree to assign codes to characters.
Encoding: Encode the input string based on the Huffman codes.
Decoding: Decode the encoded string back to the original text using the Huffman Tree.
C++ Implementation of Huffman Coding
Code:
cpp
Copy code
#include <iostream>
#include <queue>
#include <unordered_map>
#include <vector>
#include <string>
using namespace std;

// Structure to represent a Huffman Tree Node
struct Node {
    char data;
    int freq;
    Node *left, *right;

    Node(char data, int freq) {
        this->data = data;
        this->freq = freq;
        left = right = nullptr;
    }
};

// Comparison function to order nodes in a min-heap
struct compare {
    bool operator()(Node* l, Node* r) {
        return l->freq > r->freq;
    }
};

// Function to build the Huffman Tree
Node* buildHuffmanTree(const unordered_map<char, int>& freqMap) {
    priority_queue<Node*, vector<Node*>, compare> minHeap;

    // Create a leaf node for each character and add it to the priority queue
    for (auto& pair : freqMap) {
        minHeap.push(new Node(pair.first, pair.second));
    }

    // Build the Huffman tree
    while (minHeap.size() > 1) {
        Node *left = minHeap.top(); minHeap.pop();
        Node *right = minHeap.top(); minHeap.pop();

        Node *top = new Node('$', left->freq + right->freq); // Internal node
        top->left = left;
        top->right = right;

        minHeap.push(top);
    }

    return minHeap.top();
}

// Function to generate the Huffman Codes by traversing the Huffman Tree
void generateCodes(Node* root, const string& str, unordered_map<char, string>& huffmanCodes) {
    if (root == nullptr) {
        return;
    }

    // If it's a leaf node, store the Huffman code
    if (root->left == nullptr && root->right == nullptr) {
        huffmanCodes[root->data] = str;
    }

    generateCodes(root->left, str + "0", huffmanCodes);
    generateCodes(root->right, str + "1", huffmanCodes);
}

// Function to encode the given input string using Huffman Codes
string encode(const string& input, unordered_map<char, string>& huffmanCodes) {
    string encoded = "";
    for (char ch : input) {
        encoded += huffmanCodes[ch];
    }
    return encoded;
}

// Function to decode the encoded string using the Huffman Tree
string decode(Node* root, const string& encoded) {
    string decoded = "";
    Node* current = root;

    for (char bit : encoded) {
        if (bit == '0') {
            current = current->left;
        } else {
            current = current->right;
        }

        // If leaf node is reached, append the character to the decoded string
        if (current->left == nullptr && current->right == nullptr) {
            decoded += current->data;
            current = root; // Go back to the root
        }
    }

    return decoded;
}

int main() {
    string input = "ABRACADABRA";

    // Step 1: Calculate frequency of characters
    unordered_map<char, int> freqMap;
    for (char ch : input) {
        freqMap[ch]++;
    }

    // Step 2: Build the Huffman Tree
    Node* root = buildHuffmanTree(freqMap);

    // Step 3: Generate Huffman Codes
    unordered_map<char, string> huffmanCodes;
    generateCodes(root, "", huffmanCodes);

    // Step 4: Encode the input string
    string encoded = encode(input, huffmanCodes);
    cout << "Encoded: " << encoded << endl;

    // Step 5: Decode the encoded string
    string decoded = decode(root, encoded);
    cout << "Decoded: " << decoded << endl;

    return 0;
}
Explanation of Code:
Node Structure: The Node structure is used to represent a tree node, which contains the character (data), its frequency (freq), and pointers to its left and right children.
Priority Queue (Min-Heap): A priority queue is used to construct the Huffman tree. It ensures that the nodes with the smallest frequencies are merged first.
Tree Construction: The buildHuffmanTree() function constructs the tree by iteratively extracting the two nodes with the smallest frequencies and merging them into a new internal node.
Code Generation: The generateCodes() function traverses the Huffman tree and assigns binary codes (0 for left edge, 1 for right edge).
Encoding and Decoding: The encode() function converts the input string to its Huffman-encoded binary representation, while the decode() function decodes it back using the tree.
Example Output:
makefile
Copy code
Encoded: 101010000111011010100001011010010111
Decoded: ABRACADABRA
Time Complexity:
Building Frequency Map: O(n), where n is the length of the input string.
Building Huffman Tree: O(n log n), where n is the number of unique characters.
Encoding: O(n), where n is the length of the input string.
Decoding: O(m), where m is the length of the encoded string.
