# Creating Markdown of the Bible using the getbible gateway
import os
import requests

aov_link = "https://api.getbible.net/v2/aov.json"
kjv_link = "https://api.getbible.net/v2/kjv.json"

def zero_number(number):
    if number < 10:
        return f"0{number}"
    else:
        return str(number)


def generate_header(book, chapter, has_next_chapter=True):
    navbar = header_navbar(book, chapter, has_next_chapter)
    return f"""# {book} {chapter}

{navbar}
***

"""
    
def header_navbar(book, chapter, has_next_chapter = True):
    "[[Gen-02|← Genesis 02]] | [[Genesis]] | [[Gen-04|Genesis 04 →]]"
    book_short = book[:3] 
    str_chapter = zero_number(chapter)
    previous_chapter = zero_number(chapter-1)
    next_chapter = zero_number(chapter+1)

    if chapter > 1 and has_next_chapter:
        return f"[[{book_short}-{previous_chapter}|← {book} {previous_chapter}]] | [[{book}]] | [[{book_short}-{next_chapter}|{book} {next_chapter} →]]"
    elif chapter == 1 and has_next_chapter:
        return f"[[{book}]] | [[{book_short}-{next_chapter}|{book} {next_chapter} →]]"
    elif chapter == 1 and not has_next_chapter:
        return f"[[{book}]]"
    elif chapter > 1 and not has_next_chapter:
        return f"[[{book_short}-{previous_chapter}|← {book} {previous_chapter}]] | [[{book}]]"
    


aov = requests.get(kjv_link).json()
folder = './KJV'
for book in aov['books']:
    book_name = book['name']
    short_book_name = book['name'][:3]
    chapters = book['chapters']
    number = zero_number(book['nr'])
    
    book_folder = (f"{number} - {book_name}")
    book_folder_path = os.path.join(folder, book_folder)
    try:
       os.makedirs(book_folder_path)
    except:
        pass
    for chapt in chapters:
        chapter_number = zero_number(chapt['chapter'])
        has_next_chapter = True
        if chapt['chapter'] == len(chapters):
            has_next_chapter = False
        file = f"{short_book_name}-{chapter_number}.md"
        file_path = os.path.join(book_folder_path, file)
        header_navbar_text = generate_header(book_name, chapt['chapter'], has_next_chapter=has_next_chapter)
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(header_navbar_text)
            for verse in chapt['verses']:
                f.write(f"###### v{verse['verse']}\n")
                f.write(f"{verse['text']}\n")
