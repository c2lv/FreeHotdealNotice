#  무료 핫딜 공지 프로그램(FreeHotdealNotice)
[펨코 핫딜 게시판](https://www.fmkorea.com/hotdeal)에서 특정 기간 등록된 글 중 가격이 무료인 상품을 소개하는 글만 모아 출력해주는 프로그램  
추후 개선하여 알림 서비스로 개편할 예정

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
  - Library: bs4, requests
- OS
  - Windows 10 64bit