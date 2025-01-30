import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# Roblox játék URL-je
game_url = 'https://www.roblox.com/games/10938101313'  # Cseréld le a saját játékod URL-jére!

# A logolás beállítása
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# A szerverek és azok indítási idejének tárolása
servers = {}

# Folyamatosan figyeljük a szerverek állapotát
async def scrape_servers():
    print("[INFO] Beginning extraction")
    browser = await launch(headless=True)  # Fej nélküli mód
    page = await browser.newPage()

    # Nyisd meg a Roblox játék oldalát
    await page.goto(game_url)
    await page.waitForSelector('div.server-list')  # Várakozás a szerverek betöltődésére
    
    # A szerverek listájának lekérése
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')

    # A szerverek keresése (valós 'div' elem id vagy class alapján)
    server_elements = soup.find_all('div', class_='server-class')  # Cseréld le a helyes class-ra!

    current_servers = {}
    
    # Felvesszük az új szervereket és azok indítási idejét
    for server in server_elements:
        server_id = server.get_text()  # Cseréld le egy valós egyedi azonosítóra!
        if server_id not in servers:
            servers[server_id] = datetime.now()  # Mentjük a szerver indításának idejét
            logging.info(f"Új szerver indult: {server_id}, Indulás ideje: {servers[server_id]}")

        # Tároljuk az aktuális szervereket
        current_servers[server_id] = servers.get(server_id)

    # Képernyőre írjuk ki a jelenlegi szerverek állapotát és a logba is
    for server_id, start_time in current_servers.items():
        time_since_start = datetime.now() - start_time
        logging.info(f"Szerver {server_id} - {str(time_since_start)} eltelt idő")
        print(f"Szerver {server_id} - {str(time_since_start)} eltelt idő")

    # Bezárjuk a böngészőt
    await browser.close()

# A kód futtatása
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(scrape_servers())
