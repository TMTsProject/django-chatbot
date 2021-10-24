# 언어학습 챗봇 with Friends

# 목차
- [1. 코드 설명](#1-코드-설명)  
  * [1-1. 전처리 설명](#1-1-전처리-설명)
  * [1-2. 모델링 설명](#1-2-모델링-설명)
    + [1-2-1. DialoGPT 입력 형식에 맞는 데이터 셋으로 재구성](#1-2-1-dialogpt-입력-형식에-맞는-데이터-셋으로-재구성)
  * [1-3. 백엔드에서 모델 활용방안 설명](#1-3-백엔드에서-모델-활용방안-설명)
    + [1-3-1. views.py](#1-3-1-viewspy)
    + [1-3-2. demo.py의 chat함수](#1-3-2-demopy의-chat함수)
- [2. 사용방법](#2-사용방법)
  * [2-1. DialoGPT 학습](#2-1-dialogpt-학습)
  * [2-2. git clone](#2-2-git-clone)
  * [2-3. DialogRPT 모델 다운로드](#2-3-dialogrpt-모델-다운로드)
  * [2-4. 로컬에서 실행](#2-4-로컬에서-실행)
- [3. 팀원](#3-팀원)  


# 1. 코드 설명  
## 1-1. 전처리 설명

- 사용 데이터 : data/friends_raw_data 폴더의 시즌1.txt ~ 시즌10.txt
- 코드 : data/friends_data_processing.ipynb
- 지문, 나레이션과 같이 대사가 아니거나, 학습에 안 좋은 영향을 줄 수 있는 부분은 정규식을 활용하여 제거하였습니다.
  ~~~
  ex) ‘(explaining to the others) Carol moved her stuff out today.’  
	    -> Carol moved her stuff out today.
  ~~~
- 캐릭터 명이 일정하지 않은 부분을 일정하도록 변환하였습니다.
  ~~~
  ex) Rachel, RACHEL, Rach는 모두 같은 인물을 가리키는 말이므로,   
      문자를 전부 소문자화하고, rach를 rachel로 바꿔주었습니다.
  ~~~
  
- 주요 코드는 아래와 같습니다:
~~~python
# 전처리한 데이터를 저장할 데이터프레임 생성  
# 장면 번호 : 캐릭터 : 대사 형식으로 생성
data = pd.DataFrame(columns=['Scene', 'Character', 'Line'], dtype=str)
data['Scene'] = data['Scene'].astype(int)

scene_num = 0

for f_name in file_list:
    with open(PATH+f_name, 'r') as f:
	lines = f.readlines()
	for line in lines:
	    # Rachel : Hi! 처럼 대사구분이 ':'로 되어있으므로 이를 기준으로 캐릭터명과 대사를 구분함
	    if ':' in line:
		script = line.strip().split(':')
		# :가 여러번 나오면 뒤는 대사에 포함되게 함.
		if (script[0].lower()[:6] == '[scene') or (script[0].lower()[:6] == '(scene'):
		    scene_num += 1
		data = data.append({'Scene': scene_num, 'Character' : script[0].lower(), 'Line':(' ').join(script[1:])},ignore_index=True)

# 대사가 아닌 부분, 즉 지문이나 설명, 나레이션은 삭제함
idxList = []
for idx in range(len(data['Character'])):
    if 'by' in data['Character'][idx] :
	idxList.append(idx)
    elif 'note' in data['Character'][idx] :
	idxList.append(idx)
    elif 'scene' in data['Character'][idx] :
	idxList.append(idx)
    elif 'with' in data['Character'][idx] :
	idxList.append(idx)
    elif data['Character'][idx][0] == '{':
	idxList.append(idx)
    elif data['Character'][idx][0] == '[':
	idxList.append(idx)
    elif data['Character'][idx][0] == '(':
	idxList.append(idx)
    elif data['Character'][idx] == 'cut to' :
	idxList.append(idx)
    elif data['Character'][idx] == 'narrator' :
	idxList.append(idx)

data.drop(idxList , inplace=True)
data = data.reset_index(drop=True)

# 캐릭터명 통일
# 캐릭터명에 오타가 있는 경우, 대문자/소문자가 다른 경우, 이름을 줄인 경우 그리고 이름에 괄호가 있는 경우를 없애고 모두 하나로 통일시킴
# Ex. Rach -> rachel, RACHEL -> rachel 등
for i in range(len(data['Character'])):
    if 'and' in data['Character'][i]:
	continue
    if "ross " in data['Character'][i]:
	data['Character'][i] = "ross" 
    elif "rachel " in data['Character'][i]:
	data['Character'][i] = "rachel"
    elif "chandler " in data['Character'][i]:
	data['Character'][i] = "chandler"
    elif "monica " in data['Character'][i]:
	data['Character'][i] = "monica" 
    elif "phoebe " in data['Character'][i]:
	data['Character'][i] = "phoebe" 
    elif "joey " in data['Character'][i]:
	data['Character'][i] = "joey"
    elif "joey's voice" in data['Character'][i]:
	data['Character'][i] = "joey"
    elif "amy " in data['Character'][i]:
	data['Character'][i] = "amy"

for idx in range(len(data['Line'])):
    data['Character'][idx] = re.sub('\(.*\)','', data['Character'][idx])
    data['Character'][idx] = re.sub('\[.*\]','', data['Character'][idx])
    data['Character'][idx] = re.sub('  ', ' ', data['Character'][idx])
    data['Character'][idx] = data['Character'][idx].strip()
    data['Line'][idx] = re.sub('\(.*\)','', data['Line'][idx])
    data['Line'][idx] = re.sub('\[.*\]','', data['Line'][idx])
    data['Line'][idx] = re.sub('  ', ' ', data['Line'][idx])
    data['Line'][idx] = data['Line'][idx].strip()

data['Character'][data['Character']== "rachel/ross"] = "rachel"
data['Character'][data['Character']== "rach"] = "rachel"
data['Character'][data['Character']== "rahcel"] = "rachel"
data['Character'][data['Character']== "racel"] = "rachel"	
data['Character'][data['Character']== "chan"] = "chandler"
data['Character'][data['Character']== "mnca"] = "monica"
data['Character'][data['Character']== "phoe"] = "phoebe"

indexNames = data[ data['Line'] == '' ].index
data.drop(indexNames , inplace=True)
data = data.reset_index(drop=True)
~~~

## 1-2. 모델링 설명
- 데이터 : Data/Friends.csv
- 코드 : Data/Friends_DialoGPT.ipynb  

### 1-2-1. DialoGPT 입력 형식에 맞는 데이터 셋으로 재구성
- 전처리(1-1)의 과정 후 EDA를 통해 Rachel의 발화가 가장 많은 것을 알고, Rachel의 페르소나를 입힌 챗봇을 구현하기로 하였습니다.  
- DialoGPT의 입력에 맞게 중심인물(Rachel)의 발화와 그 이전 발화 3개로 데이터셋을 재구성하였습니다.
- 다만, 해당 발화 셋이 문맥에서 벗어나는 경우를 방지하기 위해 Scene 값을 활용하여 다른 Scene 값을 가질 때에는 재구성한 데이터셋에서 제외하였습니다.
~~~python
# 데이터셋 재구성
contexted = []
n = 3
for i in range(n, len(data['Line'])):
    if data['Character'][i] == 'rachel':
        row = []
        prev = i - 1 - n
        if data['Scene'][i-n] == data['Scene'][i]:
            for j in range(i, prev, -1):
                row.append(data['Line'][j])
            contexted.append(row)  
    
columns = ['response', 'context']
columns = columns + ['context_'+str(i+2) for i in range(n-1)]
df = pd.DataFrame.from_records(contexted, columns=columns)
~~~
- DialoGPT 모델 실행 코드는 아래와 같습니다.
~~~python
new_user_input_ids = None
bot_input_ids = None
chat_history_ids = None

step = 0
chat_history_idx = []

while True:
    user_input_text = input(">> User: ")
    new_user_input_ids = tokenizer.encode(user_input_text + tokenizer.eos_token, return_tensors='pt')
    
    # grammar bot
    print(languageTool(user_input_text), end='')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids != None else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens
    #샘플링 방식임
    chat_history_ids = model.generate(
        bot_input_ids, max_length=1000,
        pad_token_id=tokenizer.eos_token_id,  
        no_repeat_ngram_size=3,       
        do_sample=True, 
        top_k=100, 
        top_p=0.7,
        temperature = 0.8
    )
    step += 1
    
    # pretty print last ouput tokens from bot
    print("Rachel: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
    chat_history_idx.append(chat_history_ids.shape[-1])

    #오래된 히스토리는 삭제하여 대화가 원활하게 이어지도록 함.
    if step > 5:
        cv = subIdx(chat_history_idx)
        chat_history_ids = chat_history_ids[:, cv:]

~~~

## 1-3. 백엔드에서 모델 활용방안 설명
django app의 `views.py`와 DialogRPT_files 폴더의 `demo.py`를 중심으로 아래와 같이 설명합니다.

### 1-3-1. views.py
views.py에서 가장 핵심이 되는 함수는 `chatanswer`함수입니다. 이 함수는 아래와 같이 구성되어 있으며, 코드 설명은 주석을 참고 부탁드립니다.
~~~python
def chatanswer(request):
    start = time.time()
    context = {}
    questext = request.GET['questext']   # 사용자가 입력한 텍스트를 프론트에서 받음
    print(questext)

    # Rachel 페르소나가 투영된 모델(DialoGPT, DialogRPT가 Integrated된 형태)을 불러옴
    rachelModel = settings.rachelModel
    colorama.init()
    print("loading : ", time.time() - start)
    params = {'topk': 3, 'beam': 3, 'topp': 0.8, 'max_t':15}   # 하이퍼파라미터 설정
    
    # 채팅 히스토리 기록을 session에 저장한다
    instance = request.session.get('instance', 0)
    chat_history = request.session.get("chat_history", "")
   

    # 사용자 input에 대한 채팅의 output 반환 함수
    def chat3(user_input_text):
        
        # 사용자가 채팅 히스토리를 초기화하는 커맨드 입력시
        if user_input_text == "clear history":
            request.session['instance'] = 0
            request.session['chat_history'] = ""
            print(f"History cleared! Instance: {request.session['instance']}, History: {request.session['chat_history']}")
            return "System: History cleared."
        
        # DialogRPT 파일의 demo.py에 작성되어 있는 chat함수 호출함으로써 챗봇의 응답을 불러온다
        # answer: 채팅 반환값, chat_history_from_demo: 채팅 히스토리
        answer, chat_history_from_demo = chat(params, rachelModel, user_input_text, chat_history=chat_history, instance=instance)
        
        # instance, chat_history 정보를 session에 저장
        request.session['instance'] = instance + 1
        request.session['chat_history'] = chat_history_from_demo
        return answer

    anstext = chat3(questext)
    print("ans : ", time.time() - start)
    print(anstext)

    context['anstext'] = anstext
    context['flag'] = '0'

    return JsonResponse(context, content_type="application/json")   # 프론트로 챗봇 응답 전달
~~~

### 1-3-2. demo.py의 chat함수
chat함수는 사용자가 입력한 텍스트에 대해 DialogRPT가 점수를 매겨서, 가장 최선의 답이라고 생각되는 챗봇의 응답을 반환합니다. 이 함수는 아래와 같이 구성되어 있으며, 코드 설명은 주석을 참고 부탁드립니다.

~~~python
def chat(params, model, inputs, chat_history, instance=0):
    """
    - params: 입력받은 하이퍼파라미터
    - model: DialoGPT와 DialogRPT가 Integrated된 모델 (Rachel 페르소나 투영된 모델)
    - inputs: 사용자가 입력한 텍스트
    - chat_history: 채팅을 하는동안 저장된 채팅 히스토리
    - instance: 채팅이 몇 번 이루어졌는지 기록
    """
    
    # instace변수를 참고하여, 채팅을 처음하는지 여부를 판단하여 채팅 히스토리 기록
    if instance == 0:
        chat_history = inputs
    else :
        chat_history = chat_history + EOS_token + inputs

    # 채팅 히스토리를 고려한 응답 정보을 DialogRPT가 scoring한 순서로 ret 변수에 저장
    # 정보는 앙상블된 점수(final), DialoGPT가 예측한 점수(prob_gen), DialogRPT가 예측한 점수(score_ranker), 챗봇 응답(hyp)으로 구성
    ret = model.predict(chat_history, 0.4, params)  
    final, prob_gen, score_ranker, hyp = ret[0]

    print("Final: %.3f, Gen: %.3f, Ranker: %.3f" % (final, prob_gen, score_ranker))

    chat_history = chat_history + EOS_token + hyp   # chat_history에 채팅 기록 저장
    return hyp, chat_history
~~~


# 2. 사용방법
DialogRPT scoring 모델은 총 용량이 매우 큰 관계로(약 9GB), 아래 2-3을 참고하셔서 로컬에 다운로드 하셔야 합니다.

## 2-1. DialoGPT 학습
`notebooks/Friends_DialoGPT.ipnyb`를 이용하여 얻은 model을 이용하여 학습합니다.  
그 후, 학습한 모델을 `static`폴더에 `friends_model`이라는 이름으로 저장합니다.

## 2-2. git clone
git bash에서 아래의 커맨드를 입력하여 본 레포지토리를 git clone합니다.
~~~
git clone https://github.com/TMTsProject/django-chatbot
~~~

## 2-3. DialogRPT 모델 다운로드
용량이 매우 큰 관계로, DialogRPT 저자가 공개한 레포지토리에서 직접 받으셔야 합니다. [이 링크](https://github.com/golsun/DialogRPT)를 통해 접속 가능합니다.  
접속 후엔, `updown`와 `human_vs_rand` 두 pretrain 모델을 다운로드 받으시고, `django-chatbot/static/DialogRPT_files/restore` 경로에 두 파일을 저장해줍니다.

## 2-4. 로컬에서 실행
manage.py가 있는 경로에서 아래의 코드를 실행합니다. DB 관련으로 실행해야 하는 코드입니다.
~~~
python manage.py makemigrations
python manage.py migrate
~~~

그 후, 로컬에서 실행해줍니다.
~~~
python manage.py runserver
~~~

# 3. 팀원
- 이수빈(한국외국어대학교)
- 옥명주(경북대학교)
- 이호재(한국외국어대학교)
- 류미소(한국외국어대학교)
- 김리아(한국외국어대학교 일반대학원)
