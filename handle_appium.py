import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from handle_db import get_random_uid

cap = {
    "platformName": "Android",
    "platformVersion": "4.4.2",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.ss.android.ugc.aweme",
    "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
    "noReset": True,
    "unicodekeyboard": True,
    "resetkeyboard": True
}
driver = webdriver.Remote("http://localhost:4723/wd/hub", cap)


def get_window_size():
    x = driver.get_window_size()["width"]
    y = driver.get_window_size()["height"]
    return(x,y)


try:
    # 判断页面是否有搜索按钮并点击
    if WebDriverWait(driver, 10).until(lambda x:x.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/amq']")):
        driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/amq']").click()
    else:
        # 判断是否出现广告，点击跳过广告
        driver.tap([(603, 21), (705, 57)])
        time.sleep(10)
except:
    pass


for i in range(1000):
    if WebDriverWait(driver, 10).until(lambda x:x.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/adj']")):
        # 输入抖音id并点击搜索
        driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/adj']").click()
        user_id = get_random_uid()["user_id"]
        if user_id != "0":
            driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/adj']").send_keys(user_id)
            driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/adm']").click()
            time.sleep(1)
            # 点击用户栏
            driver.tap([(269, 115), (330, 154)])
            time.sleep(1)
            # 点击用户头像进入用户主页
            driver.tap([(36, 210), (95, 265)])
            time.sleep(3)
            try:
                # 点击粉丝进入粉丝列表
                driver.find_element_by_xpath("//android.widget.TextView[@text='粉丝']").click()
                # driver.tap([(271, 672), (408, 683)])
                time.sleep(3)
                Coordinate = get_window_size()
                X = int(Coordinate[0]*0.5)
                y1 = int(Coordinate[1]*0.9)
                y2 = int(Coordinate[1]*0.1)

                try:
                    while True:
                        if "暂时没有更多了"or"TA还没有粉丝" in driver.page_source:
                            driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/lk']").click()
                            driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/lk']").click()
                            driver.tap([(18, 53), (44, 78)])
                        else:
                            driver.swipe(X, y1, X, y2)
                            time.sleep(0.5)
                except:
                    driver.tap([(14, 66), (53, 90)])
                    time.sleep(1)
                    driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.ss.android.ugc.aweme:id/lk']").click()
                    driver.tap([(18, 53), (44, 78)])
            except:
                driver.tap([(22, 59), (55, 90)])
                driver.tap([(18, 53), (44, 78)])
