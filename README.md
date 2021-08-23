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
