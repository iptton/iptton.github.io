import os
import re

def process_files():
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.md')]
    for filename in files:
        try:
            with open(filename, 'r+', encoding='utf-8') as f:
                # Check if file is empty
                first_line = f.readline()
                if not first_line:
                    print(f"Skipping empty file: {filename}")
                    continue

                if first_line.strip() != '---':
                    print(f"Processing {filename}")
                    f.seek(0)
                    content = f.read()

                    match = re.match(r'(\d{4}-\d{2}-\d{2})(-(.+))?\.md', filename)
                    if match:
                        date = match.group(1)
                        title_part = match.group(3)

                        if title_part:
                            title = ' '.join(word.capitalize() for word in title_part.split('-'))
                        else:
                            title = date

                        front_matter = f'---\ntitle: "{title}"\ndate: "{date}"\n---\n\n'
                        new_content = front_matter + content

                        f.seek(0)
                        f.write(new_content)
                        f.truncate()
                        print(f"Added front matter to {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    process_files()
