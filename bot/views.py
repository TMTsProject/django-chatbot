import json
import torch
import time
import colorama

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import settings
from datetime import datetime
from django.utils.dateformat import DateFormat
from static.DialogRPT_files.demo import chat   # for DialogRPT


from . import api

def main(request):
    return render(request, 'main.html')

def api(request):
    return render(request, 'api-ex.html')

def ch1(request):
    return render(request, 'ch1.html')

def ch2(request):
    return render(request, 'ch2.html')

def devInfo(request):
    return render(request, 'info_developer.html')

def home(request):
    context = {}
    return render(request, "chathome.html", context)

@csrf_exempt

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

def clear_history(request):
    pass


def today(request):
    """Shows todays current time and date."""
    today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    context = {'today': today}
    return render(request, 'ch1.html',context)
