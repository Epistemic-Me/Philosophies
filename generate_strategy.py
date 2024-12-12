import os
import re
import openai
from PyPDF2 import PdfReader
import argparse

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to read text from a file
def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Function to paginate large text
def paginate_text(text, max_length=4000):
    paragraphs = text.split("\n")
    pages = []
    current_page = ""
    for paragraph in paragraphs:
        if len(current_page) + len(paragraph) + 1 > max_length:
            pages.append(current_page)
            current_page = ""
        current_page += paragraph + "\n"
    if current_page:
        pages.append(current_page)
    return pages

# Function to generate a dialectic strategy using OpenAI
def generate_dialectic_strategy(meta_prompt, content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": meta_prompt},
            {"role": "user", "content": content},
        ]
    )
    return response['choices'][0]['message']['content']

# CLI menu system for dynamic interaction
def interactive_menu():
    print("Welcome to the Dialectic Strategy Generator CLI")
    print("Please follow the prompts to generate your strategy.")

    # Get the input file path
    file_path = input("Enter the path to your input file (PDF or TXT): ").strip()
    if not os.path.exists(file_path):
        print("Error: File not found. Please provide a valid file path.")
        return

    # Get the OpenAI API key
    api_key = input("Enter your OpenAI API key: ").strip()

    # Get the meta strategy file path
    meta_file = input("Enter the path to your meta strategy file (press Enter for default 'MetaStrategy.md'): ").strip()
    if not meta_file:
        meta_file = "MetaStrategy.md"

    if not os.path.exists(meta_file):
        print(f"Error: Meta strategy file '{meta_file}' not found.")
        return

    try:
        main(file_path, api_key, meta_file)
    except Exception as e:
        print(f"An error occurred: {e}")

# Main function to process the file and generate a markdown file
def main(file_path, api_key, meta_file="MetaStrategy.md"):
    # Set OpenAI API key
    openai.api_key = api_key

    # Extract content from the file
    if file_path.endswith(".pdf"):
        content = extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        content = read_text_file(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide a PDF or TXT file.")

    # Paginate the content for large files
    pages = paginate_text(content)

    # Read the meta strategy from the specified file
    if not os.path.exists(meta_file):
        raise FileNotFoundError(f"Meta strategy file '{meta_file}' not found.")
    with open(meta_file, "r", encoding="utf-8") as meta:
        meta_prompt = meta.read()

    # Generate the dialectic strategy for each page and aggregate the results
    full_strategy = ""
    for i, page in enumerate(pages):
        print(f"Processing page {i + 1}/{len(pages)}...")
        strategy = generate_dialectic_strategy(meta_prompt, page)
        full_strategy += strategy + "\n\n"

    # Save the result to a markdown file
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"{base_name}_dialectic_strategy.md"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(full_strategy)

    print(f"Dialectic strategy saved to {output_file}")

# Run the program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a dialectic strategy from a text resource.")
    parser.add_argument("--interactive", action="store_true", help="Launch the interactive CLI menu.")
    parser.add_argument("file_path", nargs="?", help="Path to the input PDF or TXT file.")
    parser.add_argument("api_key", nargs="?", help="OpenAI API key.")
    parser.add_argument("--meta_file", default="MetaStrategy.md", help="Path to the meta strategy file (default: MetaStrategy.md).")
    args = parser.parse_args()

    if args.interactive:
        interactive_menu()
    else:
        if not args.file_path or not args.api_key:
            print("Error: Both file_path and api_key are required in non-interactive mode.")
        else:
            main(args.file_path, args.api_key, args.meta_file)

