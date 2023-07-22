from bs4 import BeautifulSoup
import time
import urllib.request


def crawl_ptt_movie(num_pages):
    base_url = "https://www.ptt.cc/bbs/movie/index.html"
    post_entries = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    for _ in range(num_pages):
        # response = requests.get(base_url)
        # soup = BeautifulSoup(response.text, 'html.parser')
        request = urllib.request.Request(base_url, headers=headers)
        with urllib.request.urlopen(request) as response:
            html_content = response.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        for entry in soup.find_all("div", class_="r-ent"):
            title = entry.find("div", class_="title").get_text(strip=True)
            push_count = entry.find("div", class_="nrec").get_text(strip=True)

            link_element = entry.find("a")
            if link_element:
                link = "https://www.ptt.cc" + link_element["href"]
                publish_time = get_publish_time(link)
                post_entries.append((title, push_count, publish_time))

        prev_page_link = soup.find("a", string="‹ 上頁")["href"]
        base_url = "https://www.ptt.cc" + prev_page_link

        time.sleep(1)

    return post_entries


def get_publish_time(post_url):
    # response = requests.get(post_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    request = urllib.request.Request(post_url, headers=headers)
    with urllib.request.urlopen(request) as response:
        html_content = response.read()
    soup = BeautifulSoup(html_content, 'html.parser')

    date_elements = soup.find_all("span", class_="article-meta-value")
    if len(date_elements) >= 4:
        return date_elements[3].get_text()
    else:
        return "Unknown"


def save_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("文章標題,推文數量,發佈時間\n")
        for entry in data:
            title, push_count, publish_time = entry
            file.write(f"{title},{push_count},{publish_time}\n")


if __name__ == "__main__":
    movie_lst = crawl_ptt_movie(3)
    save_to_file(movie_lst, "movie.txt")
