# Bugs:
#   - does not properly decode utf-8 if type of file unicode text
#   - splits .de-Domains etc. when it shouldnt

from bs4 import BeautifulSoup
import re

def newsletter_parser(path):
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
    
path1 = 'python/bkm_ai/test_newsl/Strato Newsletter.html'
path2 = 'python/bkm_ai/test_newsl/Strato Newsletter2.html'
path3 = 'python/bkm_ai/test_newsl/Strato Newsletter3.html'
path4 = 'python/bkm_ai/test_newsl/Strato Newsletter4.html'
path5 = 'python/bkm_ai/test_newsl/Strato Newsletter5.html'



print()
print(newsletter_parser(path1))
print()
print()
print(newsletter_parser(path2))
print()
print()
print(newsletter_parser(path3))
print()
print()
print(newsletter_parser(path4))
print()
print()
print(newsletter_parser(path5))
print()