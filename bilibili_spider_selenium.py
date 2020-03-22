from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

ser=input('请输入关键字')
#不加载图片提高效率
options = webdriver.ChromeOptions()
options.add_argument('--headless')#无界面
options.add_argument('--disable-gpu')
options.add_argument("window-size=1024,768")
options.add_argument("--no-sandbox")
prefs = {
              'profile.default_content_setting_values': {
                   'images': 2,
                }
             }
options.add_experimental_option('prefs', prefs)
browser= webdriver.Chrome(chrome_options=options)
browser.implicitly_wait(15)  # 隐性等待，最长等15秒
# browser.maximize_window()
browser.get("https://search.bilibili.com/")
browser.find_element_by_id("search-keyword").send_keys(ser,Keys.ENTER)
handle = browser.current_window_handle
o = 1#计数

while o!=51:
    for i in range(1,22):
        if i==21:
            browser.find_element_by_xpath("//button[@class='nav-btn iconfont icon-arrowdown3']").click()
            o += 1
        else:
        # try:
            browser.find_element_by_xpath("//li[@class='video-item matrix']"+str([i])+"/a").click()
            time.sleep(3)
            handles = browser.window_handles
            for newhandle in handles:
                tit = []
                like = []
                userjj = []
                username = []
                coin = []
                collect = []
                share = []
                # try:
                if newhandle!=handle:
                    try:
                        browser.switch_to_window(newhandle)
                        tit.append(browser.find_element_by_class_name("tit").text)
                        like.append(browser.find_element_by_class_name("like").get_attribute("title"))
                        userjj.append(browser.find_element_by_class_name("desc").text)
                        username.append(browser.find_element_by_class_name("username").text)
                        coin.append(browser.find_element_by_class_name("coin").text)
                        collect.append(browser.find_element_by_class_name("collect").text)
                        share.append(browser.find_element_by_class_name("share").text)
                        # info=browser.find_element_by_class_name("info open").text
                        print("第",o,"页",i,tit,"点赞：",like,"硬币：",coin,"收藏",collect,"分享",share,"用户名",username,"用户简介",userjj)

                        browser.close()
                        browser.switch_to_window(handles[0])
                        Data = pd.DataFrame(
                            {'标题': tit, '点赞': like, "用户简介": userjj, "up主": username, "硬币": coin, "收藏": collect,
                             "分享": share})
                        Data.to_csv('bilibili视频播放详细数据.csv', mode='a', header=False, index=False, sep=',',
                                    encoding='utf-8-sig')
                    except:
                        browser.close()
                        browser.switch_to_window(handles[0])
                    break
    if o == 51:
        browser.quit()