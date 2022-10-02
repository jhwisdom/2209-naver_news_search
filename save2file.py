def save_to_file(file_name, news_list):
    file = open(f"{file_name}.csv", "w")
    file.write("Newspaper, Time, Title, URL\n")

    for news in news_list:
        file.write(f"{news['newspaper']}, {news['time']}, {news['title']}, {news['link']}\n")

    file.close()
    print("finished")