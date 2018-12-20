
import urllib.request
from bs4 import BeautifulSoup



def crawling(category):

    if category.find('category_society') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/society?page=",category)
    elif category.find('category_politics') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/politics?page=",category)
    elif category.find('category_economic') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/economic?page=",category)
    elif category.find('category_foreign') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/foreign?page=",category)
    elif category.find('category_culture') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/culture?page=",category)
    elif category.find('category_entertain') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/entertain?page=",category)
    elif category.find('category_sports') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/sports?page=",category)
    elif category.find('category_digital') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/digital?page=",category)
    elif category.find('category_editorial') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/editorial?page=",category)
    elif category.find('category_press') != -1:
        make_txt_crawling("https://media.daum.net/breakingnews/press?page=",category)


def make_txt_crawling(url,category):

    list_href = []
    list_content = []
    texttt = ""
    # 페이지 href 찾는부분
    for i in range(1, 10):
        urls = url + str(i)
        soup = BeautifulSoup(urllib.request.urlopen(urls).read(), "html.parser")
        for ul_tags in soup.find_all("ul", class_='list_news2 list_allnews'):
                for a_tags in ul_tags.find_all("a", class_='link_txt'):
                    list_href.append(a_tags["href"])
    print(list_href)
    # href에 있는 내용 부분 크롤링
    for urls in list_href:
        soup = BeautifulSoup(urllib.request.urlopen(urls).read(), "html.parser")
        for content in soup.find_all("section"):
            list_content.append(content.get_text())


    print("d")
    # list -> 문자열로 바꿈
    text = ""
    for i in list_content:
        text += i
    # 문장을 -> 각 단어로

    #words = text.split()

    #keywords = []
    # for i in words:
    #     if len(i) >= 2:
    #         keywords.append(i)
    #
    # text2 = ""
    # for i in keywords:
    #     text2 += i + " "

    fw = open(category+".txt", 'w', -1, "utf-8")
    fw.write(text)
    fw.close()

crawling('category_society')
crawling('category_politics')
crawling('category_economic')
crawling('category_foreign')
crawling('category_culture')
crawling('category_entertain')
crawling('category_digital')
crawling('category_sports')
crawling('category_editorial')
crawling('category_press')
