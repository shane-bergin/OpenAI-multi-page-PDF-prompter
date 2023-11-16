import openai
import fitz  # PyMuPDF
import os
import argparse
import sys

root_path = os.path.abspath(os.path.dirname(__name__))

# Path to file containing API key
api_key_file_path = f"{root_path}/openai_key"

with open(api_key_file_path, 'r') as f:
    openai.api_key = f.read().strip()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--chunk_len', type=str, default='2000')
    parser.add_argument('--temperature', type=str, default='0.2')
    parser.add_argument('--context_filter', type=str, default=None)
    parser.add_argument('--return_file', type=str, default=f"{root_path}/summarized.txt")
    parser.add_argument('--pdf_path', type=str, default=f"{root_path}/your_file.pdf")
    parser.add_argument('--system_prompt', type=str, default="You are a summarization assistant.")
    parser.add_argument('--user_prompt', type=str, default="Summarize the following text")
    parser.add_argument('--import_dir', type=str, default=f'{root_path}')

    args = parser.parse_args()

    handle(args)

def handle(args):
    chunk_len = int(args.chunk_len)
    temperature = float(args.temperature)
    context_filter = args.context_filter
    return_file = args.return_file
    pdf_path = args.pdf_path
    system_prompt = args.system_prompt
    user_prompt = args.user_prompt
    import_dir = args.import_dir

    file_contents = []

    #iterate over all files in directory
    for root, subdirs, files in os.walk(import_dir):
        for file in files:
            # do conditional extension check here
            file = os.path.join(root, file)
            # if pdf file, read it
            if file.endswith('.pdf'):
                try:
                    text = read_pdf(file)
                    file_contents.append(text)
                except Exception as e:
                    print(e)
            else:
                try:
                    with open(file, 'r') as f:
                        all_txt = re.sub(r'(\s)\s+', r'\1', f.read()) 
                        file_contents.append(all_txt)
                except Exception as e:
                    print(e)

    # text = read_pdf(pdf_path)
    text = ' '.join(file_contents)

    if text:
        summarized_text = summarize_text_with_openai(text, chunk_len=chunk_len, temperature=temperature, context_filter=context_filter, return_file=return_file, system_prompt=system_prompt, user_prompt=user_prompt)
        print(summarized_text)
    else:
        print("Failed to extract text from the PDF.")

def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def summarize_text_with_openai(text, chunk_len=2000, temperature=0.2,context_filter=None, return_file=f"{root_path}/summarized.txt", system_prompt="You are a summarization assistant.", user_prompt="Summarize the following text"):
    prompt_chunks = [text[i:i + chunk_len] for i in range(0, len(text), chunk_len)]
    summarized_text = ""
    context_filter_arr = context_filter.split(',') if context_filter else None
    filtered_chunks = [text for text in prompt_chunks if any(context_filter in text for context_filter in context_filter_arr)] if context_filter_arr else prompt_chunks
    for i, chunk in enumerate(filtered_chunks):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"{system_prompt}"},
                    {"role": "user", "content": f"{user_prompt}:\n{chunk}"}
                ],
                max_tokens=min(4096, chunk_len),
                temperature=temperature
            )
            summarized_text += response['choices'][0]['message']['content'].strip() + "\n"
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {str(e)}")
    with open(return_file, 'a') as f:
        f.write(summarized_text)
    return summarized_text



if __name__ == '__main__':
    main()