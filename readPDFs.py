from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from stop_words import get_stop_words
import string
from nltk.corpus import words
from nltk.corpus import stopwords
# import nltk
from collections import Counter
from os import listdir
import json
from os.path import isfile, join


with open("words") as f:
    word_list = f.readlines()
word_list = [x.strip() for x in word_list]

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def convert_pdf_to_txt(path):
    # nltk.download()
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        try:
            interpreter.process_page(page)
        except:
            pass

    text = retstr.getvalue()
    text = text.replace('\n', ' ')
    text_list = text.split(' ')

    stop_words = list(get_stop_words('en'))  # About 900 stopwords

    tmp_text_list = [''.join(c for c in s if c not in string.punctuation) for s in text_list]  # Remove punctuation
    tmp_text_list = [s for s in tmp_text_list if s]  # Remove nulls
    tmp_text_list = [w for w in tmp_text_list if w.lower() in word_list]  # Remove words that do not exist in english
    tmp_text_list = [w for w in tmp_text_list if not hasNumbers(w)]  # Remove any strings with numbers

    text_list = [s for s in tmp_text_list if len(s) > 1 and s != 'a']  # Remove single words
    text_list = [w for w in tmp_text_list if not w.lower() in stop_words]  # Remove Stopwords

    word_counts = Counter(text_list)
    tmp_dict = {}

    for word_i in word_counts:
        try:
            tmp_list = []
            for j, word_j in enumerate(tmp_text_list):
                if word_i == word_j:
                    tmp_list.append(tmp_text_list[j + 1].lower())
            tmp_dict[word_i] = Counter(tmp_list)
        except:
            pass

    fp.close()
    device.close()
    retstr.close()
    return word_counts, tmp_dict


files = [f for f in listdir("PDFs") if isfile(join("PDFs", f))]
sum = Counter()
failed_files = 0
item = 1
succeeding_word_list = []
for file in files:
    print("Reading file: " + file + " (" + str(item) + "/" + str(len(files)) + ")")
    item += 1
    try:
        occurs, succeeding = convert_pdf_to_txt("PDFs/" + file)
        sum += occurs
        succeeding_word_list.append(succeeding)
    except Exception:
        failed_files += 1

# Combine those word lists
final_succeeding_words = {}
for counter in succeeding_word_list:
    for key in counter:
        if key in final_succeeding_words:
            final_succeeding_words[key] += counter[key]
        else:
            final_succeeding_words[key] = counter[key]

print("Failed Files: " + str(failed_files))

json_obj = {}
for k, v in sum.items():
    word = {}
    word['freq'] = v
    if k in final_succeeding_words.keys():
        word['next_word'] = final_succeeding_words[k]
    else:
        word['next_word'] = Counter()
    json_obj[k] = word
    # json_obj[k]['next_word'] = final_succeeding_words[k]

with open('wordcount.json', 'w') as outfile:
    json.dump(json_obj, outfile)


