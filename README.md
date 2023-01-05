# Translate English Journal

### English PDF file to Korean Text file using python
The this Code that uses Naver Papago API to translate and save as a Korean text file.

* Papago API는 한 번에 5,000자 1일에 10,000자 까지 번역 서비스를 제공한다.


## Requirements
```
    conda install --file requirements.txt
    python translate.py
```
## How to use
1. First Get an Papago API key.
2. Change to Line 
```python
    if __name__ == "__main__":
        #PDF name
        file_name = ''
        # PDF to Txt
        eng_text = pdfToText(os.path.join('./data/', file_name))
        # Naver papgo API ID, Secret(password)
        # ClientID
        id = '' 
        # ClientSecret
        secret = '' 
        # Translate English txt
        trans(id, secret,  eng_text)
```