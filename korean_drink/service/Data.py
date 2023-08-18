class DataService:
    def __init__ (self):
        pass

    # 서비스에 데이터 보관하기
    def setData(self, object):
        self.object = object

    # 데이터 가져오기
    def getData(self):
        return self.object