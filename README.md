# 프로젝트 제목 이곳에

데모 실행 방법 기술
(Raw 데이터 및 전처리 데이터 일체, 코딩 파일, README 파일을 zip 형태로 제출, 코드 설명 및 사용방법을 포함하는 README 파일(.txt 또는 .md 확장자)을 제출하고, 진행 과정이 이해가도록 코드 내 주석을 반드시 포함)  

# 1. 코드 설명
## 1-1. 전처리 설명
설명설명

## 1-2. 모델링 설명
설명설명

## 1-3. 백엔드에서 모델 활용방안 설명
django app의 `views.py`와 DialogRPT_files 폴더의 `demo.py`를 중심으로 아래와 같이 설명합니다.

### 1-3-1. views.py
views.py에서 가장 핵심이 되는 함수는 `chatanswer`함수입니다. 이 함수는 아래와 같이 구성되어 있으며, 코드 설명은 주석을 참고 부탁드립니다.
~~~
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

### 1-3-2. `DialogRPT_files\src\demo.py`의 chat함수
chat함수는 사용자가 입력한 텍스트에 대해 DialogRPT가 점수를 매겨서, 가장 최선의 답이라고 생각되는 챗봇의 응답을 반환합니다. 이 함수는 아래와 같이 구성되어 있으며, 코드 설명은 주석을 참고 부탁드립니다.

~~~
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
설명설명

## 2-2. git clone
git bash에서 아래의 커맨드를 입력하여 git clone 해옵니다.
~~~
git clone https://github.com/Nokomon/django-chatbot
~~~

## 2-3. DialogRPT 모델 다운로드
용량이 매우 큰 관계로, DialogRPT 저자가 공개한 레포지토리에서 직접 받으셔야 합니다. [이 링크](https://github.com/golsun/DialogRPT)를 통해 접속 가능합니다.  
접속 후엔, `depth`와 `human_vs_rand` 두 pretrain 모델을 다운받으시고, `django-chatbot\static\DialogRPT_files\restore` 경로에 두 파일을 저장해줍니다.

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
