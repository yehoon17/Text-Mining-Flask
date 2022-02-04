# Text-Mining-Flask
Text mining project with flask

## 프로젝트 개요
Text-Mining 프로젝트를 Flask로 웹 구현

## 실행 방법
`python main.py` 실행

### 웹
`http://127.0.0.1:5000/` 에 접속

`http://127.0.0.1:5000/update` 에서 json 파일 업로드

`http://127.0.0.1:5000/documents` 에서 업로드한 파일 확인

 -> 제목 클릭 시, 문서 내용으로 이동

 -> 문서의 단어들의 TFIDF 확인 

`http://127.0.0.1:5000/df` 에서 단어별 document frequency 확인

### RESTful API
`python api_test.py` 실행
