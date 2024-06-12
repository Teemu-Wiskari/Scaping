import requests
import bs4
import fake_headers
import json

URL = ("https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python&excluded_text=&area=2&area=1&salary="
       "&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period="
       "0&items_on_page=50&hhtmFrom=vacancy_search_filter")

keys = ["Django", 'Flask']


def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()


response = requests.get(URL, headers=gen_headers())
main_html = response.text
main_page = bs4.BeautifulSoup(main_html, "lxml")
vacancies = main_page.find_all("div", class_="vacancy-serp__results", id="a11y-main-content")
results = []

for vacancy in vacancies:
    link = vacancy.find("a", class_="bloko-link")['href']
    name_company = vacancy.find("a", class_="bloko-link").text
    city = vacancy.find("span", class_="fake-magritte-primary-").text
    salary = vacancy.find("span", class_="fake-magritte-primary-").text

    if salary:
        salary = salary.text.strip()
    else:
        salary = "Не указано"

    description = vacancy.find(class_='g-user-content').text
    if any(key.lower() in description.lower() for key in keys):
        info = {
            'link': link,
            'name_company': name_company,
            'city': city,
            'salary': salary
        }
        results.append(info)

with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
