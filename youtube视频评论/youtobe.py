from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

comment_total = 3200
url = 'https://www.youtube.com/watch?v=GaHcnPDcUOE'
proxy = '--proxy-server=http://127.0.0.1:10809'


def setup_chrome_driver(proxy):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(proxy)
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

driver = setup_chrome_driver(proxy)
driver.get(url)

count = 0
# 获取足够的评论数
while count < comment_total:
    length = count
    for i in range(60):
        driver.execute_script("document.documentElement.scrollBy(0, 100);")
    comment_blocks = driver.find_elements(By.TAG_NAME, 'ytd-comment-thread-renderer')
    count = len(comment_blocks)
    if length and length == count: # 如果没有新的评论加载出来，说明已经到了页面底部
        break

data = []
for comment_block in comment_blocks:
    author = comment_block.find_element(By.XPATH, './/*[@id="comment"]//*[@id="main"]//*[@id="author-text"]').text
    vote_count = comment_block.find_element(By.XPATH, './/*[@id="comment"]//*[@id="main"]//*[@id="vote-count-middle"]').text
    comment = comment_block.find_element(By.XPATH, './/*[@id="comment"]//*[@id="comment-content"]//*[@id="content"]').text
    data.append((author.replace('\n', ' ').replace('\r', ' '), vote_count, comment.replace('\n', ' ').replace('\r', ' ')))
    # print(author)
    # print(vote_count)
    # print(comment)
    # print('-----------------------------------')


filename = 'yuotube_comments.csv'

with open(filename, 'w', newline='', encoding='utf-8') as file: # 打开文件，准备写入
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, delimiter='#')     # 创建 CSV 写入器
    writer.writerow(['作者', '点赞数', '评论'])
    writer.writerows(data)

print(f'数据已经被写入到 {filename}')

# 关闭浏览器
driver.quit()