#所谓的simple指的是只提供简单的功能，自动通知
import threading
import time
import SUST

auto_check = SUST.SUST()
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print('start new thread')
        while True:
            timenow = time.localtime(time.time())
            if timenow[3] == 7 and timenow[4] >= 30 and auto_check.morning_check is False:
                auto_check.run(24)
                continue
            elif timenow[3] == 1:
                auto_check.morning_check = False

def main():
    while True:
        timenow = time.localtime(time.time())
        if timenow[3] >= 7 and timenow[4] >= 12 and auto_check.morning_check is False:
            auto_check.run(24)
            continue
        elif timenow[3] >= 12 and timenow[4] >= 17 and auto_check.noon_check is False:
            auto_check.run(25)
            continue
        elif timenow[3] == 1:
            auto_check.morning_check = False
            auto_check.noon_check = False
    return

def test():
    auto_check.run(24)
    auto_check.run(25)

if __name__ == '__main__':
    test()