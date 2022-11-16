# photoshop

실행을 위해 필요 사항
  python                    3.9.13
  numpy                     1.23.4
  opencv-python             4.6.0.66
  pip                       22.2.2
  pyside6                   6.4.0

 

## 메뉴바 기능
### 파일
+ 나가기 

  실행한 프로그램을 닫는 기능. 특징으로는 예제코드에서 수정을 거의 안함

+ 수정된 이미지 저장

  타 기능들로 원본 사진에 효과를 적용시킨 사진(toolbar를 기준으로 오른쪽에 출력되는 이미지)을 현재 위치에 'new_image_file'이란 이름으로 저장하는 기능.
  + filter 추가 -> .jpeg, .jpg 파일의 형식만 받아들일 수 있게 만듦.

### 임계영역/경계검출
+ 임계영역
  + Otsu
    
    오츠 알고리즘을 통해 threshold한 이미지를 grascale로 출력하는 기능

  + 적응형 스레시홀드
  
    옵션으로 평균값과 가우시안 분포를 적용한 결과를 각각 'Adepted Mean', 'Adepted Gaussian'을 통해 출력할 수 있다.

+ 경계검출
  + Roverts Corss Filter
  
    로버츠 크로스 필터를 통한 경계검출을 한 이미지를 출력
  
  + Sobel Filter
  
    소벨필터를 적용한 이미지를 출력

### 회전

  원본 이미지를 90도 간격으로 회전시킨 이미지를 출력한다. cv2.rotate()함수를 사용해, cv2.ROTATE_90_COLCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE 옵션으로 구햔했다.
  
### 반전

  cv2.filp()을 통해 구현되었다. 원본 이미지에서 x축, y축, 원점 대칭한 이미지를 출력한다.
  
### 보정
색상값을 다듬는 노멀라이즈, 이퀄라이즈(흑백/컬러)와 함께 여러 블러효과들을 구현했다.
+ blur effects
  
  cv2.blur()로 구현한 일반 블러를 비롯한 가우시안, 미디언 블러와 바이레이널 필터 실행시, 가운데의 toolbar에서
  '블러 커널 크기'의 spinbox와 '블러 적용' 버튼이 활성화된다. 기본적으로 블러효과를 적용하면, 블러커널크기가 3으로 효과를 적용하고, spinbox의 값을 수정하면 커널크기를
  spinbox의 값으로 적용한 블러가 적용된다. '블러 적용' 버튼을 누르면 블러 커널 spinbox를 비활성화한다.

## 툴바 기능

툴바는 원본 이미지를 출력하는 img_label1과 효과를 적용한 이미지를 출력하는 img_label2의 중간에 배치되어있다.
 버튼을 통해 기능들을 실행하고, 실행한 기능에 따라 활성화되는 spinbox들의 수치를 조정하여 적용되는 효과를 원하는대로 적용할 수 있다.
 
 ### '이미지 열기' 버튼
 
  효과를 적용할 원본 이미지를 불러온다. 
  대부분의 기능을 실행하기 위해 선행적으로 실행되어야 한다.

### '흑백' 버튼

  이미지를 grayscale로 변환하여 출력한다.
  
### '확대/축소' 버튼

  실행시 '확대 배율' spinbox가 활성화된다. cv2.resize()함수를 통해 구현되었으며, 0.1배 ~ 3.0배까지 원본 이미지의 크기를 수정할 수 있다.
   한번더 누르면 활성화된 spinbox가 비활성화된다.
   
### 알파 블랜드

  또 다른 사진을 불러와 알파블랜드를 수행한다. 실행시 '블랜드 알파값' spinbox가 활성화되고 이를 통해 알파값을 조정할 수 있다. 한번 더 누르면 이 기능으로 활성화된 spinbox가 다시 비활성화된다.
  + filter 추가 -> .jpeg, .jpg 파일의 형식만 받아들일 수 있게 만듦.
  + cat.jpg, cat(2).jpg 추가로 해당 폴더 내에서 파일들을 불러올 수 있게 함
  
### '모시깽' 버튼

  모시깽이한 기능을 위해 언젠간 달아놓아야겠다고 생각하고 만들었다가 지우는 걸 깜빡한 버튼이다. 아무런 효과를 연결해두지 않은 '장식버튼'이다. 
  
### '새로고침'

  효과가 적용된 이미지를 출력하는 img_label2에서 출력하고 있는 img를 지운다. 수정된 이미지를 저장하고 있던 self.img2의 내용도 비운다.
