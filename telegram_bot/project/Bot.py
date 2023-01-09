import telegram

class MyBot:
    def __init__(self, bot_token):
        self.bot = telegram.Bot(bot_token)
        self.notice_titles = []
        self.notice_times = []
        self.notice_urls = []

    # 텔레그램으로 공지하기 함수
    def notice_through_telegram(self, chat_id):
        if len(self.notice_titles) == 0:
            pass
        else:
            for i in range(len(self.notice_titles)):
                self.bot.send_message(chat_id = chat_id, text = f"[{self.notice_titles[i]}]({self.notice_urls[i]})\n({self.notice_times[i]})", parse_mode = "Markdown", disable_web_page_preview = True)

    # 에러 메시지
    def error_message(self, chat_id):
        self.bot.send_message(chat_id = chat_id, text = "봇 오류 발생")