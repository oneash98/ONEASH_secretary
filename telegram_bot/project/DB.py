import os

class MyDB:
    def __init__(self, dbFileName):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        DB_DIR = os.path.join(BASE_DIR, "DB")
        self.db_path = os.path.join(DB_DIR, dbFileName)

    
    # db에서 이전 공지 정보 가져오기
    def getLatestNotices(self):
        with open(self.db_path, 'r', encoding='utf-8') as f:
            latest_notices = f.readlines()
        return latest_notices

    # db 업데이트 함수
    def update_DB(self, data2update):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            for data in data2update:
                f.write(f"{data}\n")