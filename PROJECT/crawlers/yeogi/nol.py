from bs4 import BeautifulSoup

targetPath = "PROJECT/DATA/"
filename = "jeonju_nol.html"

fullPath = targetPath + filename

html = open(fullPath, 'r', encoding='UTF-8').read()
soup = BeautifulSoup(html, 'html.parser')

fullPath = targetPath + "jeonju_formatted.html"
with open(fullPath, 'w', encoding='utf-8') as f :
    f.write(soup.prettify())