import requests
from bs4 import BeautifulSoup
import telegram
import os


# soup 생성 함수
def create_soup(url, verify = True, parser = "html.parser"):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers = headers, verify = verify)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, parser)
    return soup

# 텔레그램으로 공지하기 함수
def notice_through_telegram(notice_titles, notice_times, notice_urls, category = False):
    if len(notice_titles) == 0:
        pass
    else:
        my_token = #'토큰'
        my_chat_id = #'아이디'
        bot = telegram.Bot(token=my_token)

        if category == False:
            for i in range(len(notice_titles)):
                bot.send_message(chat_id = my_chat_id, text = f"[{notice_titles[i]}]({notice_urls[i]})\n({notice_times[i]})", parse_mode = "Markdown", disable_web_page_preview = True)
        else:
            for i in range(len(notice_titles)):
                bot.send_message(chat_id = my_chat_id, text = f"[{notice_titles[i]}]({notice_urls[i]})\n({category[i]})\n({notice_times[i]})", parse_mode = "Markdown", disable_web_page_preview = True)

# 에러 메시지
def error_message():
    my_token = #'토큰'
    my_chat_id = #'아이디'
    bot = telegram.Bot(token=my_token)
    bot.send_message(chat_id = my_chat_id, text = "봇 오류 발생")

# DB 업데이트 함수     
def update_DB(latest_from_db, latest_from_page, db_path):
    if latest_from_db[0].strip() == latest_from_page[0]:
        pass
    else:
        with open(db_path, 'w', encoding = 'utf-8') as f:
            for num in latest_from_page:
                f.write(f"{num}\n")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


#######################################간호대 공지######################################################

# db에 기록된 게시물 번호
db_path = os.path.join(BASE_DIR, "DB", "latest.txt")
with open(db_path, 'r', encoding = 'utf-8') as f:
    latest_from_db = f.readlines()

try:
    # 공지
    url = "https://nursingcollege.yonsei.ac.kr/nursing/news/notice/academic.do"
    soup = create_soup(url, verify = False)
    notice_titles = []
    notice_times = []
    notice_urls = []
    notice = soup.find(attrs = {"class": "bbs-item"})
    while True:
        # URL 상의 article 번호
        article_num = notice.a["href"].split("&")[1].replace("articleNo=", "")
        # article 번호가 db 상의 번호와 같을 경우
        if article_num == latest_from_db[0].strip():
            break
        elif article_num == latest_from_db[1].strip():
            break
        elif article_num == latest_from_db[2].strip():
            break
        elif article_num == latest_from_db[3].strip():
            break
        elif article_num == latest_from_db[4].strip():
            break                        
        # 다를 경우
        else:
            notice_titles.append(notice.find(attrs = {"class": "subject"}).text)
            notice_times.append(notice.find(attrs = {"class": "info-area"}).text.strip())
            notice_urls.append(url + notice.a["href"])
            notice = notice.find_next_sibling("div")

    # 챗봇으로 공지 알림
    notice_through_telegram(notice_titles, notice_times, notice_urls)

    # DB 업데이트
    latest_from_page = []
    five_notices = soup.find_all(attrs = {"class": "bbs-item"}, limit = 5)
    for notice in five_notices:
        article_num = notice.a["href"].split("&")[1].replace("articleNo=", "")
        latest_from_page.append(article_num)
    update_DB(latest_from_db, latest_from_page, db_path)

except:
    error_message()


#######################################################################################