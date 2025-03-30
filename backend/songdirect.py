import pylast
import requests
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import re


def get_colors():
    song_colors1 = input("What's the first color you're feeling today?: ")
    song_colors2 = input("What's the second color you're feeling today?: ")
    song_colors3 = input("What's the third color you're feeling today?: ")
    song_color_list = [song_colors1,song_colors2,song_colors3]
    song_color_list = [song_colors1]
    return song_color_list

ask_for_colors = get_colors()


def generate_tags(ask_for_colors):
    client = genai.Client(api_key="AIzaSyDBMkkQEjoGsne6UPhFhoTGF9gexqfwDHc")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"Based on the colors provided, generate only 1 tag for a song that would be closely associated. Here are the colors {ask_for_colors}. Make it into a Python list."]
    )

    response_text = response.text.strip()
    
   
    
    # Extract the tag safely
    match = re.search(r"\[(.*?)\]", response_text)  # Find content inside brackets
    if match:
        tag = match.group(1).split(",")[0].strip().replace("'", "").replace('"', '')  # Extract first tag
        
        return tag
    else:
        print("No tag found in AI response.")
        return None


def tag_get_top_tracks(tag):
        API_KEY = "697b4d8866099c759ecc37c658901f34"  
        API_SECRET = "148506689d9d6a7b4fff1edfe04137e1"


        username = "JaxPet"
        password_hash = pylast.md5("Ballin123!")

        network = pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_SECRET,
            username=username,
            password_hash=password_hash,
        )

        url = f"http://ws.audioscrobbler.com/2.0/?method=tag.getTopTracks&tag={tag}&api_key={API_KEY}&format=json"
        
        response = requests.get(url)
        data = response.json()
        tracks_get = ""
        if "tracks" in data and "track" in data["tracks"]:
            top_tracks = [(track["name"], track["artist"]["name"]) for track in data["tracks"]["track"]]
            for i, (track, artist) in enumerate(top_tracks[:1], 1):  # Display top  track
                tracks_get = f"{i}. {track} - {artist}"
        else:
            tracks_get = "No tracks found or an error occurred."
    
        return tracks_get


tag = generate_tags(ask_for_colors)

if tag:
    print(f"Generated Tag: {tag}")  # Debugging step
    track = tag_get_top_tracks(tag)
    print(track)
else:
    print("No valid tag generated.")

track = tag_get_top_tracks(tag)

        
