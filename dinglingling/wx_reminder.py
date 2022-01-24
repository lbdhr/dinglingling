import datetime
import traceback
import functools
import socket
import os
import requests
import json

DATE_FORMAT = "%Y-%m-%d %H:%M:%d"

def send_message_QiYeVX(json_data, useridlist, agentID, corpID, corpSecret): # 默认发送给自己
    useridstr = "|".join(useridlist)
    agentid = agentID

    corpid = corpID
    corpsecret = corpSecret
    response = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    data = json.loads(response.text)
    access_token = data['access_token']

    json_dict = {
       "touser" : useridstr,
       "msgtype" : "text",
       "agentid" : agentid,
       "text" : {
           "content" : json.dumps(json_data)
       },
       "safe": 0,
       "enable_id_trans": 0,
       "enable_duplicate_check": 0,
       "duplicate_check_interval": 1800
    }
    json_str = json.dumps(json_dict)
    response_send = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
    return json.loads(response_send.text)['errmsg'] == 'ok'




def wx_reminder(userIdList, agentId, corpId, corpSecret, proxy: str="", remind_started: bool=True):
    """[summary]
    
    Arguments:
        SCKEY {[str]} -- [the sckey you get from http://sc.ftqq.com/3.version]
    
    Keyword Arguments:
        proxy {str} -- [if you use the proxy] (default: {""})
        reminder_start {bool} -- [if you want remind you when the function start] (default: {False})
    
    Raises:
        ex: [description]
    
    Returns:
        [type] -- [description]
    """

    if len(proxy) != 0:
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy

    def decorator_sender(func):
        @functools.wraps(func)
        def wrapper_sender(*args, **kwargs):

            start_time = datetime.datetime.now()
            host_name = socket.gethostname()
            func_name = func.__name__

            title = "Your_training_has_started."
            contents = [
                        'Machine name: %s' % host_name,
                        'Main call: %s' % func_name,
                        'Starting date: %s' % start_time.strftime(DATE_FORMAT)]
            content = '\n\n'.join(contents)
            
            data = {
                "text":title,
                "desp":content
            }

            # url = f"https://sc.ftqq.com/{SCKEY}.send"

            if remind_started:
                # requests.post(url, data)
                print(send_message_QiYeVX(data, userIdList, agentId, corpId, corpSecret))

            try:
                value = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time

                title = "Your_training_is_complete."
                contents = [
                            'Machine name: %s' % host_name,
                            'Main call: %s' % func_name,
                            'Starting date: %s' % start_time.strftime(DATE_FORMAT),
                            'End date: %s' % end_time.strftime(DATE_FORMAT),
                            'Training duration: %s' % str(elapsed_time)]
                content = '\n\n'.join(contents)

                data = {
                    "text":title,
                    "desp":content
                }

                # requests.post(url, data)
                print(send_message_QiYeVX(data, userIdList, agentId, corpId, corpSecret))

                return value

            except Exception as ex:
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time

                title = "Your_training_has_crashed."
                contents = [
                            'Machine name: %s' % host_name,
                            'Main call: %s' % func_name,
                            'Starting date: %s' % start_time.strftime(DATE_FORMAT),
                            'Crash date: %s' % end_time.strftime(DATE_FORMAT),
                            'Crashed training duration: %s\n\n' % str(elapsed_time),
                            "Here's the error:",
                            '%s\n\n' % ex,
                            "Traceback:",
                            '%s' % traceback.format_exc()]
                content = '\n\n'.join(contents)

                data = {
                    "text":title,
                    "desp":content
                }

                # requests.post(url, data)
                print(send_message_QiYeVX(data, userIdList, agentId, corpId, corpSecret))
                
                raise ex

        return wrapper_sender

    return decorator_sender