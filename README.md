# Building a Platform for Learning English with a Persona-applied Chatbot through DialoGPT and DialogRPT

This is a repository for storing codes for the main project of Data on Air 2021 (데이터 청년 캠퍼스 2021).  

Our team created an open domain chatbot which reflects a persona of someone, by having the chatbot train to imitate the utterances of him/her.  

Having known that open-domain chatbots may significantly help those who wish to learn a language, we have created one that reflects the persona of Rachel Green from the drama 'Friends.' We used **DialoGPT** as a baseline model, but have integrated **DialogRPT** approaches so that the responses that the chatbot generates are not bland. A **PyTorch**-based code was used for DialoGPT and DialogRPT modeling.  

When it comes to the "learning" part, we implemented an api from [LanguageTool](https://languagetool.org/). We linked the message that the user would type to LanguageTool in order to check whether there are spelling or grammatical errors in the user's text.  

I was responsible for data gathering, pre-processing, analyzing the modeling techniques we were to implement by examining the Hugginface Github repository, modeling the chatbots, and back-end related tasks during deploying via **Django**.

This repository generally stores everything including the Django codes, but the trained models (trained DialoGPT models) and the baseline DialogRPT models are missing, due to a storage limit. Please refer [here](https://www.notion.so/nokomon/aae788a23cab4c5882beef2af11370a1#9f33f8bd79614c2eb19b31b55a745b6c) for a demonstration video of our project.

-----------------------------------
# 개발 로그  

## static 폴더 없음
static 폴더의 friends_model, friends_tokenizer에서  
friends_model의 용량이 1.34GB로 크기 때문에 깃허브에는 올리지 않음.

## 개발 로그
0819 채팅 jquery 추가  
0819 채팅 input에 대한 문법 교정 api 적용  
- 고칠 점 : output과 함께 출력됨. input과 동시에 출력이 되도록 바꿔야 함   

0820 js 이용해서 문법 교정 api 적용하는 방법 추가 (localhost:8000/api-ex)
- UI도 간단하게 구현
- 고칠 점 : getElementById 사용하여 여러개 교정 불가, 채팅 적용은 아직 안해봄  

**--여기서부터 작업하신다면 makemigrations와 migrate하신 후에 작업하셔야 합니다!--**  
0823 채팅 기록 남도록 수정(아래에 간단하게 설명 달아놨습니다!)  
https://www.notion.so/21-08-23-b90d7a56ee6440ed9d28cf5a992e6cc3  

0824 DialogRPT 도입 (시작하시기 전에 아래 노션을 꼭 확인해주세요!)  
https://www.notion.so/21-08-24-0070678a01484c26bd4567b1d33f8771  
