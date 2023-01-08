from importlib.machinery import FileFinder
from stat import FILE_ATTRIBUTE_OFFLINE
from venv import create
import requests
from bs4 import BeautifulSoup
from user_agent import UserAgent

# soup 생성
def create_soup(url, verify = True, parser = "html.parser"):
    user_agent = UserAgent().user_agent  # user_agent.py 파일의 유저에이전트 정보
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers = headers, verify = verify)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, parser)
    return soup


# 간호대학 학부 공지
def get_notices_from_yonsei_nursing():

    # 간호대학 학부 공지사항 URL
    url = "https://nursingcollege.yonsei.ac.kr/nursing/news/notice/academic.do"
    soup = create_soup(url, verify=False)

    # 상위 5개 공지 태그
    top_five_notices_tags = soup.find_all(attrs = {"class": "bbs-item"}, limit = 5)
    # 공지 제목
    top_five_notices_titles = [item.find(attrs = {"class": "subject"}).text for item in top_five_notices_tags]
    # 공지 날짜
    top_five_notices_time = [item.find(attrs = {"class": "info-area"}).text.strip() for item in top_five_notices_tags]
    # 공지 URL
    top_five_notices_urls = [url + item.a["href"] for item in top_five_notices_tags]
    # 상위 5개 공지 딕셔너리
    top_five_notices = {"titles": top_five_notices_titles, "time": top_five_notices_time, "urls": top_five_notices_urls}

    return top_five_notices

# 연세대 공지
def get_notices_from_yonsei():
    
    # 연세대 공지 URL
    url = "https://www.yonsei.ac.kr/sc/support/notice.jsp"
    soup = create_soup(url)
    notice_board = soup.find(attrs = {"class": "board_list"})

    # 상위 5개 공지 (날짜순)
    notices = notice_board.find_all("li")
    top_five_notices_tags = sorted(notices, key = lambda x : x.find_all(attrs = {"class": "tline"})[-1].text, reverse = True)[0:5]
    # 공지 제목
    top_five_notices_titles = [item.strong.text.replace("[공지]", "").replace("만료", "").strip() for item in top_five_notices_tags]
    # 신촌/국제 구분
    campus = [item.find(attrs = {"class": "title"}).text.split(' ')[0].strip() for item in top_five_notices_tags]
    # 공지 날짜
    top_five_notices_time = [item.find_all(attrs = {"class": "tline"})[-1].text for item in top_five_notices_tags]
    # 공지 url
    top_five_notices_urls = [url + item.a["href"] for item in top_five_notices_tags]
    # 상위 5개 공지 딕셔너리
    top_five_notices = {"titles": top_five_notices_titles, "campus": campus, "time": top_five_notices_time, "urls": top_five_notices_urls}

    return top_five_notices

# 창업지원단 공지
def get_notices_from_yonsei_venture():
    
    # 창업지원단 공지 url
    url = "https://venture.yonsei.ac.kr/notice"
    soup = create_soup(url)

    # 상위 5개 공지 (날짜순)
    notices = soup.find_all(attrs = {"class": "li_body"})
    top_five_notices_tags = sorted(notices, key = lambda x: x.find(attrs = {"class": "time"})["title"], reverse = True)[:5]
    # 공지 제목
    top_five_notices_titles = [item.find("a", attrs = {"class": "list_text_title"}).text.strip() for item in top_five_notices_tags]
    # 공지 날짜
    top_five_notices_time = [item.find(attrs = {"class": "time"})["title"] for item in top_five_notices_tags]
    # 공지 url
    top_five_notices_urls = [url.replace("/notice", "") + item.find("a", attrs = {"class": "list_text_title"})["href"] for item in top_five_notices_tags]
    # 상위 5개 공지 딕셔너리
    top_five_notices = {"titles": top_five_notices_titles, "time": top_five_notices_time, "urls": top_five_notices_urls}

    return top_five_notices

# 기숙사 공지
def get_notices_from_yonsei_dorm():

    # 생활관 url
    url = "https://dorm.yonsei.ac.kr/board/?id=notice"
    soup = create_soup(url)
    notice_board = soup.tbody

    # 상위 5개 공지
    top_five_notices_tags = notice_board.find_all("tr", attrs = {"class": "hide_when_mobile"}, limit = 5)
    # 공지 제목
    top_five_notices_titles = [item.a.text for item in top_five_notices_tags]
    # 기숙사 종류
    dorm_types = [item.find_all("td")[1].text for item in top_five_notices_tags]
    # 공지 날짜
    top_five_notices_time = [item.find_all("td")[3].text for item in top_five_notices_tags]
    # 공지 url
    top_five_notices_urls = ["https://dorm.yonsei.ac.kr" + item.a["href"] for item in top_five_notices_tags]
    # 상위 5개 공지 딕셔너리
    top_five_notices = {"titles": top_five_notices_titles, "dorm_types": dorm_types, "time": top_five_notices_time, "urls": top_five_notices_urls}

    return top_five_notices