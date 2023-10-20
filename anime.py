import os
import requests
import sys
import re
import subprocess
import time
from bs4 import BeautifulSoup as soap

site = "https://samehadaku.vin"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
tmp = []
quality_index = 00

def play(link, judul):
    global quality_index
    start_time = time.time()
    print(f"Playing {judul}")
    try:
        files_link = []
        quality_videos = []
        
        req = soap(requests.get(link, headers=headers).text, "html.parser")
        get_link = req.find("div", class_="download-eps")
        #print(get_link)
        for kraken_link in get_link.find_all("a", href=True):
            if "https://krakenfiles.com" in kraken_link['href']:
                files_link.append(kraken_link['href'])
        for qu in get_link.find_all("strong"):
            quality_videos.append(qu.text)
        if files_link:
            if quality_index == 00:
                while True:
                    print("Choose you quality Video : ")
                    for i, qu in enumerate(quality_videos, start=1):
                        print(f"{i}. {qu}")
                    select_quality = int(input("Select > "))
                    if 1 <= select_quality <= len(quality_videos):
                        quality_index = select_quality - 1
                        break
                    else:
                        print("Quality you choose not found.")
                        continue
            
            req = requests.get(files_link[quality_index], headers=headers).text
            get_embed = re.search('src="([^"]+)"></iframe>', req).group(1)
            print(f"Playing {judul} with resolution {quality_videos[quality_index]}")
            subprocess.run(f"mpv {get_embed}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elapsed_time = time.time() - start_time
            sys.stdout.write(f"\rTime Spent : {int(elapsed_time)} second")
            sys.stdout.flush()
            time.sleep(1)
        else:
            print("[ERROR] This episode not contain krakenfiles.com. cannot stream\nExiting..")
            sys.exit(0)
    except Exception as e:
        print(f"Error : {e}")
    finally:
        sys.stdout.write("\n")

def search_anime():
    #req = ""
    while True:
        anime_name = input("Type anime name > ")
        print(f"Searching : {anime_name}")
        req = requests.get(site+f"/?s={anime_name}", headers=headers).text
        #open('source_code.txt', 'w+', encoding='utf8').write(req)
        if '<h3 class="notfound">' in req:
            print(f"Sadly. Anime {anime_name} not found.")
            tryagain = str(input("Search anime again? (y/n) "))[0]
            if tryagain == 'y':
                continue
        break
    animename = []
    anime_link = []
    bs = soap(req, "html.parser")
    for judul in bs.find_all("div", class_="data"):
        animename.append(judul.h2.text)
    for link in bs.find_all("div", class_="animposx"):
        for lnk in link.find_all("a", href=True):
            anime_link.append(lnk['href'])
    print("\nAnime List With Keyword {} : ".format(anime_name))
    for i, name in enumerate(animename, start=1):
        print(f"{i}. {name}")
    while True:
        select = int(input("Select > "))
        if 1 <= select <= len(anime_link):
            req = soap(requests.get(anime_link[select - 1], headers=headers).text, "html.parser")
            break
        else:
            print("Sorry Anime Not Found.")
    genre = ""
    print("<============== INFORMATION ABOUT ANIME ==============>")
    sinopsis = req.find("div", class_="desc").p.text
    print("[+] SINOPSIS : ", sinopsis)
    
    for genr in req.find_all("div", class_="genre-info"):
        for gen in genr.find_all("a"):
            genre += f"{gen.text} "
    print("[+] GENRE :", genre)
    animename = []
    anime_link = []
    for i in req.find_all("span", class_="lchx"):
        for j in i.find_all("a", href=True):
            animename.append(i.text)
            anime_link.append(j['href'])
    animename = list(reversed(animename))
    anime_link = list(reversed(anime_link))
    print("\nAnime Episode : ")
    for i, name in enumerate(animename, start=1):
        print(f"{i}. {name}")
    while True:
        print("[HELP] For watch beetwen episode using '-'. Example : 1-5 (option 1 to 5)")
        select = input("Select Episode > ")
        if '-' in select:
            begin = int(select.split("-")[0])
            end = int(select.split("-")[1])
            if begin > end:
                print("Error in episode format.\nThe end episode cannot be smaller.")
                continue
        else:
            begin = int(select)
            end = 0
        if 1 <= begin <= len(anime_link):
            break
        else:
            print("Episode not found.")
            continue
        break
    if end != 0:
        for i in range(begin, end+1):
            animlink = anime_link[i - 1]
            animjudul = animename[i - 1]
            play(animlink, animjudul)
    else:
        animlink = anime_link[begin - 1]
        animjudul = animename[begin - 1]
        #print(anim_link)
        play(animlink, animjudul)
        #print(judul)
    

    #print(req)
    
def check_mpv():
    try:
        subprocess.run(["mpv", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        pass
    except:
        print("[ERROR] MPV not found in you system.\n\nFor installation check site : https://mpv.io/installation ")
        sys.exit(0)
    
def main():
    os.system('cls') if os.name == 'nt' else os.system('clear')
    banner = """
    ____                 __           __________________
   / __/___  ____  _____/ /____  ____<  /__  /__  /__  /
  / /_/ __ \/ __ \/ ___/ __/ _ \/ ___/ / /_ < /_ <  / / 
 / __/ /_/ / /_/ (__  ) /_/  __/ /  / /___/ /__/ / / /  
/_/  \____/\____/____/\__/\___/_/  /_//____/____/ /_/   
                                                        
Anime Streaming And Downloader by github.com/fooster1337
Website using : https://samehadaku.vin
"""
    print(banner)
    check_mpv()
    try:
        req = requests.get("https://45.12.2.28", headers=headers, timeout=10).status_code
        if req != 200:
            print("Something error with site. please check!")
            sys.exit(0)
        search_anime()
    except Exception as e:
        print(f"Error when connecting to site!.\nError : {e}")
if __name__ == '__main__':
    main()
