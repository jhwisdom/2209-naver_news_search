from requests import get
from bs4 import BeautifulSoup


def naver_search(keyword = None):
    base_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
            
        soup = BeautifulSoup(response.text, "html.parser")
        news_lists = soup.find_all('ul', class_='list_news')

        for news_section in news_lists:
            news_posts = news_section.find_all('li', class_="bx")
            
            for news in news_posts:
                newspaper = news.find('a', class_="info press")
                time = news.find_all('span', class_="info")

                #날짜 부분에 날짜가 아닌 내용이 들어오는 경우를 수정함
                if len(time) >= 2:
                    time = time[1]
                else:
                    time = news.find('span', class_="info")
                title = news.find('a', class_="news_tit")
                link = title['href']
                
                news_data = {
                    'newspaper' : newspaper.text.replace(",", " "),
                    'time' : time.text.replace(",", " "),
                    'title' : title.text.replace(",", " "),
                    'link' : f"{link}"
                }

                results.append(news_data)

    return results
