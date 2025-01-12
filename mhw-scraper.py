import requests
from bs4 import BeautifulSoup
import re
import json
from fake_useragent import UserAgent

header = {
    'User-Agent': UserAgent().chrome,
    'Referer': 'https://mhworld.kiranico.com/en/',
}

def equipment_scraper():
    r = requests.get('https://mhworld.kiranico.com/en/weapons?type=13', headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    equipments = []
    weapons = []

    links = soup.find_all('a')

    #\u00e1 is á
    first_link = "Chain Blitz I".encode('utf-8').decode('utf-8')
    last_link = "Erupter Gold Razer".encode('utf-8').decode('utf-8')

    unwanted_links = [
        "https://mhworld.kiranico.com/en/skilltrees/Ll8nL/guts",
        "https://mhworld.kiranico.com/en/skilltrees/bQgZL/hasten-recovery",
        "https://mhworld.kiranico.com/en/skilltrees/majGL/razor-sharp-spare-shot",
        "https://mhworld.kiranico.com/en/skilltrees/AJBJA/kulve-taroth-essence",
        "https://mhworld.kiranico.com/en/skilltrees/L7z7m/critical-element",
        "https://mhworld.kiranico.com/en/skilltrees/LzjrL/critical-status",
        "https://mhworld.kiranico.com/en/skilltrees/LnBNL/protective-polish",
    ]

    start_index = next((i for i, link in enumerate(links) if link.get_text(strip=True) == first_link), None)
    end_index = next((i for i, link in enumerate(links) if link.get_text(strip=True) == last_link), None)

    print(f'Start index: {start_index}, End index: {end_index}')

    if start_index is not None and end_index is not None and start_index < end_index:
        for link in links[start_index:end_index + 1]:
            if link.get('href') in unwanted_links:
                continue
            url = link.get('href')
            name = link.get_text(strip=True).encode('utf-8').decode('utf-8')
            #if url and name:
            weapons.append([name, url])

    print(weapons)

    # insect glaive: 1st: Iron Blade I, last: Kj\xc3\xa1rr Glaive "Paralysis"
    # unwanted extra links (filter these out): 
    # Guts: https://mhworld.kiranico.com/en/skilltrees/Ll8nL/guts
    # Hasten Recovery: https://mhworld.kiranico.com/en/skilltrees/bQgZL/hasten-recovery
    # Razor Sharp/Spare Shot: https://mhworld.kiranico.com/en/skilltrees/majGL/razor-sharp-spare-shot
    # Kulve Taroth Essence: https://mhworld.kiranico.com/en/skilltrees/AJBJA/kulve-taroth-essence
    # Critical Element: https://mhworld.kiranico.com/en/skilltrees/L7z7m/critical-element
    # Critical Status: https://mhworld.kiranico.com/en/skilltrees/LzjrL/critical-status
    # scraper will open those links and scrape those pages too

    for weapon in weapons:
        weaponname = weapon[0]
        url = weapon[1]

        rw = requests.get(url, headers=header)
        soupw = BeautifulSoup(rw.text, 'html.parser')

        print(url)
        # extract weapon rarity
        tds = soupw.find('td')
        tdstext = tds.get_text(strip=True).encode('utf-8').decode('utf-8')
        raritynum = re.split(r'(\d+)', tdstext)[1]
        print("Rarity: " + raritynum)

        # extract weapon forge materials
        start_keyword = "Required Cost"
        end_keyword = "Tree" # sometimes it says "Unavailable"
        end_keyword_alt = "Unavailable"

        htmlstr = str(soupw)

        start_index = htmlstr.find(start_keyword)
        if htmlstr.find(end_keyword) == -1:
            end_index = htmlstr.find(end_keyword_alt)
        else:
            end_index = htmlstr.find(end_keyword)

        print(f'Start index: {start_index}, End index: {end_index}')

        if start_index != -1 and end_index != -1 and start_index < end_index:
            sliced_html = htmlstr[start_index:end_index + len(end_keyword)]
            sliced_soup = BeautifulSoup(sliced_html, 'html.parser')

            links = sliced_soup.find_all('a')

            materials_forge = []
            materials_upgrade = []

            for link in links:
                if link.parent.parent.find('td').get_text(strip=True).encode('utf-8').decode('utf-8') == "Forge Equipment":
                    url = link.get('href')
                    name = link.get_text(strip=True).encode('utf-8').decode('utf-8')
                    amt = (link.parent.parent.find_all('td')[2].get_text(strip=True).encode('utf-8').decode('utf-8')).replace("x", "")
                    #if url and name:
                    temp = {"name": name, "quantity": amt, "url": url}
                    materials_forge.append(temp)
                elif link.parent.parent.find('td').get_text(strip=True).encode('utf-8').decode('utf-8') == "Upgrade Equipment":
                    url = link.get('href')
                    name = link.get_text(strip=True).encode('utf-8').decode('utf-8')
                    amt = (link.parent.parent.find_all('td')[2].get_text(strip=True).encode('utf-8').decode('utf-8')).replace("x", "")
                    #if url and name:
                    temp = {"name": name, "quantity": amt, "url": url}
                    materials_upgrade.append(temp)
            
            equipments.append(
                {"name": weaponname,
                "type": "lbg", # IMPORTANT -----------------------------------------------------------------------------------------------------
                # IMPORTANT -----------------------------------------------------------------------------------------------------
                # IMPORTANT -----------------------------------------------------------------------------------------------------
                # IMPORTANT -----------------------------------------------------------------------------------------------------
                # IMPORTANT -----------------------------------------------------------------------------------------------------
                # IMPORTANT -----------------------------------------------------------------------------------------------------
                "rarity": raritynum,
                "materials-forge": materials_forge,
                "materials-upgrade": materials_upgrade,
                })

    print(equipments)

    with open('mhw-tools/drop-list/items-list/temp.json', 'w') as f:
        json.dump(equipments, f, indent=4)


def determine_type(material, mined):
    if material["name"] in mined:
        return "mining-outcrop"
    else:
        return "carve-quest"

def get_mined_materials(material):
    url = material["url"]
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    tds = soup.find('td')
    tdstext = tds.get_text(strip=True).encode('utf-8').decode('utf-8')
    raritynum = re.split(r'(\d+)', tdstext)[1]

    start_keyword = "Where to find " + material["name"]
    end_keyword = "What " + material["name"] + " is used for"

    htmlstr = str(soup)

    start_index = htmlstr.find(start_keyword)
    end_index = htmlstr.find(end_keyword)

    print(f'Start index: {start_index}, End index: {end_index}', material["url"])

    if start_index != -1 and end_index != -1 and start_index < end_index:
        sliced_html = htmlstr[start_index:end_index + len(end_keyword)]
        sliced_soup = BeautifulSoup(sliced_html, 'html.parser')

        rows = sliced_soup.find_all('tr')

        locales = []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                p1 = cols[0].get_text(strip=True).encode('utf-8').decode('utf-8')
                p2 = cols[1].get_text(strip=True).encode('utf-8').decode('utf-8')
                p3 = cols[2].get_text(strip=True).encode('utf-8').decode('utf-8')

                if not p3 == "Mining Outcrop":
                    continue

                full_source = p1 + " " + p2 + " Mining Outcrop"
                locales.append(full_source)
        
    return locales, raritynum

def get_materials_mix(material):
    url = material["url"]
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    tds = soup.find('td')
    tdstext = tds.get_text(strip=True).encode('utf-8').decode('utf-8')
    raritynum = re.split(r'(\d+)', tdstext)[1]

    start_keyword = "Where to find " + material["name"]
    end_keyword = "What " + material["name"] + " is used for"

    htmlstr = str(soup)

    start_index = htmlstr.find(start_keyword)
    end_index = htmlstr.find(end_keyword)

    monsters = []
    quests = []

    print(f'Start index: {start_index}, End index: {end_index}', material["url"])

    if start_index != -1 and end_index != -1 and start_index < end_index:
        sliced_html = htmlstr[start_index:end_index + len(end_keyword)]
        sliced_soup = BeautifulSoup(sliced_html, 'html.parser')

        rows = sliced_soup.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 0:
                p1 = cols[0].get_text(strip=True).encode('utf-8').decode('utf-8')
                p2 = cols[1].get_text(strip=True).encode('utf-8').decode('utf-8')

                full_source = p1 + " " + p2

                if p2 == "Quest Rewards":
                    if full_source not in quests:
                        quests.append(full_source)
                else:
                    if full_source not in monsters:
                        monsters.append(full_source)
                
    return monsters, quests, raritynum

def get_material_sources(material):
    url = material["url"]
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    tds = soup.find('td')
    tdstext = tds.get_text(strip=True).encode('utf-8').decode('utf-8')
    raritynum = re.split(r'(\d+)', tdstext)[1]

    start_keyword = "Where to find " + material["name"]
    end_keyword = "What " + material["name"] + " is used for"

    htmlstr = str(soup)

    start_index = htmlstr.find(start_keyword)
    end_index = htmlstr.find(end_keyword)

    print(f'Start index: {start_index}, End index: {end_index}', material["url"])

    if start_index != -1 and end_index != -1 and start_index < end_index:
        sliced_html = htmlstr[start_index:end_index + len(end_keyword)]
        sliced_soup = BeautifulSoup(sliced_html, 'html.parser')

        rows = sliced_soup.find_all('tr')

        sources = []

        for row in rows:
            cols = row.find_all('td')
            temp_array = []
            for col in cols:
                temp_array.append(col.get_text(strip=True).encode('utf-8').decode('utf-8'))

            sources.append(temp_array)

    return sources, raritynum

def materials_scraper():
    # materials scraper

    mined = [
        "Iron Ore",
        "Machalite Ore",
        "Dragonite Ore",
        "Carbalite Ore",
        "Fucium Ore",
        "Eltalite Ore",
        "Meldspar Ore",
        "Earth Crystal",
        "Coral Crystal",
        "Dragonvein Crystal",
        "Spiritvein Crystal",
        "Lightcrystal",
        "Novacrystal",
        "Purecrystal",
        "Firecell Stone",
        "Bathycite Ore",
        "Gracium",
        "Aquacore Ore",
        "Spiritcore Ore",
        "Dreamcore Ore",
        "Dragoncore Ore",
        "Phantomcore Ore",
        "Shadowcore Ore",
    ]

    # if mined, ONLY check for mining outcrops, NO quest rewards. IGNORE Seliana Supply Cache    DONE!
    # if material has both monster drops and quest rewards, IGNORE quest rewards
    # if material has only quest rewards, use quest rewards
    # For all materials, take first two columns of table.

    # Rerun weapon scraper, added new part.

    materials_json = []
    searched_links = []

    with open('mhw-tools/drop-list/items-list/materials.json') as f:
        mats = json.load(f)
        for mat in mats:
            searched_links.append(mat["url"])

    with open('mhw-tools/drop-list/items-list/temp.json') as f:
        equipments = json.load(f)

        for equipment in equipments:
            for material in equipment["materials-forge"]:
                if material["url"] not in searched_links:
                    match determine_type(material, mined):
                        case "mining-outcrop":
                            # if mined, ONLY check for mining outcrops, NO quest rewards. IGNORE Seliana Supply Cache
                            loc, rar = get_mined_materials(material)
                            materials_json.append({
                                "name": material["name"],
                                "type": "mining-outcrop",
                                "source": ["Mining Outcrop"],
                                "locales": loc,
                                "rarity": rar,
                                "url": material["url"],
                            })
                        case "carve-quest":
                            mon, que, rar = get_materials_mix(material)
                            if mon and que: # if material has both monster drops and quest rewards, IGNORE quest rewards
                                materials_json.append({
                                    "name": material["name"],
                                    "type": "monster-drop",
                                    "source": mon,
                                    "locales": ["N/A"],
                                    "rarity": rar,
                                    "url": material["url"],
                                })

                            if mon and not que: # if material has only monster drops, use monster drops
                                materials_json.append({
                                    "name": material["name"],
                                    "type": "monster-drop",
                                    "source": mon,
                                    "locales": ["N/A"],
                                    "rarity": rar,
                                    "url": material["url"],
                                })

                            if que and not mon: # if material has only quest rewards, use quest rewards
                                materials_json.append({
                                    "name": material["name"],
                                    "type": "quest-reward",
                                    "source": que,
                                    "locales": ["N/A"],
                                    "rarity": rar,
                                    "url": material["url"],
                                })
                
                searched_links.append(material["url"])
        
            for material in equipment["materials-upgrade"]:
                if material["url"] not in searched_links:
                    match determine_type(material, mined):
                        case "mining-outcrop":
                            # if mined, ONLY check for mining outcrops, NO quest rewards. IGNORE Seliana Supply Cache
                            loc, rar = get_mined_materials(material)
                            materials_json.append({
                                "name": material["name"],
                                "type": "mining-outcrop",
                                "source": ["Mining Outcrop"],
                                "locales": loc,
                                "rarity": rar,
                                "url": material["url"],
                            })
                        case "carve-quest":
                            mon, que, rar = get_materials_mix(material)
                            if mon and que: # if material has both monster drops and quest rewards, IGNORE quest rewards
                                materials_json.append({
                                    "name": material["name"],
                                    "type": "monster-drop",
                                    "source": mon,
                                    "locales": ["N/A"],
                                    "rarity": rar,
                                    "url": material["url"],
                                })

                            if mon and not que: # if material has only monster drops, use monster drops
                                materials_json.append({
                                    "name": material["name"],
                                    "type": "monster-drop",
                                    "source": mon,
                                    "locales": ["N/A"],
                                    "rarity": rar,
                                    "url": material["url"],
                                })

                            if que and not mon: # if material has only quest rewards, use quest rewards
                                materials_json.append({
                                    "name": material["name"],
                                    "type": "quest-reward",
                                    "source": que,
                                    "locales": ["N/A"],
                                    "rarity": rar,
                                    "url": material["url"],
                                })
                
                searched_links.append(material["url"])

    with open('mhw-tools/drop-list/items-list/temp-mats.json', 'w') as g:
        json.dump(materials_json, g, indent=4)

def detailed_materials_scraper():
    # materials scraper

    mined = [
        "Iron Ore",
        "Machalite Ore",
        "Dragonite Ore",
        "Carbalite Ore",
        "Fucium Ore",
        "Eltalite Ore",
        "Meldspar Ore",
        "Earth Crystal",
        "Coral Crystal",
        "Dragonvein Crystal",
        "Spiritvein Crystal",
        "Lightcrystal",
        "Novacrystal",
        "Purecrystal",
        "Firecell Stone",
        "Bathycite Ore",
        "Gracium",
        "Aquacore Ore",
        "Spiritcore Ore",
        "Dreamcore Ore",
        "Dragoncore Ore",
        "Phantomcore Ore",
        "Shadowcore Ore",
    ]

    # if mined, ONLY check for mining outcrops, NO quest rewards. IGNORE Seliana Supply Cache    DONE!
    # if material has both monster drops and quest rewards, IGNORE quest rewards
    # if material has only quest rewards, use quest rewards
    # For all materials, take first two columns of table.

    # Rerun weapon scraper, added new part.

    materials_json = []
    searched_links = []

    with open('mhw-tools/drop-list/items-list/materials.json') as f:
        materials = json.load(f)

        for material in materials:
            sources, rarity = get_material_sources(material)

            materials_json.append({
                "name": material["name"],
                "source": sources,
                "rarity": rarity,
                "url": material["url"]
            })
            
            searched_links.append(material["url"])

    with open('mhw-tools/drop-list/items-list/temp-mats.json', 'w') as g:
        json.dump(materials_json, g, indent=4)

#equipment_scraper()
#materials_scraper()

detailed_materials_scraper()

# TODO for armour:
# when scraping, only check the first layer of <tr> of the table for links. 