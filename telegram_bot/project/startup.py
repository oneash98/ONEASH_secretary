from Bot import MyBot
from DB import MyDB
from customFunctions import *
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

bot_token = "봇토큰"
channel_ID = "채널 id"
warning_ID = "오류 알림용 id"

bot_startup = MyBot(bot_token)

db_yonseiVenture_top = MyDB("db_yonseiVenture_top.txt") # 연세대 창업지원단 상단 
db_yonseiVenture_normal = MyDB("db_yonseiVenture_normal.txt") # 연세대 창업지원단 일반
db_kstartup = MyDB("db_kstartup.txt") # k-startup
db_ccei = MyDB("db_ccei.txt") # 서울창조경제혁신센터
db_sba = MyDB("db_sba.txt") # sba 서울산업진흥원

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"


################## 연세대 창업지원단 #################
try:
    url_yonseiVenture = "https://venture.yonsei.ac.kr/notice"
    soup_yonseiVenture = create_soup(url_yonseiVenture, user_agent)

    ### 상단 고정 공지 ###
    notice_yonseiVenture_top = soup_yonseiVenture.find_all(attrs = {"class": "notice_body"})
    latest_from_db_yonseiVenture_top = db_yonseiVenture_top.getLatestNotices()

    for notice in notice_yonseiVenture_top:
        # 게시글 id
        notice_id = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")

        # 게시글 id가 db 상의 번호와 같을 경우
        if notice_id in [num.strip() for num in latest_from_db_yonseiVenture_top]:
            break                   
        # 다를 경우
        else:
            bot_startup.notice_titles.append(notice.find(attrs = {"class": "list_text_title"}).text.strip())
            bot_startup.notice_times.append(notice.find(attrs = {"class": "time"}).text.strip())
            bot_startup.notice_urls.append(url_yonseiVenture.replace("/notice", "") + notice.find(attrs={"class": "list_text_title"})["href"])

    # DB 업데이트
    five_from_yonseiVenture_top = []
    five_notices_yonseiVenture_top = notice_yonseiVenture_top[:5]
    for notice in five_notices_yonseiVenture_top:
        notice_id = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")
        five_from_yonseiVenture_top.append(notice_id)
    db_yonseiVenture_top.update_DB(five_from_yonseiVenture_top)


    ### 일반 공지 ###
    notice_yonseiVenture_normal = soup_yonseiVenture.find_all(lambda attrs: attrs.get("class", []) == ["li_body", "holder"])
    latest_from_db_yonseiVenture_normal = db_yonseiVenture_normal.getLatestNotices()

    for notice in notice_yonseiVenture_normal:
        # 게시글 id
        notice_id = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")

        # 게시글 id가 db 상의 번호와 같을 경우
        if notice_id in [num.strip() for num in latest_from_db_yonseiVenture_normal]:
            break                   
        # 다를 경우
        else:
            bot_startup.notice_titles.append(notice.find(attrs = {"class": "list_text_title"}).text.strip())
            bot_startup.notice_times.append(notice.find(attrs = {"class": "time"}).text.strip())
            bot_startup.notice_urls.append(url_yonseiVenture.replace("/notice", "") + notice.find(attrs={"class": "list_text_title"})["href"])

    # DB 업데이트
    five_from_yonseiVenture_normal = []
    five_notices_yonseiVenture_normal = notice_yonseiVenture_normal[:5]
    for notice in five_notices_yonseiVenture_normal:
        notice_id = notice.find(attrs={"class": "list_text_title"})["href"].split("&")[2].replace("idx=", "")
        five_from_yonseiVenture_normal.append(notice_id)
    db_yonseiVenture_normal.update_DB(five_from_yonseiVenture_normal)

except Exception as e:
    bot_startup.error_message(warning_ID, f"연세대 창업지원단 오류\n{e}")


#################### K-Startup ##########################

try: 
    url_kstartup = "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do"
    soup_kstartup = create_soup_selenium(url_kstartup, user_agent, wait_for=(By.CLASS_NAME, "notice"))

    notice_kstartup = soup_kstartup.find_all(attrs= {"class": "notice"})
    latest_from_db_kstartup = db_kstartup.getLatestNotices()

    for notice in notice_kstartup:
        # 게시글 id
        notice_id = notice.a["href"].replace("javascript:go_view(", "").replace(");", "")

        # 게시글 id가 db 상의 번호와 같을 경우
        if notice_id in [num.strip() for num in latest_from_db_kstartup]:
            break                   
        # 다를 경우
        else:
            bot_startup.notice_titles.append(notice.a.p.text.strip())
            bot_startup.notice_times.append(notice.find(attrs = {"class": "bottom"}).find_all("span")[2].text.strip().split(" ")[-1])
            bot_startup.notice_urls.append(f"https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=view&pbancSn={notice_id}&page=1&schStr=regist&pbancEndYn=N")

    # DB 업데이트
    five_from_kstartup = []
    five_notices_kstartup = notice_kstartup[:5]
    for notice in five_notices_kstartup:
        notice_id = notice.a["href"].replace("javascript:go_view(", "").replace(");", "")
        five_from_kstartup.append(notice_id)
    db_kstartup.update_DB(five_from_kstartup)

except Exception as e:
    bot_startup.error_message(warning_ID, f"k-startup 오류\n{e}")      



##################### 서울창조경제혁신센터 #######################
try:
    url_ccei = "https://ccei.creativekorea.or.kr/seoul/custom/notice_list.do?&sPtime=my&page=1"
    soup_ccei = create_soup_selenium(url_ccei, user_agent)

    notice_ccei = soup_ccei.find(attrs={"id": "list_body"}).find_all("tr")
    latest_from_db_ccei = db_ccei.getLatestNotices()

    for notice in notice_ccei:
        # 상단 고정 제외
        if notice.has_attr("class"):
            pass
        else:
            # 게시글 id
            notice_id = notice.a["onclick"].replace("fnDetailPage(", "").replace(")", "").split(",")[0]
            #번호 같을 경우
            if notice_id in [num.strip() for num in latest_from_db_ccei]:
                break
            #번호 다를 경우
            else:
                bot_startup.notice_titles.append(notice.a.text.strip())
                bot_startup.notice_times.append(notice.find_all("td")[4].text.strip())
                bot_startup.notice_urls.append(f"https://ccei.creativekorea.or.kr/seoul/custom/notice_view.do?no={notice_id}")

    # DB 업데이트
    id_from_ccei = []
    for notice in notice_ccei:
        if notice.has_attr("class"):
            pass
        else:
            notice_id = notice.a["onclick"].replace("fnDetailPage(", "").replace(")", "").split(",")[0]
            id_from_ccei.append(notice_id)
    db_ccei.update_DB(id_from_ccei)

except Exception as e:
    bot_startup.error_message(warning_ID, f"ccei 오류\n{e}")  


######################## SBA ###########################
try:
    url_sba = "https://www.sba.seoul.kr/"
    browser_options = webdriver.ChromeOptions()
    browser_options.headless = True
    browser_options.add_argument("window-size=1080,720")
    browser_options.add_argument(f"user-agent = {user_agent}")
    browser_options.add_argument("no-sandbox")
    browser_options.add_argument("disable-dev-shm-usage")
    browser_sba = webdriver.Chrome("./chromedriver", options = browser_options)
    browser_sba.get(url_sba)

    browser_sba.find_element(By.LINK_TEXT, "기업지원").click()
    browser_sba.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_MainContents_P_ORDER"]/option[2]').click()
    browser_sba.find_element(By.ID, "btn_search").click()
    time.sleep(2)

    soup_sba = BeautifulSoup(browser_sba.page_source, "html.parser")

finally:
    browser_sba.quit()

try:  
    notice_sba = soup_sba.find_all(attrs= {"class": "card_box"})
    latest_from_db_sba = db_sba.getLatestNotices()

    for notice in notice_sba:
        # 태그 확인 (SBA, 자금, 입주공간, 창업, 기타만 확인)
        if notice.find(attrs = {"class": "label gray"}).text not in ["SBA", "자금", "입주공간", "창업", "기타"]:
            pass
        else:
            # 게시글 id
            notice_id = notice.a["href"].replace("javascript:contentsDetail('", "").replace("')", "")
            # 게시글 id와 db 상의 번호 같을 경우
            if notice_id in [num.strip() for num in latest_from_db_sba]:
                break
            # 다를 경우
            else:
                bot_startup.notice_titles.append(notice.a.text.strip())
                bot_startup.notice_times.append(notice.find(attrs = {"class": "date"}).text.split("~")[0])
                bot_startup.notice_urls.append(f"https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support_Detail.aspx?RID={notice_id}")

    # DB 업데이트
    five_from_sba = []
    five_notices_sba = notice_sba[:5]
    for notice in five_notices_sba:
        notice_id = notice.a["href"].replace("javascript:contentsDetail('", "").replace("')", "")
        five_from_sba.append(notice_id)
    db_sba.update_DB(five_from_sba)

except Exception as e:
    bot_startup.error_message(warning_ID, f"sba 오류\n{e}")  



####################### 챗봇으로 공지 알림 ############################
bot_startup.notice_through_telegram(channel_ID)