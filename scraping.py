from datetime import datetime, timedelta
from utils import *
from bs4 import BeautifulSoup
import re

def scraping():
    ret = []
    finish = False
    i = 1
    now = datetime.now()
    now += timedelta(hours=9)

    while True:
        response = get_requests(PROTOCOL_AND_DOMAIN + PATH, {'mid': 'hotdeal', 'page': i})
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.find_all('li', {"class":["li", "li_best2_pop0", "li_best2_hotdeal0"]})
            for post in posts:
                ''' 5분 이내로 작성된 글만 스크래핑 '''
                regdate = post.find('span', {"class":"regdate"})
                regdate = remove_tab(regdate.text)
                reg_hour = int(regdate[:2])
                reg_minute = int(regdate[3:5])
                if regdate[4] == '.': # 24시간 이상 지난 글이면
                    finish = True
                    break
                if now.minute == 0 and \
                not ((now.hour == 0 and (((reg_hour == 23) and (55 < reg_minute < 60)) or ((reg_hour == 0) and (reg_minute == 0)))) \
                or ((reg_hour == now.hour - 1) and (55 < reg_minute < 60)) \
                or ((reg_hour == now.hour) and (reg_minute == 0))): # 지금이 0분일 때
                    finish = True
                    break
                else: # 지금이 5~55분일 때
                    if not (now.hour == reg_hour and now.minute - 5 < reg_minute):
                        finish = True
                        break

                info = post.find_all('a', {"class":"strong"})
                price = info[1].text # 가격
                mall = info[0].text # 쇼핑몰
                delivery_fee = info[2].text # 배송비
                if price == '0원' or price == '공짜' or '무' in price or 'x' in price: # 가격이 0원이면
                    # 종료된 핫딜은 'hotdeal_var8Y' class이므로 해당 if문에서 필터링
                    if post.find('a', {"class":"hotdeal_var8"}): # If object is not NoneType
                        title = post.find('a', {"class":"hotdeal_var8"})
                        path_params = title['href']
                        title = title.text
                        title = re.sub(pattern = '\[[^\]]*\]', repl = '', string = title) # 댓글수 제거
                        title = remove_tab(title)
                        path_params = remove_tab(path_params)
                        
                        # 썸네일
                        thumb = post.find('img', {"class":"thumb"})
                        if thumb:
                            thumb = 'https:'+thumb['data-original']
                        else:
                            thumb = 'https://static.fmkorea.com/widgets/fmkorea_best/non-img.gif'
                        
                        # 카테고리
                        category = post.find('span', {"class":"category"}).find('a')
                        category = remove_tab(category.text)
                        
                        post_url = PROTOCOL_AND_DOMAIN + path_params # 핫딜 글 URL
                        response = requests.get(post_url)
                        if response.status_code == 200:
                            html = response.text
                            soup = BeautifulSoup(html, 'html.parser')
                            xe_contents = soup.find_all('div', {"class":'xe_content'})
                            related_url = xe_contents[0].find('a')['href'] # 관련 URL
                            content = xe_contents[5].text # 글 내용
                            ret.append({
                                "title": title,
                                "mall": mall,
                                "price": price,
                                "delivery_fee": delivery_fee,
                                "category": category,
                                "thumb": thumb,
                                "post_url": post_url,
                                "related_url": related_url,
                                "content": content
                            })
                        else:
                            ret.append({
                                "error": "Second response failed"
                            })
                            return ret
            if finish:
                return ret
            i += 1
        else:
            ret.append({
                "error": "First response failed"
            })
            return ret