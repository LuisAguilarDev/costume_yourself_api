import cloudinary
import re
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from config import Settings
from werkzeug.datastructures import FileStorage
import requests
from io import BytesIO
import base64
import requests
from io import BytesIO
import logging
import aiohttp
import asyncio

cloudinary.config(cloud_name = Settings.CLOUD_NAME_CLOUDINARY,
                  api_key = Settings.API_KEY_CLOUDINARY,
                  api_secret = Settings.API_SECRET_CLOUDINARY,
                  secure=True)


def encode_spaces(url):
    return url.replace(' ', '_').replace('.','').replace(',','')

dictBackDescription = {
    "Pirate": "Creative Pirate costume hat sword",
    "Knight": "Creative Knight costume Armor, shield, and sword",
    "Cowboy": "Creative Cowboy hat, boots, and bandana",
    "Superhero": "Creative Superhero Cape, mask, and emblem like Superman or Batman",
    "Vampire king": "A_high_collared black satin vest with silver buttons and brocade patterns, paired with a white silk shirt with ruffled sleeves and sleek black leather pants_creating an elegant and powerful look",
    "Gladiator": "Creative Armor, sandals, and a sword",
    "Zombie": "Creative Zombie dirty and torn clothes rusted",
    "Samurai": "Creative Kimono, sword, and samurai helmet",
    "Werewolf": "Creative Fur, claws, and wolf mask",
    "Wizard": "Creative Robe, wand, and pointed hat like Merlin or Harry Potter",
    "Witch": "Creative Pointed hat, broomstick, and dark dress",
    "Fairy": "creative_fairy_costume_wings_tiara_and_wand",
    "Princess": " Creative Gown, tiara, and jewelry like Cinderella",
    "Mermaid": "Creative Tail, seashells, and flowing hair",
    "Catwoman": "Creative Black bodysuit, cat ears, and mask",
    "Flapper": "Creative Fringe dress, feathered headband, and long gloves 1920s style",
    "Greek Goddess": "Creative Greek Goddess Flowing toga, gold accessories, and sandals",
    "Zombie Bride": "Creative Zombie Bride Torn wedding dress, pale makeup, and veil",
    "Steampunk Adventurer": "Creative Steampunk Adventurer Corset, goggles, and gear-themed accessories",
    "Skeleton": "Creative SkeletonFull-body skeleton suit, face paint",
    "Clown": "Creative Clow costume Colorful wig, oversized shoes, and makeup",
    "Ghost": "Creative Ghost White sheet or tattered clothing with pale makeup",
    "Alien": "Creative Alien Metallic suit, antenna headband, and space elements",
    "Angel": "Creative Angel White robes, halo, and wings",
    "Devil": "Creative Devil Red outfit, horns, and a pitchfork",
    "Astronaut": "Creative Astronaut Space suit, helmet, and gloves",
    "Robot": "Creative Robot Metallic grey kind of exoskeleton, boxy shapes, and LED lights",
    "Vampire Queen": "Creative Vampire Cape, fangs, and dark clothing",
    "Mummy King": "Creative Mummy Male Bandages wrapped around the body, ancient Egyptian look",
    "Mummy Queen": "Creative Mummy Female Bandages wrapped around the body, ancient Egyptian look"
  }
dictBackTheme = {
    "Pirate": "Pirate Era the Golden Age of Piracy",
    "Knight": "Medieval Times",
    "Cowboy": "Wild West",
    "Superhero": "Modern Heroic Era",
    "Vampire king": "Victorian Gothic",
    "Vampire Queen": "Victorian Gothic",
    "Gladiator": "Ancient Rome",
    "Zombie": "Post-Apocalyptic",
    "Samurai": "Feudal Japan",
    "Werewolf": "Medieval Fantasy",
    "Wizard": "Medieval Fantasy",
    "Witch": "Witchcraft Era",
    "Fairy": "Mythical Forest",
    "Princess": "Fairy Tale Kingdom",
    "Mermaid": "Underwater Kingdom",
    "Catwoman": "Modern Urban",
    "Flapper": "Roaring 1920s glamorous Jazz Age",
    "Greek Goddess": "Ancient Greece",
    "Zombie Bride": "Post-Apocalyptic",
    "Steampunk Adventurer": "Steampunk Era",
    "Skeleton": "Day of the Dead",
    "Clown": "Circus Era",
    "Ghost": "Haunted Era",
    "Alien": "Space Age",
    "Angel": "Heavenly Realm",
    "Devil": "Underworld",
    "Astronaut": "Space",
    "Robot": "Futuristic Era",
    "Mummy King": "Ancient Egypt",
    "Mummy Queen": "Ancient Egypt"
}

def get_image_file(url):
    response = requests.get(url)
    print(response,url)
    if response.status_code == 200:
        image_file = BytesIO(response.content)
        return image_file
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        return None
async def fire_and_forget_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # We don't await or process the response
            print(f"Fire-and-forget request to {url} sent.")
            # This will not wait for the response or process it
  
# async def get_image_file(url):
#     timeout = aiohttp.ClientTimeout(total=6000)
#     async with aiohttp.ClientSession(timeout=timeout) as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 image_content = await response.read()
#                 image_file = BytesIO(image_content)
#                 return image_file
#             else:
#                 print(f"Failed to retrieve image. Status code: {response.status}")
#                 return None
    
def get_image_file_base64(image_file):
        if image_file is None:
            raise ValueError("No image file provided")
        encoded_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
        return encoded_image

def transform(file:FileStorage,costume:str):
    #Upload base img
    response=cloudinary.uploader.upload(file)
    match = re.search(r'/upload/[^/]+/([^\.]+)\.', response["secure_url"])


    #Replace BackGround
    theme=dictBackTheme[costume]

    BG=f"{theme}_put_lighting_and_surrounding_details_to_match_the_{theme}_Incorporate_specific_elements_or_objects_that_are_iconic_for_this_{theme}_Ensure_that_the_colors_mood_and_textures_reflect_the_{theme}_atmosphere"

    fixed_url_bg=encode_spaces(BG)
    bgreplace = f"e_gen_background_replace:prompt_an_{fixed_url_bg}"

    "Replace Clothes"
    clothes= dictBackDescription[costume]
    encoded_url=encode_spaces(clothes)
    clothes_replace=f"e_gen_replace:from_all_clothes;to_{encoded_url}"
    new_url_full_transform_url = f"https://res.cloudinary.com/desdbp97s/image/upload/{bgreplace}/{clothes_replace}/{match.group(1)}.jpg"
    print("url",new_url_full_transform_url)
    logging.basicConfig(level=logging.INFO)
    logging.info(new_url_full_transform_url)
    file3=get_image_file(new_url_full_transform_url)
    return get_image_file_base64(file3)
