# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv

class Extraction():

    def has_class(self,tag):
        return tag.has_attr('class')


    def get_all_game_links(self):
        url = "https://itch.io/jam/slavic-game-jam-2017"
        print("Downloading " + url)
        r = requests.get(url)
        r.encoding = 'utf-8'

        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        games = soup.find_all("a", {"class": "thumb_link"})
        game_links = []

        for game in games:
            game_links.append(game['href'])

        return game_links


    def get_game_info_dict(self,game_url):
        r = requests.get(game_url)
        r.encoding = 'utf-8'
        data = r.text

        soup = BeautifulSoup(data, "html.parser")

        game_info_dict = {}

        game_info_dict['game_title'] = soup.find_all("h1", {"class": "game_title"})[0].string if len(
            soup.find_all("h1", {"class": "game_title"})) > 0 else ''
        print("game_title =", game_info_dict['game_title'])

        game_info_dict['sub_title'] = soup.find_all("div", {"class": "header_buy_row"})[0].text if len(
            soup.find_all("div", {"class": "header_buy_row"})) > 0 else ''
        print("sub_title =", game_info_dict['sub_title'])

        game_info_dict['description'] = soup.find_all("div", {"class": "formatted_description"})[0].text if len(
            soup.find_all("div", {"class": "formatted_description"})) > 0 else ''
        print("description =", game_info_dict['description'])

        game_info_dict['url'] = game_url
        print("url =", game_info_dict['url'])
        info_row = {}
        game_info2 = soup.find_all("div", {"class": "game_info_panel_widget"})[0].table.tbody.contents if len(
            soup.find_all("div", {"class": "game_info_panel_widget"})) > 0 else list()
        for info in game_info2:
            info_row[info.contents[0].text] = info.contents[1].text
            # print(info.contents[0].text+" | "+info.contents[1].text)

        print(info_row)
        game_info_dict['authors'] = info_row.get('Authors')
        print("authors =", game_info_dict['authors'])

        game_info_dict['published'] = info_row.get('Published')
        print("published =", game_info_dict['published'])

        game_info_dict['status'] = info_row.get('Status')
        print("status =", game_info_dict['status'])

        game_info_dict['platforms'] = info_row.get('Platforms')
        print("platforms =", game_info_dict['platforms'])

        game_info_dict['rating'] = info_row.get('Rating')
        print("rating =", game_info_dict['rating'])

        game_info_dict['genre'] = info_row.get('Genre')
        print("genre =", game_info_dict['genre'])

        return game_info_dict


    def run(self,urls):

        with open('app/static/sites_metadata.csv', 'w') as csvfile:
            fieldnames = ['title', 'language', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            
            row = {}
            row['title']="SOME TITLE"
            row['language']="SOME SUBTITLE"
            row['url']="some url"
            
            writer.writerow(row)
            
            
        print("Data extraction successful.")


    
