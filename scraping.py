from datetime import datetime, timedelta
from utils import *
from bs4 import BeautifulSoup
import re
import time

# fmkorea hotdeal
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
                                "error": f"{response.status_code}: Second response failed\n{response.content.decode('utf-8')}"
                            })
                            print(response.content.decode('utf-8'))
                            return ret
            if finish:
                return ret
            i += 1
        else:
            ret.append({
                "error": f"{response.status_code}: First response failed"
            })
            return ret

# coolenjoy jirum2
def scraping2():
    ret = []
    i = 1
    post_num = 1
    now = datetime.now()

    while True:
        finish = True
        response = get_requests(f'https://coolenjoy.net/bbs/jirum2/p{i}')
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.find('tbody').find_all('tr')
            for post in posts:
                td = post.find_all('td') # [분류(td_num), 제목(td_subject), 글쓴이(td_name_sv_use), 날짜(td_date), 조회, 추천(td_hit)]
                td_date = remove_tab(td[3].text)
                if td[0].text != '공지' and now.strftime("%y-%m-%d") == td_date:
                    finish = False
                    post_url = td[1].find('a')['href']

                    response = get_requests(post_url)
                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        title = soup.find('h1', {"id": "bo_v_title"})
                        title = title.text.strip()
                        content = ''
                        ps = soup.find('div', {"id": "bo_v_con"}).find_all('p')
                        for p in ps:
                            p = p.text
                            if p != '':
                                content += p
                                content += '\n'
                        related_url = soup.find('section', {"id": "bo_v_link"}).find('strong').text
                        ret.append({
                            "post_num": post_num,
                            "title": title,
                            "post_url": post_url,
                            "related_url": related_url,
                            "content": content
                        })
                        post_num += 1
                        time.sleep(0.5) # Delay
                    else:
                        ret.append({
                            "post_num": post_num,
                            "error": f':warning: 실행 중 문제가 발생했습니다.\n{response.status_code}: Second response failed'
                        })
                        return scraping2_2(now, ret)
            if finish:
                return scraping2_2(now, ret)
            i += 1
        else:
            ret.append({
                "post_num": post_num,
                "error": f':warning: 실행 중 문제가 발생했습니다.\n{response.status_code}: First response failed'
            })
            return scraping2_2(now, ret)
def scraping2_2(now, ret):
    jirum2_message = []
    message = f':star: {now.year}년 {now.month}월 {now.day}일 쿨엔조이 지름알뜰정보 이벤트 글 목록입니다.'
    for info in ret:
        message += f"\n\n===== {info['post_num']} =====\n"
        if 'error' in info:
            message += info['error']
            break
        else:
            ''' 아래 에러 발생 가능성이 있어 본문 글자수 제한
            discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
            In content: Must be 2000 or fewer in length.
            '''
            c = info["content"]
            if len(c) < 1500:
                message += f':person_tipping_hand: {info["title"]}\n\n{c}\n'
                message += f':link: {info["related_url"]}'
            else:
                message += f':person_tipping_hand: {info["title"]}\n\n'
                message += f':face_with_raised_eyebrow: 본문이 길이 제한을 초과하여 생략되었습니다. 아래 링크에서 직접 확인해보세요.\n\n'
                message += f':link: {info["post_url"]}'
        jirum2_message.append(message)
        message = ''
    return jirum2_message