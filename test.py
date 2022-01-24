from dinglingling import wx_reminder

userIdList = [] 
agentId = ""
corpId = ""
corpSecret = ""
proxy = "" # if you needn't proxy, ignore it.

@wx_reminder(userIdList=userIdList, agentId=agentId, corpId=corpId, corpSecret=corpSecret, proxy=proxy, remind_started=True)
def test_correct_func():
    print("hello world")

@wx_reminder(userIdList=userIdList, agentId=agentId, corpId=corpId, corpSecret=corpSecret, proxy=proxy, remind_started=True)
def test_error():
    raise Exception("test error")


if __name__ == "__main__":
    test_correct_func()
    # test_error()
    pass