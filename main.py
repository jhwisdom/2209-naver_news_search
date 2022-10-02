from naver import naver_search
from save2file import save_to_file

def search(keyword):
    if keyword == None:
        print("pls. input keyword again")
        return input()
    else:
        result = naver_search(keyword)
        print("search done")
        save_to_file(keyword, result)
        print("saved")
        #print(result, "\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\n\n")
    return result

word = input("input a keyword: ")
search(word)