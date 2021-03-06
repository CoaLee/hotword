from konlpy.tag import Twitter
from collections import Counter
from operator import eq
import crawling

# 단어구름에 필요한 라이브러리를 불러옵니다.
import numpy as np
from PIL import Image
from wordcloud import WordCloud
# 그래프에 필요한 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

'''
    데이터 받아서 가공하는 함수
'''
# 폰트 설정
font_path = 'NanumGothic.ttf'

def get_tags(text, ntags=50):
    spliter = Twitter()
    # konlpy의 Twitter객체
    nouns = spliter.nouns(text)

    # 한 글자로 구성된 의미없는 문자 제거
    nouns_c = []
    for i in nouns:
        if len(i)==1:
            continue
        elif eq(i, "뉴스"):
            continue
        elif eq(i, "기자"):
            continue
        elif eq(i, "제공"):
            continue
        nouns_c.append(i)

    # nouns 함수를 통해서 text에서 명사만 분리/추출
    count = Counter(nouns_c)
    # Counter객체를 생성하고 참조변수 nouns할당

    return_dic = {}  # 명사 빈도수 저장할 변수
    for n, c in count.most_common(ntags):
        return_dic[n] = c
        # temp = {'tag': n, 'count': c}
        # return_list.append(temp)
    # most_common 메소드는 정수를 입력받아 객체 안의 명사중 빈도수
    # 큰 명사부터 순서대로 입력받은 정수 갯수만큼 저장되어있는 객체 반환
    # 명사와 사용된 갯수를 return_list에 저장합니다.
    return return_dic

def make_cloud_image(tags, output_name):
    '''
    wordcloud 패키지를 이용해 트럼프 대통령 실루엣 모양의 단어구름을 생성합니다.
    '''
    # word_to_count = {}
    # with open(tags_file) as file:
    #     for line in file:
    #         data=line.split()
    #         word, count = data[0], float(data[1])
    #         word_to_count[word] = count
    # mask = np.array(Image.open("trump.png"))

    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white",
        # mask= mask
    )

    wordcloud = wordcloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    fig.savefig("img_wordcloud/{0}.png".format(output_name))

def process_main(text_file_name):
# def process_main():
    # text_file_name = "test"
    # 분석할 파일
    noun_count = 150
    # 최대 많은 빈도수 부터 30개 명사 추출
    output_file_name = text_file_name+"_result.txt"
    # count.txt 에 저장
    open_text_file = open("category\\" + text_file_name+".txt", 'r', -1, "utf-8")
    # 분석할 파일을 open
    text = open_text_file.read()  # 파일을 읽습니다.
    tags = get_tags(text, noun_count)  # get_tags 함수 실행
    open_text_file.close()  # 파일 close
    # print(tags)
    # open_output_file = open(output_file_name, 'w', -1, "utf-8")
    # # 결과로 쓰일 count.txt 열기
    # for tag in tags:
    #     noun = tag['tag']
    #     count = tag['count']
    #     open_output_file.write('{} {}\n'.format(noun, count))
    # # 결과 저장
    # open_output_file.close()
   
    # cloud 이미지로 만들기
    make_cloud_image(tags, text_file_name)


def process_search(keyword):
    # def process_main():
    # text_file_name = "test"
    # 분석할 파일
    noun_count = 150
    # 최대 많은 빈도수 부터 30개 명사 추출
    output_file_name = keyword + "_result.txt"
    # count.txt 에 저장

    text = crawling.search_crawling(keyword) # 파일을 읽습니다.
    tags = get_tags(text, noun_count)  # get_tags 함수 실행
    # print(tags)
    # open_output_file = open(output_file_name, 'w', -1, "utf-8")
    # # 결과로 쓰일 count.txt 열기
    # for tag in tags:
    #     noun = tag['tag']
    #     count = tag['count']
    #     open_output_file.write('{} {}\n'.format(noun, count))
    # # 결과 저장
    # open_output_file.close()

    # cloud 이미지로 만들기
    result_code = make_cloud_image_search(tags, keyword)
    print("result_code 1: {}".format(result_code))
    return result_code

def make_cloud_image_search(tags, output_name):
    '''
    wordcloud 패키지를 이용해 트럼프 대통령 실루엣 모양의 단어구름을 생성합니다.
    '''
    # word_to_count = {}
    # with open(tags_file) as file:
    #     for line in file:
    #         data=line.split()
    #         word, count = data[0], float(data[1])
    #         word_to_count[word] = count
    # mask = np.array(Image.open("trump.png"))

    print("wordcloud: {}".format(str(tags)))
    if tags == {}:
        return -1

    wordcloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white",
        # mask= mask
    )

    wordcloud = wordcloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    fig.savefig("img_wordcloud/{0}.png".format('keyword_result'))

    return 1

# if __name__ == '__main__':
#     process_main()

