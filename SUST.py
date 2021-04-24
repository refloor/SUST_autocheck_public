from typing import ChainMap, List
from EmailSender import EmailSender
import requests
import random
import json
import time

class SUST:
    update_time: int = 0
    update_time_detail: str = ''
    morning_check: bool = False
    noon_check: bool = False
    day_check: bool = False
    morning_check_str: str = ''
    noon_check_str: str = ''

    retry: bool = False
    retry_code: int = 0

    sender: EmailSender = None

    add_list: list = None
    change_id_list: list = None
    key_list: list = ['KDJSIAOAUN']

    def __init__(self) -> None:
        with open('data.json','r', encoding='utf-8') as f:
            tarjson = json.load(f)
        if 'email' in tarjson:
            self.sender = EmailSender(tarjson['email'], tarjson['email_pwd'])
        self.add_list = []
        self.change_id_list = []

    def getCoookies(self, url: str):
        try:
            req = requests.get(url)
            cookies = req.headers['set-cookie']
            return cookies.split(';')[0].split('=')[1]
        except:
            return None

    def getStr(self, code: int, location: str = None) -> dict:
        a = 36
        b = random.randint(1, 5)
        sss = str(a) + '.' + str(b)
        loc = location if location else '陕西省+西安市+未央区+111县道+111县+靠近陕西科技大学学生生活区+&'
        tar_dic = None
        if code == 24:
            tar_dic = {
                '24[0][0][name]'.encode(): 'form[24][field_1588749561_2922][]'.encode(),
                '24[0][0][value]'.encode(): sss,
                '24[0][1][name]'.encode(): 'form[24][field_1588749738_1026][]'.encode(),
                '24[0][1][value]'.encode(): loc.encode(),
                '24[0][2][name]'.encode(): 'form[24][field_1588749759_6865][]'.encode(),
                '24[0][2][value]'.encode(): '是'.encode(),
                '24[0][3][name]'.encode(): 'form[24][field_1588749842_2715][]'.encode(),
                '24[0][3][value]'.encode():'否'.encode(),
                '24[0][4][name]'.encode(): 'form[24][field_1588749886_2103][]'.encode(),
                '24[0][4][value]'.encode(): '1'.encode()
            }
        elif code == 25:
            tar_dic = {
                '25[0][0][name]'.encode(): 'form[25][field_1588750276_2934][]'.encode(),
                '25[0][0][value]'.encode(): sss,
                '25[0][1][name]'.encode(): 'form[25][field_1588750304_5363][]'.encode(),
                '25[0][1][value]'.encode(): loc.encode(),
                '25[0][2][name]'.encode(): 'form[25][field_1588750323_2500][]'.encode(),
                '25[0][2][value]'.encode(): '是'.encode(),
                '25[0][3][name]'.encode(): 'form[25][field_1588750343_3510][]'.encode(),
                '25[0][3][value]'.encode():'否'.encode(),
                '25[0][4][name]'.encode(): 'form[25][field_1588750363_5268][]'.encode(),
                '25[0][4][value]'.encode(): '1'.encode()
            }
        elif code == 13:
            tar_dic={
                '13[0][0][name]'.encode():'form[13][field_1587635120_1722][]'.encode(),
                '13[0][0][value]'.encode():sss,
                '13[0][1][name]'.encode():'form[13][field_1587635142_8919][]'.encode(),
                '13[0][1][value]'.encode():'正常'.encode(),
                '13[0][2][name]'.encode():'form[13][field_1587635252_7450][]'.encode(),
                '13[0][2][value]'.encode():loc.encode(),
                '13[0][3][name]'.encode():'form[13][field_1587635509_7740][]'.encode(),
                '13[0][3][value]'.encode():'否'.encode(),
                '13[0][4][name]'.encode():'form[13][field_1587998920_6988][]'.encode(),
                '13[0][4][value]'.encode():'0'.encode(),
                '13[0][5][name]'.encode():'form[13][field_1587998777_8524][]'.encode(),
                '13[0][5][value]'.encode():'否'.encode(),
                '13[0][6][name]'.encode():'form[13][field_1587635441_3730][]'.encode(),
                '13[0][6][value]'.encode():'0'.encode()
            }
        return tar_dic

    def getCheckRes(self, code: int, cookie: str, location: str=None) -> dict:
        url = 'http://yiban.sust.edu.cn/v4/public/index.php/Index/formflow/add.html?desgin_id=13&list_id=9' if code == 13 else f' http://yiban.sust.edu.cn/v4/public/index.php/Index/formflow/add.html?desgin_id={code}&list_id=12'
        cookies = dict(PHPSESSID=cookie, client='android')
        head = {'Content-Type':'application/x-www-form-urlencoded','X-Requested-With': 'XMLHttpRequest','Connection': 'keep-alive'}
        try:
            req = requests.post(url, cookies=cookies, data=self.getStr(code, location), headers=head)
            return req.json()
        except:
            return None
    
    def clockin(self, student_info: dict, code: int) -> bool:
        name = student_info['name']
        url = student_info['url']
        cookie = None
        for i in range(3):
            cookie = self.getCoookies(url)
            if cookie != None:
                break
        else:
            print('[-]error in get cookies')
            return False
        result = None
        for i in range(3):
            if 'location' in student_info and len(student_info['location']) > 4:
                result = self.getCheckRes(code, cookie, location=student_info['location'])
            else:
                result = self.getCheckRes(code, cookie)
            if result == None:
                print(f'{name}:error in {i},trying the next time')
                continue
            if 'code' not in result:
                continue
            if result['code'] == 1 or result['code'] == 0:
                if code == 24:
                    student_info['morning_check'] = True
                else:
                    student_info['noon_check'] = True
                break
        else:
            if code == 24:
                student_info['morning_check'] = False
            else:
                student_info['noon_check'] = False
            print(f'{name}:error in check')
            return False
        print(f'{name}:check in finish!', end='')
        print(result)
        return True

    def run(self, code: int):
        codes = [24, 25, 13]
        if code not in codes:
            return
        curtime = time.localtime(time.time())
        self.update_time_detail = f'{curtime[1]}|{curtime[2]} {curtime[3]}:{curtime[4]}:{curtime[5]}'
        print(self.update_time_detail+':', end='')
        with open('data.json', 'r', encoding='utf-8') as f:
            tar_json = json.load(f)
        tar_list: list = tar_json['data']
        all_ = len(tar_list)+len(self.add_list)
        succ = 0
        fail_name_list = []

        for tar in tar_list:
            if self.clockin(tar, code) is True:
                succ += 1
            else:
                self.change_id_list.append(tar['id'])
                fail_name_list.append(tar['name'])
                del tar
        
        while len(self.add_list)>0:
            tar = self.add_list.pop()
            tar_list.append(tar)
            if self.clockin(tar, code) is True:
                succ += 1
            else:
                self.change_id_list.append(tar['id'])

        tar_json['last_update_day'] = curtime[2]
        self.update_time = curtime[2]
        if code == 24:
            self.morning_check = True
            self.morning_check_str = f'{succ}/{all_}'
        elif code == 25:
            self.noon_check = True
            self.noon_check_str = f'{succ}/{all_}'
        else:
            self.day_check = True
        with open('data.json', 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(tar_json, indent=4, ensure_ascii=False))
        if self.sender is not None:
            if not self.sender.send(tar_json['email_send'], 
                                    f'code:{code} had done,at{self.update_time_detail}, fail_list:{fail_name_list}', 
                                    f'[success] code:{code} had done'):
                print('[error] can not send email')
    def getRandomID(self):
        res = ''
        for i in range(5):
            a = random.randint(10, 50)
            res += str(a)
        return res

    def getLocation(self, position: str) -> str:

        url = f'http://api.map.baidu.com/reverse_geocoding/v3/?ak=uwGCSvEZY9kGWWp2fGOV3brU2zj1rFPB&output=json&coordtype=wgs84ll&location={position}'
        response = requests.get(url)
        data = response.json()
        if data['status'] != 0:
            return None
        tar:dict = data['result']['addressComponent']
        province = tar['province']
        city = tar['city']
        district = tar['district']
        street = tar['street']
        result_str = f'{province}+{city}+{district}+{street}+&'
        return result_str

    def addurl(self, url: str) -> bool:
        if len(url) != 221:
            return False
        if url[0:44] != 'http://yiban.sust.edu.cn/v4/public/index.php':
            return False
        response = requests.get(url=url)
        name = response.text
        try:
            name = name[name.rfind('：')+1: len(name)-29]
        except ValueError as e:
            print(e)
            return False
        tar = {'name':name, 'id':self.getRandomID(), 'url':url, 'morning_check':False, 'noon_check':False}
        self.add_list.append(tar)
        return True


def Test():
    sust = SUST()
    sust.run(24)
    return

if __name__ == "__main__":
    Test()