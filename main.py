import requests
from bs4 import BeautifulSoup
import json


def get_info(id):
    url = f'http://amdy.su/page/{id}/'

    req = requests.get(url)
    src = req.text

    with open(f'index{id}.html', 'w', encoding='UTF-8') as file:
        file.write(src)

    with open(f'index{id}.html', encoding='UTF-8') as file:
        src = file.read()

    all_posts_dict = {}

    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all(class_='read-more')
    titles = soup.find_all(class_='entry-title')

    for item in links:
        link = item.find('a').get('href')
        print(link)
        for t in titles:
            title = t.text
            all_posts_dict[title] = link

    for item, t in zip(links, titles):
        link = item.find('a').get('href')
        title = t.text
        all_posts_dict[title] = link

    return all_posts_dict


new_dict_value = {}
for i in range(1, 10):
    res = get_info(i)
    new_dict_value[i] = res

with open('posts.json', 'w', encoding='UTF-8') as file:
    json.dump(new_dict_value, file, indent=4, ensure_ascii=False)

with open('posts.json', encoding='UTF-8') as file:
    all_posts = json.load(file)

count = 0

for value in all_posts.values():

    for post_title, post_link in value.items():
        rep = [' ', ',', "'", '-']

        for item in rep:
            if item in post_title:
                post_title = post_title.replace(item, '_')

        req = requests.get(post_link)
        src = req.text

        with open(f'data/{count}_{post_title}.html', 'w', encoding='UTF-8') as file:
            file.write(src)

        with open(f'data/{count}_{post_title}.html', encoding='UTF-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        title = soup.find(class_='entry-title')
        title = title.text
        content = soup.find(class_='entry-content').find_all('p')
        content_list = []
        for c in content:
            c = c.text
            content_list.append(c)

        with open('text.txt', 'a', encoding='UTF-8') as file:
            file.write(title)
            file.write('\n')
            content_write = '\n'.join(content_list)
            file.write(content_write)
            file.write('\n')
    count += 1
