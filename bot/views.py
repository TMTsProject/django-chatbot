import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

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
    tokenizer = AutoTokenizer.from_pretrained('static/friends_tokenizer')
    model = AutoModelForCausalLM.from_pretrained("static/friends_model")

    import colorama
    colorama.init()
    print("loading : ", time.time() - start)
    def chat3(user_input_text):
        new_user_input_ids = None
        bot_input_ids = None
        chat_history_ids = None

        new_user_input_ids = tokenizer.encode(user_input_text + tokenizer.eos_token, return_tensors='pt')

        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids],
                                  dim=-1) if chat_history_ids is not None else new_user_input_ids
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

        return answer

    anstext = chat3(questext)
    print("ans : ", time.time() - start)
    print(anstext)

    context['anstext'] = anstext
    context['flag'] = '0'

    return JsonResponse(context, content_type="application/json")
