# Invisible Character Text Steganography

## Introduction

This project is a steganography toolkit that utilizes invisible characters, such as zero-width spaces, to embed hidden messages within plain text. It implements multiple strategies to enhance security, efficiency, and error correction. The toolkit is modular, allowing for easy experimentation with different techniques.

## Table of Contents

1. [Introduction](#introduction)
2. [Folder Structure](#folder-structure)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contributor](#contributor)

## Folder Structure

- `strategies/`: Contains implementations of the encoding and decoding strategies.
- `cover_texts/`: Sample text files for use as cover texts in the steganographic process.
- `hidden_messages/`: Messages of varying lengths to test the encoding and decoding processes.
- `evaluations/`: Scripts to analyze and benchmark the performance of each strategy.

## Features

- **Basic approach**: Embeds binary messages using static mapping of invisible characters.
- **Dynamic Mapping**: Secure and randomized mapping of bits to invisible characters.
- **Huffman Encoding**: Compresses messages for improved payload capacity.
- **Hamming Code**: Provides error detection and correction.
- **Extensive Evaluation**: Includes performance and readability tests for each strategy.

## Installation

1. Clone the repository:
   ```
   git clone <https://github.com/DertjeR/bachelor_thesis.git>
   ```
2. Ensure Python 3.8+ is installed.

## Usage

All the strategies can be used by running the file in the commandline.
A standard cover text and hidden message is defined in all the main functions. If you want to use other cover texts or hidden messages you can edit the file paths in the main functions.

## Contributor
D.J. Roggeveen
d.j.roggeveen@student.rug.nl
