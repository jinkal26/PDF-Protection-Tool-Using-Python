# PDF-Protection-Tool-Using-Python

A simple and effective Python tool to add password protection to PDF files using the PyPDF2 library.
This project demonstrates practical applications of file handling, encryption, and command-line argument processing in Python.

# 📘 Objective

The objective of this project is to develop a Python-based tool that allows users to apply password protection to PDF files.
This helps in securing sensitive documents and gives learners hands-on experience with Python file operations and encryption.

# 🧩 Project Overview

PDF files often contain confidential or sensitive data. Adding password protection ensures an additional layer of security.

This tool:

Takes an input PDF file.

Applies a password using Python’s PyPDF2 library.

Saves the output as a new encrypted PDF file.

# ⚙️ How It Works

Input Handling:
The script accepts three command-line arguments:

Input PDF file path

Output (encrypted) PDF file path

Password

Reading the PDF:
The input file is opened in read mode using PyPDF2.PdfReader().

Creating a New PDF:
A new PDF object is created, and pages from the input file are copied.

Applying Encryption:
The encrypt() function is used to secure the PDF with a password.

Saving the Encrypted File:
The final encrypted PDF is saved to the output path.

Error Handling:
Handles missing, invalid, or unreadable files gracefully.

# 🧠 Key Concepts Covered

File handling in Python

Working with PDFs using PyPDF2

Implementing encryption for document security

Using command-line arguments

Exception handling for robust execution

# 🚀 Step-by-Step Implementation:

1. Install Dependencies:

pip install PyPDF2

2. Run the Script:

python pdf_protect.py input.pdf output.pdf yourpassword

3.Result
A new encrypted PDF file (output.pdf) is generated, requiring the specified password to open.

# 🎯 Expected Outcomes

By completing this project, you will:

Learn how to manipulate PDF files using Python.

Understand the basics of encryption for file security.

Gain experience handling command-line inputs.

Build a practical tool for securing confidential PDF documents.

# OUTPUT:


