from Bot import MyBot
from DB import MyDB
from customFunctions import create_soup

bot_token = "봇 토큰"
channel_ID = "채널 ID"
warning_ID = "오류 알림용 ID"

bot_nursing = MyBot(bot_token)

try:
    url = "https://nursingcollege.yonsei.ac.kr/nursing/news/notice/academic.do"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    
    soup_nursing = create_soup(url, user_agent, verify=False)
    notice_nursing = soup_nursing.find(attrs = {"class": "bbs-item"})
    
    db_nursing = MyDB("db_nursing.txt")
    latest_from_db_nursing = db_nursing.getLatestNotices()
    
    while True:
        # URL 상의 article 번호
        article_num = notice_nursing.a["href"].split("&")[1].replace("articleNo=", "")
        # article 번호가 db 상의 번호와 같을 경우
        if article_num == latest_from_db_nursing[0].strip():
            break
        elif article_num == latest_from_db_nursing[1].strip():
            break
        elif article_num == latest_from_db_nursing[2].strip():
            break
        elif article_num == latest_from_db_nursing[3].strip():
            break
        elif article_num == latest_from_db_nursing[4].strip():
            break                        
        # 다를 경우
        else:
            bot_nursing.notice_titles.append(notice_nursing.find(attrs = {"class": "subject"}).text)
            bot_nursing.notice_times.append(notice_nursing.find(attrs = {"class": "info-area"}).text.strip())
            bot_nursing.notice_urls.append(url + notice_nursing.a["href"])
            notice_nursing = notice_nursing.find_next_sibling("div")
    
    # 챗봇으로 공지 알림
    bot_nursing.notice_through_telegram(channel_ID)
    
    # DB 업데이트
    latest_from_page = []
    five_notices = soup_nursing.find_all(attrs = {"class": "bbs-item"}, limit = 5)
    for notice in five_notices:
        article_num = notice.a["href"].split("&")[1].replace("articleNo=", "")
        latest_from_page.append(article_num)
    db_nursing.update_DB(latest_from_page)

except:
    bot_nursing.error_message(warning_ID)