from Bot import MyBot
from DB import MyDB
from customFunctions import create_soup

bot_token = "봇토큰"
channel_ID = "채널 id"
warning_ID = "오류 알림용 id"

bot_startup = MyBot(bot_token)

db_yonseiVenture_top = MyDB("db_yonseiVenture_top.txt") # 연세대 창업지원단 상단 
db_yonseiVenture_normal = MyDB("db_yonseiVenture_normal.txt") # 연세대 창업지원단 일반


################## 연세대 창업지원단 #################
try:
    url = "https://venture.yonsei.ac.kr/notice"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    soup_yonseiVenture = create_soup(url, user_agent)

    ### 상단 고정 공지 ###
    notice_yonseiVenture_top = soup_yonseiVenture.find_all(attrs = {"class": "notice_body"})
    latest_from_db_yonseiVenture_top = db_yonseiVenture_top.getLatestNotices()

    for notice in notice_yonseiVenture_top:
        # URL 상의 article 번호
        article_num = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")

        # article 번호가 db 상의 번호와 같을 경우
        if article_num in [num.strip() for num in latest_from_db_yonseiVenture_top]:
            break                   
        # 다를 경우
        else:
            bot_startup.notice_titles.append(notice.find(attrs = {"class": "list_text_title"}).text.strip())
            bot_startup.notice_times.append(notice.find(attrs = {"class": "time"}).text.strip())
            bot_startup.notice_urls.append(url.replace("/notice", "") + notice.find(attrs={"class": "list_text_title"})["href"])

    # DB 업데이트
    five_from_yonseiVenture_top = []
    five_notices_yonseiVenture_top = notice_yonseiVenture_top[:5]
    for notice in five_notices_yonseiVenture_top:
        article_num = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")
        five_from_yonseiVenture_top.append(article_num)
    db_yonseiVenture_top.update_DB(five_from_yonseiVenture_top)


    ### 일반 공지 ###
    notice_yonseiVenture_normal = soup_yonseiVenture.find_all(lambda attrs: attrs.get("class", []) == ["li_body", "holder"])
    latest_from_db_yonseiVenture_normal = db_yonseiVenture_normal.getLatestNotices()

    for notice in notice_yonseiVenture_normal:
        # URL 상의 article 번호
        article_num = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")

        # article 번호가 db 상의 번호와 같을 경우
        if article_num in [num.strip() for num in latest_from_db_yonseiVenture_normal]:
            break                   
        # 다를 경우
        else:
            bot_startup.notice_titles.append(notice.find(attrs = {"class": "list_text_title"}).text.strip())
            bot_startup.notice_times.append(notice.find(attrs = {"class": "time"}).text.strip())
            bot_startup.notice_urls.append(url.replace("/notice", "") + notice.find(attrs={"class": "list_text_title"})["href"])

    # DB 업데이트
    five_from_yonseiVenture_normal = []
    five_notices_yonseiVenture_normal = notice_yonseiVenture_normal[:5]
    for notice in five_notices_yonseiVenture_normal:
        article_num = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")
        five_from_yonseiVenture_normal.append(article_num)
    db_yonseiVenture_normal.update_DB(five_from_yonseiVenture_normal)

except:
    bot_startup.error_message(warning_ID)



####################### 챗봇으로 공지 알림 ############################
bot_startup.notice_through_telegram(channel_ID)