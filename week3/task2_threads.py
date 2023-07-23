import threading
from bs4 import BeautifulSoup
import time
import urllib.request


def get_crawl_content(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    request = urllib.request.Request(base_url, headers=headers)
    with urllib.request.urlopen(request) as response:
        html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def crawl_ptt_movie(base_url, post_entries):

    soup = get_crawl_content(base_url)

    for entry in soup.find_all("div", class_="r-ent"):
        title = entry.find("div", class_="title").get_text(strip=True)
        push_count = entry.find("div", class_="nrec").get_text(strip=True)

        # enter the post to get datetime
        link_element = entry.find("a")
        if link_element:
            link = "https://www.ptt.cc" + link_element["href"]
            publish_time = get_publish_time(link)
            post_entries.append((title, push_count, publish_time))
    # time.sleep(1)

    return post_entries


def get_page(iter):
    global link

    if (iter != 0):
        soup = get_crawl_content(link)
        next_link = soup.find("a", string="‹ 上頁")

        if next_link:
            next_link = "https://www.ptt.cc" + next_link["href"]
            link = next_link

    else:
        link = base_url

    return link


def get_publish_time(post_url):
    soup = get_crawl_content(post_url)

    date_elements = soup.find_all("span", class_="article-meta-value")
    if len(date_elements) >= 1:
        return date_elements[-1].get_text()
    else:
        return "Unknown"


def save_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("文章標題,推文數量,發佈時間\n")
        for entry in data:
            title, push_count, publish_time = entry
            file.write(f"{title},{push_count},{publish_time}\n")


if __name__ == "__main__":
    start_time = time.time()
    num_threads = 3
    threads = []
    post_entries = []
    base_url = 'https://www.ptt.cc/bbs/movie/index.html'
    for i in range(num_threads):
        # first get all links then start threading
        thread = threading.Thread(
            target=crawl_ptt_movie, args=(get_page(i), post_entries))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    save_to_file(post_entries, "movie2.txt")

    print(time.time() - start_time)
