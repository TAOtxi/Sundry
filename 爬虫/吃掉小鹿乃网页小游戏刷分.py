from selenium import webdriver
import time

# 游戏网址  https://xingye.me/game/eatkano/index.php

def click():

    # 游戏显示层序号
    game = 1
    while True:
        path = r'//*[@id="GameLayer%d"]/*[contains(@class, "t")]' % game

        # 定位所有目标方块(class属性含有t的就是)
        elements = browser.find_elements('xpath', path)
        for i in elements:

            # 点击间隔，最好不要去掉或者太小，网址会过滤掉异常分数，貌似300分为阈值？
            time.sleep(0.0001)
            # Action.click(i).perform() # 这个也能点击，不过效率有点慢
            # browser.execute_script("arguments[0].click();", i) # 不知道为啥这个用不了

            # 点击小鹿乃方块~
            i.click()

            # 倒计时的时间，倒计时为1的时候就退出函数，不然游戏结束了一直点击下去会报错
            countdown = browser.find_element('xpath', r'//*[@id="GameTimeLayer"]').text
            if int(countdown.split(':')[1]) <= 1:
                return
        # for循环结束后，游戏显示层也就更新了，这里换一下序号
        if game == 1:
            game = 2
        else:
            game = 1

browser = webdriver.Chrome()
url = "https://xingye.me/game/eatkano/index.php"
browser.get(url=url)
time.sleep(1)

# 想上榜的话把下面代码的#去掉，设置上榜名字
# # 自己设置名字，最长好像7个字符
# name = 'Your Name'
# # 点击游戏设置
# browser.find_element('xpath', r'//*[@id="btn_group"]/div/a[2]').click()
# # 传入名字
# browser.find_element('xpath', r'//*[@id="username"]').send_keys(name)
# # 暂停2秒让本人看看有无错误
# time.sleep(2)
# # 确定
# browser.find_element('xpath', r'//*[@id="setting"]/button').click()

# 点击开始按钮
browser.find_element('xpath', r'//*[@id="btn_group"]/div/a[1]').click()

click()

# 防止程序结束后浏览器关闭
input()

