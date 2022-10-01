#  무료 핫딜 공지 프로그램(FreeHotdealNotice)
[펨코 핫딜 게시판](https://www.fmkorea.com/hotdeal)에서 특정 기간 등록된 글 중 가격이 무료인 상품을 소개하는 글만 모아 전달해드립니다.  
[쿨엔조이 지름알뜰정보 이벤트 게시판](https://coolenjoy.net/bbs/jirum2)에서 매일 업로드된 글을 모아, 이벤트에 바로 참여하기 쉬운 형태의 메시지로 만들어 보내드립니다.  
현재 디스코드 메시지 알림 서비스 제공중이며, 추후 카카오톡 채널 알림 서비스로도 제공 예정입니다.  
[디스코드 채널 바로가기](https://discord.gg/Frr7mxvV85)

---
## Usage
1. Clone this repository.
```git bash
git clone https://github.com/c2lv/FreeHotdealNotice.git
```
2. Change directory and activate virtualenv.
```git bash
cd FreeHotdealNotice
pip install virtualenv
virtualenv venv
source venv/Scripts/activate
```
3. Add `CH_FREEHOTDEAL_FMKOREA_ID` and `TOKEN` value in `const.py`.
4. Install the requirements.
```git bash
pip install -r requirements.txt
```
5. Run `main.py`.
```git bash
python main.py
```
---
## Environment
- Python
  - Version: 3.10.0
  - Library: bs4, requests, aiocron, discord
- OS
  - Windows 10 64bit