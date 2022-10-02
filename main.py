from naver import naver_search
from save2file import save_to_file

def search(keyword):
    if keyword == None:
        print("Pls. input keyword again: ")
        return input()
    else:
        result = naver_search(keyword)
        print("search done")
        save_to_file(keyword, result)
        print("saved")

    return result

word = input("Input a keyword: ")
search(word)