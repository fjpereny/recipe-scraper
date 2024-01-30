
import os
import sys
import glob
import requests
from PIL import Image
from bs4 import BeautifulSoup, ResultSet


def get_soup(url: str) -> BeautifulSoup:
    req = requests.get(url)
    return BeautifulSoup(req.content, "html.parser")


def get_title(soup: BeautifulSoup) -> str:
    h1 = soup.find_all("h1")[0]
    title = h1.get_text()
    return title


def remove_buttons(soup: BeautifulSoup):
    btns = soup.find_all("button")
    for btn in btns:
        btn.decompose()


def find_recipe(soup: BeautifulSoup) -> BeautifulSoup:
    ingredients = soup.find_all("h2", string="Ingredients")[0]
    recipe = ingredients.parent.parent.parent
    remove_buttons(recipe)
    return recipe


def find_imgs(soup: BeautifulSoup) -> ResultSet:
    imgs = soup.find_all("img", {"decoding": "async", "data-nimg": "1"})
    return imgs 


def run():
    # Recipe Scraping
    url = sys.argv[1]
    print(f"Scraping recipe from <{url}>")
    soup = get_soup(url)
    title = get_title(soup) 
    recipe = find_recipe(soup).prettify()
    print("Recipe scraping complete!")

    # Image Scraping
    imgs = find_imgs(soup)
    os.mkdir(f"{title}")
    img_n = 0
    for img in imgs:
        img_n += 1
        img_url = img['src']
        image = Image.open(requests.get(img_url, stream=True).raw)
        image.save(f"{title}/{img_n}.jpg")
    print("Image scraping complete!")

    # HTML Generation
    file_path = f"{title}.html"
    with open(file_path, "w") as file:
        file.write(f"<div style=\"padding: 25px;\" >")
        file.write(f"<h1 style=\"font-family: sans-serif\">{title}</h1>")
        file.write(recipe)
        g = glob.glob(f"{title}/*.jpg")
        for img in g:
            file.write(f"<div><img src=\"{img}\" style=\"padding: 25px;\" /></div>\n")
        file.write("</div>")
        file.close()

    print("Finished!")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run()
    else:
        print("Usage: python delish_com_scraper.py <url>") 
