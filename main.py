from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

store_url = 'https://www.amazon.com/gp/video/storefront'

driver = webdriver.Chrome()
driver.get(store_url)

# hardcoded class vars
title = {
    "class": "h1",
    "name": "_2IIDsE _3I-nQy"
}
rating = {
    "class": "span",
    "name": "XqYSS8 FDDgZI"
}
synopsis = {
    "class": "div",
    "name": "_3qsVvm _1wxob_"
}
vid_dl_url = "/gp/video/detail/"

vid_links = []
titles = []
ratings = []
synopsises = []

def scrape_text(lst, class_type, class_name):
    find_class = soup.find_all(class_type, class_=class_name)
    if (len(find_class) == 0):
        lst.append(None)
    else:
        for n in find_class:
            if class_name == rating['name']:
                lst.append(float(n.text[-3:]))
            else:
                lst.append(n.text)

elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    if vid_dl_url in elem.get_attribute("href"):
        vid_links.append(elem.get_attribute("href"))

vid_links = list(dict.fromkeys(vid_links))

for i in range(0, len(vid_links)):
    driver.get(vid_links[i])
    content = driver.page_source
    soup = BeautifulSoup(content)

    scrape_text(titles, title["class"], title["name"])
    scrape_text(ratings, rating["class"], rating["name"])
    scrape_text(synopsises, synopsis["class"], synopsis["name"])

driver.close()
driver.quit()

data = { 'Title': titles, "Rating": ratings, "Synopsis": synopsises}
df = pd.DataFrame(data)
df.to_csv('PrimeVid.csv', index=False, encoding='utf-8')

def wc(df, filename):
    if len(df) < 1:
        return

    text = ' '.join(df.Synopsis)
    wordcloud=WordCloud().generate(text)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(filename+".png")

df1 = df.loc[(df['Rating'] < 6)]
df3 = df.loc[(df['Rating'] >= 6)]

wc(df1, "below6")
wc(df3, "above6")