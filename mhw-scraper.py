import requests
from bs4 import BeautifulSoup
import re

r = requests.get('https://mhworld.kiranico.com/en/weapons?type=10')
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a')

first_link = "Iron Blade I"
last_link = "Kj\xc3\xa1rr Glaive \"Paralysis\"".encode('raw_unicode_escape').decode('utf-8')

unwanted_links = [
    "https://mhworld.kiranico.com/en/skilltrees/Ll8nL/guts",
    "https://mhworld.kiranico.com/en/skilltrees/bQgZL/hasten-recovery",
    "https://mhworld.kiranico.com/en/skilltrees/majGL/razor-sharp-spare-shot",
    "https://mhworld.kiranico.com/en/skilltrees/AJBJA/kulve-taroth-essence",
    "https://mhworld.kiranico.com/en/skilltrees/L7z7m/critical-element",
    "https://mhworld.kiranico.com/en/skilltrees/LzjrL/critical-status"
]

start_index = next((i for i, link in enumerate(links) if link.get_text(strip=True) == first_link), None)
end_index = next((i for i, link in enumerate(links) if link.get_text(strip=True) == last_link), None)

print(f'Start index: {start_index}, End index: {end_index}')

if start_index is not None and end_index is not None and start_index < end_index:
    for link in links[start_index:end_index + 1]:
        if link.get('href') in unwanted_links:
            continue
        url = link.get('href')
        name = link.get_text(strip=True).encode('utf-8')
        #if url and name:
        print(f'{name}: {url}')
        

# insect glaive: 1st: Iron Blade I, last: Kj\xc3\xa1rr Glaive "Paralysis"
# unwanted extra links (filter these out): 
# Guts: https://mhworld.kiranico.com/en/skilltrees/Ll8nL/guts
# Hasten Recovery: https://mhworld.kiranico.com/en/skilltrees/bQgZL/hasten-recovery
# Razor Sharp/Spare Shot: https://mhworld.kiranico.com/en/skilltrees/majGL/razor-sharp-spare-shot
# Kulve Taroth Essence: https://mhworld.kiranico.com/en/skilltrees/AJBJA/kulve-taroth-essence
# Critical Element: https://mhworld.kiranico.com/en/skilltrees/L7z7m/critical-element
# Critical Status: https://mhworld.kiranico.com/en/skilltrees/LzjrL/critical-status
# scraper will open those links and scrape those pages too

rw = requests.get('https://mhworld.kiranico.com/en/weapons/WgswETq4/beo-glaive-i')
soupw = BeautifulSoup(rw.text, 'html.parser')

# extract weapon rarity
tds = soupw.find('td')
tdstext = tds.get_text(strip=True).encode('utf-8').decode('utf-8')
raritynum = re.split(r'(\d+)', tdstext)[1]
print("Rarity: " + raritynum)

# extract weapon forge materials
start_keyword = "Required Cost"
end_keyword = "Tree"

htmlstr = str(soupw)

start_index = htmlstr.find(start_keyword)
end_index = htmlstr.find(end_keyword)

print(f'Start index: {start_index}, End index: {end_index}')

if start_index != -1 and end_index != -1 and start_index < end_index:
    sliced_html = htmlstr[start_index:end_index + len(end_keyword)]
    sliced_soup = BeautifulSoup(sliced_html, 'html.parser')

    links = sliced_soup.find_all('a')

    for link in links:
        if link.parent.parent.find('td').get_text(strip=True).encode('utf-8').decode('utf-8') == "Forge Equipment":
            continue
        url = link.get('href')
        name = link.get_text(strip=True).encode('utf-8')
        amt = (link.parent.parent.find_all('td')[2].get_text(strip=True).encode('utf-8').decode('utf-8')).replace("x", "")
        #if url and name:
        print(f'{name}, x{amt}: {url}')