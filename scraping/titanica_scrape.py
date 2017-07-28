import requests
import pandas as pd
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

age_dfs = []
for age in range(0, 75):
    print("Parsing age:\t" + str(age))
    url = "https://www.encyclopedia-titanica.org/titanic-ages/" + str(age) + ".html"
    r = requests.get(url, headers=header)

    try:
        age_dfs.append(pd.read_html(r.text, flavor='bs4')[0])
        print("Parse Complete!")
    except ValueError:
        print("No passengers found...")


fr_age = pd.concat(age_dfs)
fr_age.to_csv('output.csv', encoding='utf-8')
