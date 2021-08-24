#demo.py
import os
import sys
import argparse
import re
import pandas as pd
from numpy import argmax

import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel

from .dialogRPT import getIntegrated
from .src.generation import GPT2Generator

#EOS_token 호출 추가
from .src.shared import EOS_token

# EOS = "<|endoftext|>"

def chat(params, model, inputs, chat_history, instance=0):
    if instance == 0:
        chat_history = inputs
    else :
        chat_history = chat_history + EOS_token + inputs
    ret = model.predict(chat_history, 0.4, params)
    
    final, prob_gen, score_ranker, hyp = ret[0]
    print("Final: %.3f, Gen: %.3f, Ranker: %.3f" % (final, prob_gen, score_ranker))

    chat_history = chat_history + EOS_token + hyp
    return hyp, chat_history


MODEL_PATH = "/static/"

# parser = argparse.ArgumentParser()
# parser.add_argument('--dbname', '-db', type=str, default = 'db.pickle')
# parser.add_argument('--port', '-p', type=int, default = 3305)
# parser.add_argument('--ip', '-i', type=str, default = '0.0.0.0')
# parser.add_argument('--path_generator', '-pg', type=str, default = MODEL_PATH)
# parser.add_argument('--path_ranker', '-pr', type=str, default = "static/DialogRPT_files/restore/ensemble.yml")
# parser.add_argument('--topk', type=int, default=3)
# parser.add_argument('--beam', type=int, default=3)
# parser.add_argument('--wt_ranker', type=float, default=0.4)   # weight param
# parser.add_argument('--topp', type=float, default=0.8)
# parser.add_argument('--max_t', type=int, default=15)
# parser.add_argument('--cpu', action='store_true', help='enables CUDA training')
# args = parser.parse_args()

# cuda = False if args.cpu else torch.cuda.is_available()
# rachelModel.play(args.wt_ranker, params)

# CODES FOR RUNNING THE DEMO IS AS FOLLOWS
# rachelModel = getIntegrated(args.path_ranker, args.path_generator, cuda)
# params = {'topk': args.topk, 'beam': args.beam, 'topp': args.topp, 'max_t':args.max_t}
# chat(params, rachelModel) # begin chatting
