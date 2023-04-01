# ToDo:
#   - add functionality to handle cases where title and or body cant be extracted due to format inconsistencies
# Bugs:
#   - does not properly decode utf-8 if type of file unicode text
#   - splits .de-Domains etc. when it shouldnt

from bs4 import BeautifulSoup
import re
import os

def newsletter_parser_body(path):
    with open(path, 'rb') as f:
        soup = BeautifulSoup(f, 'html.parser')
        tmp = soup.get_text()

        # Extracts the text body (always starts with 'Hallo' and ends with 'STRATO Team').
        text = tmp[tmp.find('Hallo'):tmp.find('STRATO Team')+11]

        # Removes occurrences of punctuation (preserves one occurrence), removes extra spaces.
        text = re.sub(r'([^\w\s])\1+', r'\1 ', text)
        text = re.sub(r'(\s+)([^\w\s])*\s*', r'\2 ', text)

        # Inserts the missing spaces between words (can contain äöüßÜÖÄ) and after punctuation.
        text = re.sub(r'(?<=[.,?!])(?=[^\s\d])(?!$)|(?<=[a-zäöüß])(?=[A-ZÜÖÄ])', r' ', text)

        return text
    
def newsletter_parser_title(path):
    with open(path, 'rb') as f:
        soup = BeautifulSoup(f, 'html.parser')

        # Tries to find the title as a header.
        try:
            title = soup.find_all('span', style="font-size:16px;")[0].text
            return title
        except IndexError:

            # Looks for a Title embedded into an image.
            try:
                img_title = soup.find_all('img')[1].get('alt')
                return img_title
            except IndexError:
                return ''

def newsletter_dict_maker(folder_path):
    prompts = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = newsletter_parser_body(file_path)
            title = newsletter_parser_title(file_path)
            if title:
                prompts[title] = text
    return prompts

prompts = newsletter_dict_maker('/home/leo/coding/python/bkm_ai/test_newsl')

for prompt in prompts.items():
    print(prompt)
    print('\n###\n')