import os
import re
import json
import openai
from PyPDF2 import PdfReader

# Paths
INDEX_PATH = "resources/index.json"       # Where index.json is located
META_STRATEGY_PATH = "MetaStrategy.md"    # Path to your meta strategy file
RESOURCES_DIR = "resources"               # Where the input PDF/TXT files are stored
PHILOSOPHIES_DIR = "philosophies"         # Output location for .md and .json

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("The environment variable 'OPENAI_API_KEY' is not set. Please set it to your OpenAI API key.")

# Set the OpenAI API key for the library
openai.api_key = OPENAI_API_KEY

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_meta_strategy(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Meta strategy file '{path}' not found.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_dialectic_strategy(meta_prompt, content):
    stream = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": meta_prompt},
            {"role": "user", "content": content}
        ],
        model="gpt-4o",
        stream=True
    )
    result = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content
    return result

def main():
    # 1) Load index.json
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"Index JSON file '{INDEX_PATH}' not found.")

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # We expect index_data to have "selfs" and "resources" arrays
    all_selfs = index_data.get("selfs", [])
    all_resources = index_data.get("resources", [])

    # Build a quick lookup: self_id -> self_name
    self_lookup = {}
    for s in all_selfs:
        self_lookup[s["id"]] = s["name"]

    # 2) Read the meta strategy (only once)
    meta_prompt = read_meta_strategy(META_STRATEGY_PATH)

    # 3) For each resource, generate the strategy
    for res in all_resources:
        self_id = res["self_model"]  # e.g. "1"
        file_name = res["file"]      # e.g. "RespondAndDontReact.txt"

        # Find the "owner" name by self_id
        owner_name = self_lookup.get(self_id)
        if not owner_name:
            print(f"Warning: No 'self' found for id {self_id}. Skipping {file_name}")
            continue

        # Construct the full path to the input resource
        input_path = os.path.join(RESOURCES_DIR, file_name)

        if not os.path.exists(input_path):
            print(f"Warning: File {input_path} not found. Skipping.")
            continue

        # Extract content depending on file extension
        if file_name.lower().endswith(".pdf"):
            content = extract_text_from_pdf(input_path)
        elif file_name.lower().endswith(".txt"):
            content = read_text_file(input_path)
        else:
            print(f"Skipping unsupported file type: {file_name}")
            continue

        # Generate strategy
        print(f"Generating philosophy for {file_name} ...")
        strategy_text = generate_dialectic_strategy(meta_prompt, content)

        # Build output directory: philosophies/<owner_name>/
        output_dir = os.path.join(PHILOSOPHIES_DIR, owner_name)
        os.makedirs(output_dir, exist_ok=True)

        # Build the .md output path by replacing .pdf/.txt with .md
        md_filename = re.sub(r"\.pdf$", ".md", file_name, flags=re.IGNORECASE)
        md_filename = re.sub(r"\.txt$", ".md", md_filename, flags=re.IGNORECASE)
        md_output_path = os.path.join(output_dir, md_filename)

        # Write the .md file
        with open(md_output_path, "w", encoding="utf-8") as f_md:
            f_md.write(strategy_text)

        # Build the .json output path similarly
        json_filename = re.sub(r"\.pdf$", ".json", file_name, flags=re.IGNORECASE)
        json_filename = re.sub(r"\.txt$", ".json", json_filename, flags=re.IGNORECASE)
        json_output_path = os.path.join(output_dir, json_filename)

        # Write the .json file
        data_to_save = {
            "self_id": self_id,  # <--- Store self_id instead of 'owner'
            "file": file_name,
            "strategy": strategy_text,
            "meta_strategy_used": META_STRATEGY_PATH,
        }
        with open(json_output_path, "w", encoding="utf-8") as f_json:
            json.dump(data_to_save, f_json, ensure_ascii=False, indent=2)

        print(f"Saved:\n  {md_output_path}\n  {json_output_path}\n")

if __name__ == "__main__":
    main()