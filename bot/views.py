import json
import torch
import time

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

# Create your views here.
def home(request):
    context = {}
    return render(request, "chathome.html", context)

@csrf_exempt
def chatanswer(request):
    start = time.time()
    context = {}
    questext = request.GET['questext']
    print(questext)

    import colorama
    rachelModel = settings.rachelModel
    colorama.init()
    print("loading : ", time.time() - start)
    params = {'topk': 3, 'beam': 3, 'topp': 0.8, 'max_t':15}
    instance = request.session.get('instance', 0)
    chat_history = request.session.get("chat_history", "")
   
    def chat3(user_input_text):
        # 임시방편으로 clear history를 이곳에 두었습니다.
        if user_input_text == "clear history":
            request.session['instance'] = 0
            request.session['chat_history'] = ""
            print(f"History cleared! Instance: {request.session['instance']}, History: {request.session['chat_history']}")
            return "History cleared."
        
        # demo.py의 chat함수 호출
        answer, chat_history_from_demo = chat(params, rachelModel, user_input_text, chat_history=chat_history, instance=instance)
        
        # instance, chat_history 정보 세션 관련 DB에 저장
        request.session['instance'] = instance + 1
        request.session['chat_history'] = chat_history_from_demo
        return answer

    anstext = chat3(questext)
    # print("instance", instance)
    # print("chat history", chat_history)
    print("ans : ", time.time() - start)
    print(anstext)

    context['anstext'] = anstext
    context['flag'] = '0'

    return JsonResponse(context, content_type="application/json")

def clear_history(request):
    pass
    # if request.method == "GET":
    #     try:
    #         request.session['instance'] = 0
    #         request.session['chat_history_idx'] = []
    #         request.session["chat_history_ids"] = None
    #         print("Session cleared!")
    #     except:
    #         print("Session is not cleared.")
    #         pass
    # return redirect('home')

def today(request):
    """Shows todays current time and date."""
    today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    context = {'today': today}
    return render(request, 'ch1.html',context)