# -*- coding: utf-8 -*-
import json,datetime,time
from ws4py.client.threadedclient import WebSocketClient

wx_map={}

menu_content=r'''指令操作指南\n输入(?) 显示帮助菜单\n输入(A) 显示相关支撑系统运行状况\n输入(B) 天山运营信息(http://10.76.134.138:30000)\n输入(C) DevOps运营信息'''
zc_content=r'''网管支撑系统共计38个，目前正常运行38个，问题系统0个'''
ts_content=r'''天山平台目前共计注册用户5228人，日均活跃用户25人次\n资源：主机135台，交换设备5台，虚拟机135台\n工具：有数报表 54人；游龙（CI/CD） 23人；莫问 12人；舍神 45人\n应用：共计156个，其中省公司13个，地市公司143个 '''
do_content=r'''DevOps目前纳管3个生产系统\n无线网子中心 每周迭代34次 部署频率12次 部署时长10秒 需求平均交付时长5天\n家宽平台 每周迭代21次 部署频率6次 部署时长8秒 需求平均交付时长6天\n天山平台 每周迭代43次 部署频率8次 部署时长5秒 需求平均交付时长3天'''

def getid():
    id = time.time()*1000
    return str(int(id))

def debug_switch():
    j='{"id":'+"\""+getid()+"\""+',"type":6000,"content":"on","wxid":"ROOT"}'
    return json.dumps(json.loads(j))

class CG_Client(WebSocketClient):
    def open(self):
        self.send(debug_switch())
        """ req = '{}'
        self.send(req) """

    def closed(self, code, reason=None):
        print("Closed down:",  reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        type_id=resp['type']
        sender=resp['sender'] if resp['sender'] !='' else 'khmcxq'

        if type_id==1:
            #监控某一个chatroom，并捕获核心关键内容，进行自动回复。
            if resp['wxid']=='6736538273@chatroom':
                #print(resp['content'])
                #如果输入?则显示菜单
                if resp['content']=='\uFF1F':
                    req = '{"id":'+"\""+getid()+"\""+r',"wxid":"6736538273@chatroom","content":"@'+sender+" "+menu_content+r'","roomid":"6736538273@chatroom","type":555}'
                    req_json=json.dumps(json.loads(req))
                    self.send(req_json)
                #如果输入A，则显示...
                if resp['content']=='A':
                    req = '{"id":'+"\""+getid()+"\""+r',"wxid":"6736538273@chatroom","content":"@'+sender+" "+zc_content+r'","roomid":"6736538273@chatroom","type":555}'
                    #print(req)
                    req_json=json.dumps(json.loads(req))
                    self.send(req_json)
                #如果输入B，则显示...
                if resp['content']=='B':
                    req = '{"id":'+"\""+getid()+"\""+r',"wxid":"6736538273@chatroom","content":"@'+sender+" "+ts_content+r'","roomid":"6736538273@chatroom","type":555}'
                    #print(req)
                    req_json=json.dumps(json.loads(req))
                    self.send(req_json)
                #如果输入C，则显示...
                if resp['content']=='C':
                    req = '{"id":'+"\""+getid()+"\""+r',"wxid":"6736538273@chatroom","content":"@'+sender+" "+do_content+r'","roomid":"6736538273@chatroom","type":555}'
                    #print(req)
                    req_json=json.dumps(json.loads(req))
                    self.send(req_json)

            if resp['wxid'].endswith("chatroom"):
                talk=sender +" 在 "+resp['time']+" 在 "+ resp['wxid']+"群中发送 "+resp['content']
            else:
                talk=sender +" 在 "+resp['time']+" 给 "+" khmcxq 发送 "+resp['content']
            with open("result.txt",'a',encoding='utf-8') as f:
                f.write(talk+"\n")
        elif type_id==5005:
            print("服务端心跳包发送！！！！！！") 
        else:
            print(resp)

class TK_WX(WebSocketClient):
    def opened(self):
        req = '{"id":'+"\""+getid()+"\""+r',"wxid":"2983091172@chatroom","content":"@杨宏华 机器人测试","roomid":"2983091172@chatroom","type":555}'
        req_json=json.dumps(json.loads(req))
        print(req_json)
        self.send(req_json)

    def closed(self, code, reason=None):
        print("Closed down:", reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        print(resp)
        self.close(reason='Bye bye')


if __name__ == '__main__':
    ws = None
    try:
        ws = CG_Client('ws://127.0.0.1:5555')
        ws.connect()
        ws.run_forever()
        #在群众聊天
        #tk = TK_WX('ws://127.0.0.1:5555')
        #tk.connect()
        #tk.run_forever()
    except KeyboardInterrupt:
        ws.close()