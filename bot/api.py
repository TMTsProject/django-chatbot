import requests
from urllib.parse import quote

# encoding
def encodeInput(text):
    encoded_text = "text=" + quote(text) + "&language=en-US"
    return encoded_text
    
# language tool api
def languageTool(text):
    url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"
    
    inputText = encodeInput(text)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "49491d0e58mshc6937e8d420377ap1de6f6jsn6ea9c2dcaa0b",
        'x-rapidapi-host': "dnaber-languagetool.p.rapidapi.com"
    }

    response = requests.request("POST", url, data=inputText, headers=headers)
    matches =  response.json()['matches']
    
    if matches == []:
       # 맞는 문장
        #msg = "Correct!"
        msg = ""
    else:
        #틀린 문장    
        msg = ""
		# 오류가 여러개면 여러개 출력하도록 함.
        mis = False
        for m in range(len(matches)):
            err =  matches[m]['shortMessage']
            # spelling mistake : 철자오류 또는 띄어쓰기 오류
            # 그런 종류의 오류는 무시함
            if err == 'Spelling mistake' :
                if mis :
                    continue
                msg += "There is a spelling mistake. The chatbot may not work smoothly.<br>"
                mis = True
                continue
            elif err == '':
                continue
            msg += err + " : " + matches[m]['message'] + '<br>'
            msg += 'Can be replaced by : '
            rep = matches[m]['replacements']
            for i in range(len(rep)):
                msg += rep[i]['value']
                if i != len(rep)-1:
                    msg += ', '
            msg += '\n'
    return msg
