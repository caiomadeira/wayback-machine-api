from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, BrowserType, expect, Selectors
import os
import requests
from link import *

path = 'http://archive.org/'

def user_url(date: str, **kwargs):
    url = kwargs.get('url')
    if url == None or url == '' or url == ' ':
        raise TypeError('You need to pass a valid url')
    else:
        return f'https://web.archive.org/web/{date}*/' + kwargs.get('url').replace(" ", "%20")


def search(url: str, year: any, day: int, month_name: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=100)
        pg = browser.new_page()
        pg.goto(user_url(date=str(year), url=url))
        #html_content = pg.content()
        #print(html_content)
        #return html_content
        # Wait for the div to be loaded
        pg.wait_for_selector('.calendar-layout')  # Wait for the outer div to be loaded
        calendar_layout = pg.query_selector('.calendar-layout')  # Get the outer div ElementHandle
        pg.wait_for_selector('.calendar-grid')
        calendar_grid = calendar_layout.query_selector('.calendar-grid')  # Get the inner div ElementHandle
        
        calendar_grid.wait_for_selector('.month')
        if calendar_grid:
            month_grid = calendar_grid.query_selector_all('.month')
            #link = get_link_for(day=day, selector=month_grid)
            #print("link: ", link)
            
            months = get_all_months(selector=month_grid)
            snp_days = get_snapshots_days(months=months)
            print("snp days: ", snp_days)
            browser.close()
    # acess page
    #access_pg(link=get_link)
    #html_parse()
    
def get_link_for(day: int, selector: any) -> str:
    get_link = str()
    months = get_valid_days(selector=selector)
    for month in months:
        for month_name, month_content in month.items():
            if month[month_name]:
                for days in month_content:
                    for day_key, day_value in days.items():
                        if int(day_key) == day:
                            for link in day_value:
                                get_link = link
    return get_link
            
def archive_goto(link: str):
    path: str = 'https://web.archive.org'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=100)
        pg = browser.new_page()
        pg.goto(url=path + link)
        pg.wait_for_selector('form')
        
        form_element = pg.query_selector('form')
        pg.wait_for_selector('img')
        img_elements = form_element.query_selector_all('img')
        img_urls = [img.get_attribute('src') for img in img_elements]
        print(img_urls)
        for img_url in img_urls:
            if img_urls:
                try:
                    download_file(url='https://web.archive.org' + img_url, path='tmp/')
                except Exception as e:
                    print("Failed to download.", e)
        
        #create_file(content=form_element.inner_html(), path='tmp')


def download_file(url: str, path: str):
    filename = url.split('/')[-1]
    print("filename: ", filename)
    local_path = os.path.join(path, filename)
    print("url:", url)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path

def get_all_months(selector: any) -> dict:
    handlers: dict = {}
    for month in selector:
        month_title = month.query_selector('.month-title')
        month_title_text = month_title.inner_text()
        month_body = month.query_selector('.month-body')
        handlers[month_title_text] = month_body
    return handlers

def get_weeks(selector: list, for_month=None, textfy=None) -> list:
    if textfy != None and type(textfy) != bool and for_month != None and for_month != 'all':
        raise ValueError("The parameter 'textfy' only works with no month selected (wich means all months).")
    count = 0
    handlers: dict = {}
    for title, body in selector.items():
        if for_month and for_month != 'all':
            if for_month == title:
                if body:
                    weeks_selector = body.query_selector_all('.month-week')
                    for week in weeks_selector:
                        handlers[str(count)] = week
                        count = count + 1
        else:
            all_weeks: list = []
            if body:
                weeks_selector = body.query_selector_all('.month-week')
                for week in weeks_selector:
                    if textfy:
                        all_weeks.append(week.inner_text().split('\n'))
                    else:
                        all_weeks.append(week)
                handlers[title] = all_weeks
    return handlers

def get_days(months: list, for_month='all'):
    handlers: dict = {}
    if for_month == None or for_month == 'all':
        month_weeks = get_weeks(selector=months, for_month='all')
        for month_name, weeks in month_weeks.items():
            all_days: list = []
            for week in weeks:
                days = week.query_selector_all('.month-day-container')
                all_days.extend([day for day in days])
            handlers[month_name] = all_days
    else:
        raise ValueError("Feature for a specific month not implemented yet.")
    return handlers

def get_snapshots_days(months: list, for_month='all'):
    valid_days: dict = {}
    if for_month == None or for_month == 'all':
        days = get_days(months=months)
        for month_name, days_list in days.items():
            for day in days_list:
                calendar_days = day.query_selector_all('.calendar-day')
                if calendar_days:
                    for calendar_day in calendar_days:
                        positions = calendar_day.query_selector_all('a[href]')
                        valid_links = [link.get_attribute('href') for link in positions]
                        valid_days[month_name] = { str(day.inner_text()): valid_links}
    else:
        raise ValueError("Feature for a specific month not implemented yet.")
    print("valid_days: ", valid_days)
    return valid_days

def save_html(date, url):
    content = search(date=date, url=url)
    create_file(content=content)
        
# Criar em C posteriormente
def create_file(content: str, path: str):
    with open(f"{path}/index.html", "w+") as f:
        f.write(content)
    f.close()
    
    
if __name__ == '__main__':
   search(url='www.google.com', year=1998, day=2, month_name='DEC')