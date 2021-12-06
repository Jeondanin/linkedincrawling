from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
import pandas as pd

options = ChromeOptions()
driver = Chrome("C://Users//danin//Downloads//chromedriver.exe",options=options)



    # target url
def crawling_user(user_info_list, n):
    if n == 1:
        url = "https://www.linkedin.com/search/results/people/?origin=GLOBAL_SEARCH_HEADER&profileLanguage=%5B%22ko%22%5D&schoolFilter=%5B%2217950%22%5D&sid=DR-"
    else:
        url = f"https://www.linkedin.com/search/results/people/?origin=GLOBAL_SEARCH_HEADER&page={n}&profileLanguage=%5B%22ko%22%5D&schoolFilter=%5B%2217950%22%5D&sid=D1_"
    driver.get(url)
    sleep(3)
    # ul
    ul_class= "reusable-search__entity-result-list"
    input_element = driver.find_element_by_class_name(ul_class)
    # loop
    user_list = input_element.find_elements_by_tag_name('li')
    # li
    for user in user_list:
        tmp = user.text.replace("\n", "")
        # app aware link 
        anchor_tag = user.find_element_by_class_name("app-aware-link")
        href_url = anchor_tag.get_attribute("href")
        user_info_list.append((tmp, href_url))
    return user_list

if __name__ == "__main__":
    driver.get("https://www.linkedin.com/login/ko?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    keyword = "USERID"
    # login
    input_element = driver.find_element_by_id("username")
    input_element.send_keys(keyword)
    keyword = "PASSWORD"
    input_element = driver.find_element_by_id("password")
    input_element.send_keys(keyword)
    input_element = driver.find_element_by_class_name("btn__primary--large")
    input_element.send_keys(Keys.RETURN)
    sleep(5)
    user_info_list = []
    n = 0
    while True:
        try:
            n += 1
            crawling_user(user_info_list, n)
            print(f"the number of people {len(user_info_list)}")
        except Exception as e:
            print(e)
            break
    print(user_info_list)
    tmp_df = pd.DataFrame(user_info_list)
    tmp_df.to_csv("user_info.csv")
sleep(200000)