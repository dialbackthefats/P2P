import app


class approveAPI():
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.ger_approve_url = app.BASE_URL + '/member/member/getapprove'

    def approve(self, session, realname, cardId):
        data = {"realname": realname,"card_id": cardId}
        response = session.post(self.approve_url, data=data, files={'x': 'y'})   # multi-part多消息体数据，传递参数的方法
        return response

    def get_approve(self, session):
        response = session.post(self.ger_approve_url)
        return response
