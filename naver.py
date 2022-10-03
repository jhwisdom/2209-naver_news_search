from requests import get
from bs4 import BeautifulSoup

#페이지 이동하며 크롤링하기
def get_page_count(keyword, start_page, limit):

    base_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
    full_url = f"{base_url}{keyword}"
    response = get(full_url)

    if response.status_code != 200:
        print("Can't request website")
    else:
        soup = BeautifulSoup(response.text, "html.parser")

        pagination = soup.find("div", class_="sc_page_inner")

        if pagination == None:
            return 1
        
        #start_page = input("Choose which page to start from: ")
        #limit = input("Make a limit to the end page during searching (number of end page): ")
        if start_page == None:
            count = 1
        else: count = int(start_page) #서칭을 시작할 페이지 쪽수
        
        page_number = page_turner(count, int(limit), full_url)
        print(page_number)
    return page_number



def page_turner(count_start, limit, full_url):
    total_page = []
    page = len(total_page)
    start = count_start
    
    """
    if start > limit:
        print("Wrong directive. Pls. insert right number of page.")
        start = int(input("Choose which page to start from: "))
        limit = int(input("Make a limit to the end page during searching (number of end page): "))        
    """
    
    while start <= page+count_start:
        print("start: ", start)

        page_turner = get(f"{full_url}&start={start*10+1}")
        soup = BeautifulSoup(page_turner.text, "html.parser")
        pagination = soup.find("div", class_="sc_page_inner")
        pages = pagination.find_all("a", class_="btn", recursive = False)

        if start == 0 and limit >9:
            for one in range(len(pages)):
                print("one: ", one)
                total_page.append(one)
                print("total: ", total_page)
                page = len(total_page)
                start += 1

        elif page == int(limit-1):   #서칭 가능한 쪽수 리밋 설정 
            print(f"{page}쪽 도달")
            print(total_page)
            break

        elif (start == 0 and limit<=9) or (start >= 1 and pages[1].string) :
            total_page.append(start-1)
            page = len(total_page)
            start += 1


    count = len(total_page)        
    #choose_pages = input(f"How many pages do you want to search? (from {count_start} page to {count+1} page): ")
    for choice in range(int(count)+1):
        finish = total_page[:choice]
    
    return finish




def naver_search(keyword = None, start_page = 0, limit = None):

    pages = get_page_count(keyword, start_page, limit)
    print("Found", pages, "pages")

    results = []

    #페이지를 넘기며 크롤링하기
    for page in pages:
        base_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
        response = get(f"{base_url}{keyword}&start={int(page)*10+1}") #start= 부분이 페이지에 따라 변하는 부분
        print(int(page)*10+1)  
                
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
