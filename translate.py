import requests
import re
import time
from PyPDF2 import PdfReader
from tqdm import tqdm

def papagoAPI(id, secret, sentence):
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers ={"X-Naver-Client-Id": id, "X-Naver-Client-Secret": secret}
    params = {"source": "en", "target": "ko", "text": sentence}
    response =requests.post(request_url, headers=headers, data=params)
    try:
        result = response.json()
        result["message"]["result"]["translatedText"]
    except:
        print(result)
        exit()
    return result["message"]["result"]["translatedText"]
'''
The format of Example format in response.json
Input: How are you?
{
    'message': 
    {
        '@type': 'response', 
        '@service': 'naverservice.nmt.proxy', 
        '@version': '1.0.0', 
        'result': 
            {
                'srcLangType': 'en', 
                'tarLangType': 'ko', 
                'translatedText': '어떻게 지내니?', 
                'engineType': 'N2MT', 
                'pivot': None
            }
    }
}
'''

def pdfToText(inputFile:str)->str:
    """English PDF file translate to Korean txt format
    Args:
        inputFile (str): pdf path
    Returns:
        str: extracted english txt
    """
    reader = PdfReader(inputFile)
    number_of_pages = len(reader.pages)
    
    print("Number of pages : ", number_of_pages)

    # pdf Txt parser
    ext_text = ""
    temp = ""
    for i in tqdm(range(number_of_pages)):
        page = reader.pages[i]
        temp = page.extract_text()
        temp = temp.replace("\n", " ")
        ext_text = ext_text + temp
        temp = ""
    print("Total txt length : ", len(ext_text))

    # Find a word with a period 
    # and create a sentence by a regular expression.
    txt = ""
    final_sent = re.compile("[a-z]*\.")
    for i in range(len(ext_text)):
        txt = txt + ext_text[i]
        m = final_sent.findall(ext_text[i])
        if m:
            txt = txt + "\n"

    # save txt to res_text.txt
    with open('./data/res_text.txt', 'wb') as f:
        f.write(txt.encode('UTF-8'))

    # read res_text.txt
    with open('./data/res_text.txt', 'rb') as f:
        text = f.readlines()

    print("extracted txt length : ", len(text))
    return text

def trans(id:str, secret:str, inputtext:str, line:int=None):
    """Save to txt using Papago API

    Args:
        id (str): Naver client id
        secret (str): Naver ClientSecret
        inputtext (str): wanna be input .txt
        line (int, optional): wanna be lines. Defaults to None.
    """
    text = ""
    for i, txt in tqdm(enumerate(inputtext)):
        if isinstance(line, int) and i >= line:
            break
        result_txt = papagoAPI(id, secret, txt)
        # print("번역결과 {} : {}".format(i, result_txt))
        text = text + result_txt + "\n"
        time.sleep(2)

    with open("./data/trans_result.txt", 'w', encoding='utf-8') as trans_file:
        trans_file.write(text)
    
import os
if __name__ == "__main__":
    #PDF name
    file_name = 'example.pdf'
    # pdf to text 함수 호출
    eng_text = pdfToText(os.path.join('./data/', file_name))
    # Naver 번역 API ID, Secret(password)
    # 발급받은ClientID
    id = 'd8HqVxml_YQaSzipnJwI' 
    # 발급받은ClientSecret
    secret = 'PiOCQ9ffFs' 
    # Text 영문, Papago 번역후 Text파일저
    trans(id, secret, 
        eng_text)
