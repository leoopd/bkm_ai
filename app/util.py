# ToDo:
#   - the textbodies end in different 
# Bugs:
#   - does not properly decode utf-8 if type of file unicode text
#   - splits .de-Domains etc. when it shouldnt

from bs4 import BeautifulSoup
import re
import os
import csv

path1 = '/home/leo/coding/python/bkm_ai/test_newsl/20230113-So schützen Sie Ihre Daten-18.html'
path2 = '/home/leo/coding/python/bkm_ai/test_newsl/20220724-Ihre Vorteile als STRATO Kunde - jetzt ansehen!-45.html'
path3 = '/home/leo/coding/python/bkm_ai/test_newsl/20230402-WG_ Welt-Backup-Tag_ 50 % Rabatt auf das HiDrive Geräte-Backup-86.html'

folder_path = '/home/leo/coding/python/bkm_ai/test_newsl'

def newsletter_parser_body(path):
    with open(path, 'rb') as f:
        soup = BeautifulSoup(f, 'html.parser')
        tmp = soup.get_text()
        # Removes occurrences of punctuation (preserves one occurrence), removes extra spaces
        # and inserts the missing spaces between words (can contain äöüßÜÖÄ) and after punctuation.
        tmp = re.sub(r'([^\w\s])\1+', r'\1 ', tmp)
        tmp = re.sub(r'(\s+)([^\w\s])*\s*', r'\2 ', tmp)
        tmp = re.sub(r'(?<=[.,?!])(?=[^\s\d])(?!$)|(?<=[a-zäöüß])(?=[A-ZÜÖÄ])', r' ', tmp)

        # Extracts the text body.
        text = tmp[tmp.find('Hallo'):tmp.find('30 Tage')+11]
        if not text:
            text = tmp[tmp.find('Sehr geehrt'):tmp.find('30 Tage')+11]

        # Same re as above.
        text = re.sub(r'([^\w\s])\1+', r'\1 ', text)
        text = re.sub(r'(\s+)([^\w\s])*\s*', r'\2 ', text)
        text = re.sub(r'(?<=[.,?!])(?=[^\s\d])(?!$)|(?<=[a-zäöüß])(?=[A-ZÜÖÄ])', r' ', text)
        return text

def newsletter_parser_title(path):
        # Tries to find the title as a header.
        try:
            with open(path, 'rb') as f:
                soup = BeautifulSoup(f, 'html.parser')
                title_tag = soup.find_all('span', style="font-size:16px;")
                if not title_tag:
                    title_tag = soup.find_all('span', style="font-size:19px;")
                return title_tag[0].text
                
        except:
            # Looks for a Title embedded into an image.
            try:
                with open(path, 'rb') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    img_title = soup.find_all('img')[1].get('alt')
                    if img_title == 'STRATO AG':
                        img_title = soup.find_all('img')[2].get('alt')
                    return img_title
                    
            except:
                return ''

def newsletter_dict_maker(folder_path):
    prompts = {}

    # Iterates over all files in the folder specified.
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = newsletter_parser_body(file_path)
            title = newsletter_parser_title(file_path)
            if title and text:
                prompts[title] = text
            elif title:
                print(f'{folder_path+"/"+filename} missing text')
            else:
                print(f'{folder_path+"/"+filename} missing title')
        else:
            print(f'{folder_path+"/"+filename} not a file')
    return prompts

def prompts_to_csv(prompts_dict):
    with open('python/bkm_ai/test_output/prompts_output.csv', 'w') as f:
        writer = csv.writer(f, delimiter='#')
        writer.writerow(['Title', 'Text'])
        for title, text in prompts_dict.items():
            writer.writerow([title, text])

prompts_to_csv(newsletter_dict_maker('/home/leo/coding/python/bkm_ai/test_newsl'))