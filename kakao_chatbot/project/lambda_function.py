import json
import main


def lambda_handler(event, context):

    try:
        request_body = json.loads(event['body'])
        params = request_body['action']['params']
        notice_type = params['noticetype']
    
        if notice_type == "간호대 공지":
            notices = main.get_notices_from_yonsei_nursing()
            notice_titles = notices["titles"]
            notice_time = notices["time"]
            notice_urls = notices["urls"]
            
            items = []
            for i in range(len(notice_titles)):
                item = {
                    "title": f"{notice_titles[i]}",
                    "description": f"{notice_time[i]}",
                    "link": {
                        "web": f"{notice_urls[i]}"
                    }
                }
                items.append(item)
            
        
            result = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "간호대학 상위 5개 공지입니다."
                                },
                                "items": items,
                                "buttons": [
                                    {
                                        "label": "더 보러 가기",
                                        "action": "webLink",
                                        "webLinkUrl": "https://nursingcollege.yonsei.ac.kr/nursing/news/notice/academic.do"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        
        elif notice_type == "연세대 공지":
            notices = main.get_notices_from_yonsei()
            notice_titles = notices["titles"]
            campus = notices["campus"]
            notice_time = notices["time"]
            notice_urls = notices["urls"]
            
            items = []
            for i in range(len(notice_titles)):
                item = {
                    "title": f"{notice_titles[i]}",
                    "description": f"{notice_time[i]} {campus[i]}",
                    "link": {
                        "web": f"{notice_urls[i]}"
                    }
                }
                items.append(item)
            
        
            result = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "연세대학교 상위 5개 공지입니다."
                                },
                                "items": items,
                                "buttons": [
                                    {
                                        "label": "더 보러 가기",
                                        "action": "webLink",
                                        "webLinkUrl": "https://www.yonsei.ac.kr/sc/support/notice.jsp"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
    
        elif notice_type == "기숙사 공지":
            notices = main.get_notices_from_yonsei_dorm()
            notice_titles = notices["titles"]
            dorm_types = notices["dorm_types"]
            notice_time = notices["time"]
            notice_urls = notices["urls"]
            
            items = []
            for i in range(len(notice_titles)):
                item = {
                    "title": f"{notice_titles[i]}",
                    "description": f"{notice_time[i]} {dorm_types[i]}",
                    "link": {
                        "web": f"{notice_urls[i]}"
                    }
                }
                items.append(item)
            
        
            result = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "연세대 기숙사 상위 5개 공지입니다."
                                },
                                "items": items,
                                "buttons": [
                                    {
                                        "label": "더 보러 가기",
                                        "action": "webLink",
                                        "webLinkUrl": "https://dorm.yonsei.ac.kr/board/?id=notice"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
    
        elif notice_type == "창업지원단 공지":
            notices = main.get_notices_from_yonsei_venture()
            notice_titles = notices["titles"]
            notice_time = notices["time"]
            notice_urls = notices["urls"]
            
            items = []
            for i in range(len(notice_titles)):
                item = {
                    "title": f"{notice_titles[i]}",
                    "description": f"{notice_time[i]}",
                    "link": {
                        "web": f"{notice_urls[i]}"
                    }
                }
                items.append(item)
            
        
            result = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "listCard": {
                                "header": {
                                    "title": "창업지원단 상위 5개 공지입니다."
                                },
                                "items": items,
                                "buttons": [
                                    {
                                        "label": "더 보러 가기",
                                        "action": "webLink",
                                        "webLinkUrl": "https://venture.yonsei.ac.kr/notice"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
    
    except:
        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "오류 발생. 관리자에게 문의하세요."
                        }
                    }    
                ]
            }
        }
    

    return {
        'statusCode':200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }