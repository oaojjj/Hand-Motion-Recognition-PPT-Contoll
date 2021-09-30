# Hand-Motion-Recognition-PPT-Control
부경대학교 IT융합응용공학과 캡스톤 디자인 작품 - 손 동작 인식 ppt 제어<br>
capstone design - hand motion recognition ppt control)
## 프로젝트 소개
학교, 회사뿐 만 아니라 여러 분야에서 프레젠테이션은 적극적으로 활용되고 있다. 프레젠테이션할 때 대부분 리모컨을 사용하거나 직접 마우스를 통해 조작하는 경우가 대다수이다. 마우스를 통해 직접 조작을 한다면 프레젠테이션에서 중요한 몸짓에 있어서 제약이 생기고 리모컨을 사용한다면 휴대성과 배터리의 문제를 생각하지 않을 수 없다. 우리는 이러한 불편함을 해결하고자 동작 인식을 통한 프레젠테이션이라는 주제를 선정하게 되었다.
<br>
<br>
동작 인식은 소형 카메라가 사람의 손을 추적하고 손동작을 유추하여 딥러닝 모델을 학습 하는 것이고, 모델을 적용하여 발표자의 손동작을 실시간으로 분석 후 유추하여 프레젠테이션을 제어하는 프로그램을 개발을 목표로 한다.
<br>
<br>
손 동작 인식에는 딥러닝 LSTM 모델을 사용했습니다
## 기능
|손 동작(모션)|기능|
|------|---|
|우측에서 좌측으로 손바닥이 보이게 평행이동|ppt 뒤로 넘기기|
|좌축에서 우측으로 손바닥이 보이게 평행이동|ppt 앞으로 넘기기|
|주먹 쥐기 & 손바닥 하단에서 상단으로 평행이동|잠금 & 해제|
|‘따봉’ 동작에서 우측으로 손목꺾기|음량 높이기|
|‘따봉’ 동작에서 좌측으로 손목꺾기|음량 낮추기|
|랜드마크들의 좌표의 상대 위치를 활용|클릭|

## 시연영상
[강의실]<br>
https://drive.google.com/file/d/1VzOn_l9O_n91n4QIvF54lzZgzd-QHJ6v/view
<br>
<br>
[집]<br>
[![시연영상](https://img.youtube.com/vi/T6w6k1_jkFg/0.jpg)](https://youtu.be/T6w6k1_jkFg) 

## 팀 소개
펀쿨섹(Fun..Cool..Sexy) 팀
- 권오성(팀장)<br>
  IT융합응용공학과 201611990 4학년<br>
  모션 인식 및 학습 구현, pyqt5 gui 구현 및 연동<br>
  oxojjjj@gmail.com
  <br>
  <br>
  <br>
- 송상한(팀원)<br>
  IT융합응용공학과 201612021 3학년<br>
  데이터 수집, 보고서 작성, gui 연동<br>
  https://github.com/siiiido
  <br>
  <br>
  <br>
- 이학진(팀원)<br>
  IT융합응용공학과 201612037 4학년<br>
  모델, pyqt5 gui 구현 및 연동<br>
  https://github.com/LEEHAKJIN-VV
  <br>
  <br>
  <br>
- 임종윤(팀원)<br>
  IT융합응용공학과 201612038 4학년<br>
  데이터 수집, 보고서 작성, gui 연동<br>
  https://github.com/hijongyoon
