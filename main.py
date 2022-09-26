from bs4 import BeautifulSoup
from utils import *
from const import *
# import time

'''
Run
'''
print('어느 날짜 이후까지 검색할지 입력해주세요.\n입력 예시: 2022.09.11') # 스크롤바로 검색 기간 설정할 수 있도록 수정할 예정
date = input()

i = 1
finish = False
while True:
    # begin = time.time()
    response = random_proxy(PROTOCOL_AND_DOMAIN + PATH, {'mid': 'hotdeal', 'page': i})
    # end = time.time()
    # result = end - begin
    # result = round(result, 3)
    # print("time taken to execute random_proxy(): ", result)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('li', {"class":["li", "li_best2_pop0", "li_best2_hotdeal0"]})
        for post in posts:
            regdate = post.find('span', {"class":"regdate"})
            regdate = remove_tab(regdate.text)
            if regdate == date:
                print('검색이 완료되었습니다.')
                finish = True
                break
            info = post.find_all('a', {"class":"strong"})
            if info[1].text == '0원' \
            or info[1].text == '공짜' \
            or '무' in info[1].text \
            or 'x' in info[1].text: # 가격이 0원이면
                # 종료된 핫딜은 'hotdeal_var8Y' class이므로 해당 if문에서 필터링
                if post.find('a', {"class":"hotdeal_var8"}): # If object is not NoneType
                    title = post.find('a', {"class":"hotdeal_var8"})
                    path_params = title['href']
                    title = remove_tab(title.text)
                    path_params = remove_tab(path_params)
                    # 웹 화면에 출력되도록 수정할 예정
                    print(title)
                    print(PROTOCOL_AND_DOMAIN + path_params)
        if finish:
            break
        i += 1
    else:
        print('status code is not 200, retry')