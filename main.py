from dotenv import load_dotenv
import requests
import random
import telegram
import os


def download_images(filename, url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(filename, 'wb') as file:
       file.write(response.content)


def get_numbers_comics():
    comics = 'https://xkcd.com/info.0.json'
    response = requests.get(comics)
    response.raise_for_status()
    comic_number_total = response.json()['num']
    return comic_number_total


def get_random_comics(all_number_comics):
    random_comic = random.randint(1, all_number_comics)
    comic_url = f"https://xkcd.com/{random_comic}/info.0.json"
    response = requests.get(comic_url)
    response.raise_for_status()
    comic = response.json()
    img_url = comic['img']
    comment = comic["alt"]
    return img_url, comment
    

def main():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    try:
        bot = telegram.Bot(token=tg_token)
        comics_numbers = get_numbers_comics()
        img_url, comment = get_random_comics(comics_numbers)
        download_images("comic.png", img_url)
        with open("comic.png", 'rb') as f:
            bot.send_photo(chat_id=chat_id, photo=f, caption=comment)
    finally:
        os.remove("comic.png") 


if __name__ == '__main__':
    main()