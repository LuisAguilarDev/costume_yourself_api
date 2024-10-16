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
    "Vampire king": "Creative high-collared, black satin vest with silver buttons and elegant brocade patterns. Underneath, a flowing white silk shirt with ruffled sleeves, adding a timeless and aristocratic vibe. His black leather pants are sleek, fitting tightly to emphasize his agility and power.",
    "Gladiator": "Creative Armor, sandals, and a sword",
    "Zombie": "Creative Zombie dirty and torn clothes rusted",
    "Samurai": "Creative Kimono, sword, and samurai helmet",
    "Werewolf": "Creative Fur, claws, and wolf mask",
    "Wizard": "Creative Robe, wand, and pointed hat like Merlin or Harry Potter",
    "Witch": "Creative Pointed hat, broomstick, and dark dress",
    "Fairy": "Creative Wings, tiara, and a wand",
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
    "Mummy queen": "Creative Mummy Female Bandages wrapped around the body, ancient Egyptian look"
  }
dictBackTheme = {
    "Pirate": "Pirate Era the Golden Age of Piracy",
    "Knight": "Medieval Times",
    "Cowboy": "Wild West",
    "Superhero": "Modern Heroic Era",
    "Vampire king": "Victorian Gothic",
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
    "Mummy queen": "Ancient Egypt"
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

    BG=f"{theme} setting Maintain the central elements of the original photo put lighting and surrounding details to match the {theme} Incorporate specific elements or objects that are iconic for this theme Ensure that the colors mood and textures reflect the {theme} atmosphere while keeping the photo main focus intact"

    fixed_url_bg=encode_spaces(BG)
    bgreplace = f"e_gen_background_replace:prompt_an_{fixed_url_bg}"

    "Replace Clothes"
    clothes= dictBackDescription[costume]
    encoded_url=encode_spaces(clothes)
    clothes_replace=f"e_gen_replace:from_all_clothes;to_{encoded_url}"
    new_url_full_transform_url = f"https://res.cloudinary.com/desdbp97s/image/upload/{clothes_replace}/{bgreplace}/{match.group(1)}.jpg"
    file3=get_image_file(new_url_full_transform_url)
    return get_image_file_base64(file3)
