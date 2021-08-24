import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
from config import settings
from datetime import datetime
from django.utils.dateformat import DateFormat

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
    model = settings.model
    tokenizer = settings.tokenizer
    colorama.init()
    print("loading : ", time.time() - start)

    def subIdx(a):
        v = a.pop(0)
        for i in range(len(a)):
            a[i] -= v
        return v

    def chat3(user_input_text):
        instance = request.session.get('instance', 0)
        chat_history_idx = request.session.get('chat_history_idx', [])
        chat_history_ids = request.session.get("chat_history_ids", None)
        
        chat_history_ids = None if instance == 0 else torch.LongTensor(chat_history_ids)
        new_user_input_ids = tokenizer.encode(user_input_text + tokenizer.eos_token, return_tensors='pt')

        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids],
                                  dim=-1) if chat_history_ids != None else new_user_input_ids
        chat_history_ids = model.generate(
            bot_input_ids, max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )
        answer = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        request.session['instance'] = instance + 1
        request.session['chat_history_idx'] = chat_history_idx + [chat_history_ids.shape[-1]]

        # print("instance", instance)
        # print("chat_history_idx", chat_history_idx)

        if request.session['instance'] > 5:
            cv = subIdx(request.session['chat_history_idx'])
            chat_history_ids = chat_history_ids[:, cv:]
        
        request.session['chat_history_ids'] = chat_history_ids.tolist()

        # print("chat_history_ids:", chat_history_ids)

        return answer

    anstext = chat3(questext)
    # print("ans : ", time.time() - start)
    # print(anstext)

    context['anstext'] = anstext
    context['flag'] = '0'

    return JsonResponse(context, content_type="application/json")

def clear_history(request):
    if request.method == "GET":
        try:
            request.session['instance'] = 0
            request.session['chat_history_idx'] = []
            request.session["chat_history_ids"] = None
            print("Session cleared!")
        except:
            print("Session is not cleared.")
            pass
    return redirect('home')

def today(request):
    """Shows todays current time and date."""
    today = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    context = {'today': today}
    return render(request, 'ch1.html',context)