import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from time import sleep

global search

if os.path.exists('C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/final.xlsx'):
    os.remove('C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/final.xlsx')

dollar = 40
dollars = "$"
search = input("Введите название телефона: ")
spl = search.split()
search1 = "-".join(spl)
items = []


def olx():
    global nname, pprice, cond1, url, res, res1
    url = f"https://www.olx.ua/d/uk/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/q-{search1}"
    pages = 5
    print(f"Страниц готово: 1/{pages}")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    everithing = soup.findAll("a", class_="css-rc5s2u")
    for item in everithing:
        name = item.find("h6", class_="css-1pvd0aj-Text eu5v0x0")
        prices = item.find('p')
        links = item.get("href")
        for names in name:
            nname = names.get_text()
        for price in prices:
            pprice = price.get_text()
            res = re.sub(" грн.", "", pprice)
            res1 = re.sub(" ", "", res)

        if search in nname:
            items.append(
                {
                    "name": nname,
                    "price": res1,
                    "link": "https://www.olx.ua" + links,
                    "res": "olx"
                }
            )

    for i in range(2, 5 + 1):  # парсінг решти сторінок
        r = requests.get(url + f"?page={i}")
        soup = BeautifulSoup(r.content, "html5lib")
        print(f"Страниц готово: {i}/{pages}")
        everithing = soup.findAll("a", class_="css-rc5s2u")
        for item in everithing:
            name = item.find("h6", class_="css-1pvd0aj-Text eu5v0x0")
            prices = item.find('p')
            links = item.get("href")
            condition = item.findAll("div", class_="css-1h0qipy")
            for names in name:
                nname = names.get_text()
            for price in prices:
                pprice = price.get_text()
                res = re.sub(" грн.", "", pprice)
                res1 = re.sub(" ", "", res)
            if search in nname:
                items.append(
                    {
                        "name": nname,
                        "price": res1,
                        "link": "https://www.olx.ua" + links,
                        "res": "olx"
                    }
                )
    z = pd.DataFrame(items)  # створення таблиці
    z.to_excel("C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/olx.xlsx",
               index=False)  # на основі створеної таблиці створення excel файлу
    items.clear()


def ob():
    global nname, pprice, link, res
    pages = 5
    print(f"Страниц готово: 1/{pages}")
    url = f"https://obyava.ua/ua/elektronika/mobilnye-telefony/s-{search1}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    everithing = soup.findAll("div", class_="single-item__content")
    for item in everithing:
        name = item.find("a", class_="single-item__title")
        prices = item.findAll('div', class_="single-item__price")
        for names in name:
            nname = names.get_text()
            link = name.get('href')
        for price in prices:
            pprice = price.get_text()
            pprice.replace(" ", "")
        if "ГРНторг" in pprice:
            res = pprice.replace("ГРНторг", "")
        elif "ГРН" in pprice:
            res = pprice.replace("ГРН", "")
        if search in nname:
            items.append(
                {
                    "name": nname.replace(" ", ''),
                    "price": res.replace(" ", ''),
                    "link": link,
                    "res": "ob"
                }
            )
    for i in range(2, pages + 1):
        r = requests.get(url + f"?page={i}")
        soup = BeautifulSoup(r.content, "html5lib")
        print(f"Страниц готово: {i}/{pages}")
        everithing = soup.findAll("div", class_="single-item__content")
        for item in everithing:
            name = item.find("a", class_="single-item__title")
            prices = item.findAll('div', class_="single-item__price")
            for names in name:
                nname = names.get_text()
                link = name.get('href')
            for price in prices:
                pprice = price.get_text()
                pprice.replace(" ", '')
            if "ГРНторг" in pprice:
                res = pprice.replace("ГРНторг", "")
            elif "ГРН" in pprice:
                res = pprice.replace("ГРН", "")
            if search in nname:
                items.append(
                    {
                        "name": nname.replace(" ", ''),
                        "price": res.replace(" ", ''),
                        "link": link,
                        "res": "ob"
                    }
                )
    z = pd.DataFrame(items)  # створення таблиці
    z.to_excel("C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/ob.xlsx",
               index=False)  # на основі створеної таблиці створення excel файлу
    items.clear()


def izi():
    global nname, pprice, price, res, llink, res1, res2
    pages = 5
    url = f"https://izi.ua/uk/c-490-mobilnie-telefony?search_text={search1}"
    print(f"Страниц готово: 1/{pages}")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    everithing = soup.findAll("li", class_="ek-grid__item b-catalog__item")
    for item in everithing:
        name = item.findAll("a")
        prices = item.findAll('span', class_="ek-text ek-text_size_h5 ek-text_weight_bold")
        for names in name:
            llink = names.get("href")
            nname = names.get("title")
        for price in prices:
            pprice = price.get_text()
            pprice.replace(" ", '')
        if "$" in pprice:
            res = pprice.replace("$", "")
            res = int(res) * int(dollar)
        elif "₴" in pprice:
            res = re.sub("₴", "", pprice)
            res1 = re.sub(" ", '', res)
            if "." in pprice:
                res1 = re.sub("\n", "", res1)
                res1 = float(res1)
                res1 = float('{:.0f}'.format(res1))
        items.append(
            {
                "name": nname.replace(" ", ''),
                "price": int(res1),
                "link": "https://izi.ua" + llink,
                "res": "izi"
            }
        )
    for i in range(2, pages + 1):
        r = requests.get(f"https://izi.ua/uk/c-490-mobilnie-telefony/page{i}?search_text={search}")
        soup = BeautifulSoup(r.content, "html5lib")
        print(f"Страниц готово: {i}/{pages}")
        everithing = soup.findAll("li", class_="ek-grid__item b-catalog__item")
        for item in everithing:
            name = item.findAll("a")
            prices = item.findAll('span', class_="ek-text ek-text_size_h5 ek-text_weight_bold")
            for names in name:
                llink = names.get("href")
                nname = names.get("title")
            for price in prices:
                pprice = price.get_text()
            if "$" in pprice:
                res = pprice.replace("$", "")
                res1 = int(res) * int(dollar)
            elif "₴" in pprice:
                res = re.sub("₴", "", pprice)
                res1 = re.sub(" ", '', res)
                if "." in pprice:
                    res1 = re.sub("\n", "", res1)
                    res1 = float(res1)
                    res1 = float('{:.0f}'.format(res1))
            items.append(
                {
                    "name": nname.replace(" ", ''),
                    "price": int(res1),
                    "link": "https://izi.ua" + llink,
                    "res": "izi"
                }
            )
    z = pd.DataFrame(items)  # створення таблиці
    z.to_excel("C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/izi.xlsx",
               index=False)  # на основі створеної таблиці створення excel файлу
    items.clear()


def kidstaff():
    global nname, pprice, price, res, llink, p1rice  # обозначення всіх змінних які будуть потрібні
    url = f"https://www.kidstaff.com.ua/goods/home/telefony/smartfony/words-{search1}"  # посилання
    pages = 5
    # парсінг першої сторінки
    print(f"Страниц готово: 1/{pages}")
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html5lib")
    everithing = soup.findAll("div", class_="goodscard column border-bottom-dotted is-half-mobile is-one-third-tablet "
                                            "is-one-quarter-desktop")
    for item in everithing:
        name = item.find("div",
                         class_="goodscard-title is-text-cut-ellipsis-line-2 is-size-7 has-text-grey")
        prices = item.find('div', class_="goodscard-price--current is-inline-block is-size-4")
        links = item.findAll("a")
        for names in name:
            nname = names.get_text()
        for price in prices:
            pprice = price.get_text()
            if pprice != "₴":
                p1rice = pprice
                p1rice = int(p1rice)
        for link1 in links:
            llink = link1.get("href")
        if search in nname:
            items.append(
                {
                    "name": nname,
                    "price": p1rice,
                    "link": llink,
                    "res": "kidstaff"
                }
            )
    for i in range(2, pages + 1):
        print(f"Страниц готово: {i}/{pages}")
        r = requests.get(url + f"?page-{i}")
        soup = BeautifulSoup(r.content, "html5lib")
        everithing = soup.findAll("div",
                                  class_="goodscard column border-bottom-dotted is-half-mobile is-one-third-tablet "
                                         "is-one-quarter-desktop")
        for item in everithing:  # цикл пошуку потрібних даних
            name = item.find("div",
                             class_="goodscard-title is-text-cut-ellipsis-line-2 is-size-7 has-text-grey")
            prices = item.find('div', class_="goodscard-price--current is-inline-block is-size-4")
            links = item.findAll("a")
            for names in name:
                nname = names.get_text()
            for price in prices:
                pprice = price.get_text()
                if pprice != "₴":
                    p1rice = pprice
                    p1rice = int(p1rice)
            for link1 in links:
                llink = link1.get("href")
            if search in nname:
                items.append(
                    {
                        "name": nname,
                        "price": p1rice,
                        "link": llink,
                        "res": "kidstaff"
                    }
                )
    z = pd.DataFrame(items)
    z.to_excel("C:/Users/shifu/Desktop/Манн/дорогой дневник/excel/kidstaff.xlsx",
               index=False)
    items.clear()
    print("Готово!")
    sleep(5)