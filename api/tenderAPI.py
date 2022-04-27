import app


class tenderAPI():
    def __init__(self):
        self.get_loaninfo_url = app.BASE_URL + '/common/loan/loaninfo'
        self.tender_url = app.BASE_URL + '/trust/trust/tender'
        self.get_mytender_list = app.BASE_URL + '/loan/tender/mytenderlist'

    def get_loaninfo(self, session, tender_id):
        data ={"id": tender_id}
        response = session.post(self.get_loaninfo_url,data=data)
        return response

    def tender(self, session, tenderid, amount):
        url = self.tender_url
        data = {"id": tenderid,
                "depositCertificate": "-1",
                "amount": amount}
        response = session.post(url,data=data)
        return response

    def mytender_list(self, session, status):
        url = self.get_mytender_list
        data = {"status": status}
        response = session.post(url, data=data)
        return response



