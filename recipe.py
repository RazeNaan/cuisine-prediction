import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
import time
import csv

browser = webdriver.Firefox()
URL = "https://www.yummly.com/recipes?allowedCuisine=cuisine^cuisine-italian"
r = browser.get(URL) 

lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(1000)
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

# Now that the page is fully scrolled, grab the source code.
source_data = browser.page_source

soup = BeautifulSoup(source_data, 'html5lib') 

recipes = soup.find_all('div', attrs = {'class':'recipe-card-img-wrapper'}) 

# print(recipes[0])
csvData = [['ID', 'Ingredients', 'Cuisine']]
recipe_ingredients = []
count = 1
for i in range(len(recipes)):
    for recipe in recipes[i].find_all('a', attrs = {'class': 'card-ingredients font-light micro-text flex-column'}):
        for ingredients in recipe.find_all('span'):
            recipe_ingredients.append(ingredients['title'])
            csvItem = [count, ingredients['title'], 'Italian']
            csvData.append(csvItem)
            count = count + 1
            print(count)

with open('recipe.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)

csvFile.close()
print (len(recipe_ingredients))
