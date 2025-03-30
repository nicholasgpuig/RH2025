import pylast
import requests
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation






<<<<<<< HEAD
=======
 #This is the api key for the last.fm api, which is giving us our data
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


 #This gives us the tags for the artists and tracks
tags = []
def get_top_tags(track, artist):
     api_key = API_KEY
     url = f"https://ws.audioscrobbler.com/2.0/?method=track.getTopTags&track={track}&artist={artist}&api_key={api_key}&format=json"
    
     response = requests.get(url)
     data = response.json()
  
     if "toptags" in data:
         for tag in data["toptags"]["tag"]:
            
            
             tags.append({tag['name']}) 
     else:
         print("No tags found.")
     return tags



def client(song_name, artist_name):
    client = genai.Client(api_key="AIzaSyDBMkkQEjoGsne6UPhFhoTGF9gexqfwDHc")

    contents = (f"Based off the tags and the song album cover I give you give me the top 3 colors that are associated with this song. Make one 50%, one 30%, one 20%." +

                f" Here are the tags:{tags}. Here is the song {song_name} by {artist_name}. Don't include any analysis just give me a python list with the hexcodes but not in quotes. Put it on one list on one line" )

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            colors = part.text.split("[", 1)[1].split("]", 1)[0]  # Extract content inside brackets
            colors = colors.split(",")  # Split by commas
            colors = [color.strip().replace("'", "").replace('"', '') for color in colors]  # Clean spaces & quotes

            return colors
            
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('gemini-native-image.png')
            image.show()
            return ["0", "0", "0"]  # Return a default value if no text is found




>>>>>>> 422631397da581b70082ffb415e46a3506a53077
# Function to generate a random colormap


def getPlot():
        #This is the api key for the last.fm api, which is giving us our data
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


<<<<<<< HEAD
    #This gives us the tags for the artists and tracks
    tags = []
    def get_top_tags(track, artist):
        api_key = API_KEY
        url = f"https://ws.audioscrobbler.com/2.0/?method=track.getTopTags&track={track}&artist={artist}&api_key={api_key}&format=json"
        
        response = requests.get(url)
        data = response.json()
=======
# Function to update the colormap smoothly
def update(frame):
    global cmap1, cmap2

    # Interpolate between two colormaps
    alpha = (np.sin(frame / 20) + 1) / 2  # Varies between 0 and 1
    blended_colors = [
        (1 - alpha) * np.array(plt.get_cmap(cmap1)(i / 2)) + alpha * np.array(plt.get_cmap(cmap2)(i / 2))
        for i in range(3)
    ]
>>>>>>> 422631397da581b70082ffb415e46a3506a53077
    
        if "toptags" in data:
            for tag in data["toptags"]["tag"]:
                
                
                tags.append({tag['name']}) 
        else:
            print("No tags found.")
        
    song_name = input("Enter the song: ")
    artist_name = input("Enter the band: ")

    get_top_tags(song_name, artist_name)


<<<<<<< HEAD





    client = genai.Client(api_key="AIzaSyDBMkkQEjoGsne6UPhFhoTGF9gexqfwDHc")

    contents = (f"Based off the tags and the song album cover I give you give me the top 5 colors that are associated with this song. Make one 40%, one 25%, one 20%, one 10%, one 5%." +

                f" Here are the tags:{tags}. Here is the song {song_name} by {artist_name}. Don't include any analysis just give me a python list with the hexcodes but not in quotes. Put it on one list on one line" )

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )
    colors = []

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            colors = part.text.split("[", 1)[1].split("]", 1)[0]  # Extract content inside brackets
            colors = colors.split(",")  # Split by commas
            colors = [color.strip().replace("'", "").replace('"', '') for color in colors]  # Clean spaces & quotes

            print(colors)
            
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save('gemini-native-image.png')
            image.show()

    def random_cmap():
        return LinearSegmentedColormap.from_list(
            "random_cmap", 
            [np.random.choice(colors) for _ in range(3)]
        )

        # Create two initial colormaps
    cmap1 = random_cmap()
    cmap2 = random_cmap()
    #  Define the figure and axis
    fig, ax = plt.subplots(figsize=(2.5, 2.5))

    # Initial probability values
    probability = np.linspace(0, 1, 100)
    # Display the initial gradient
    gradient = ax.imshow([probability], aspect="auto", cmap=cmap1, extent=[0, 1, 0, 1])
    ax.axis("off")
    # Function to update the colormap smoothly
    def update(frame):
        global cmap1, cmap2

        # Interpolate between two colormaps
        alpha = (np.sin(frame / 20) + 1) / 2  # Varies between 0 and 1
        blended_colors = [
            (1 - alpha) * np.array(plt.get_cmap(cmap1)(i / 2)) + alpha * np.array(plt.get_cmap(cmap2)(i / 2))
            for i in range(3)
        ]
        
        new_cmap = LinearSegmentedColormap.from_list("blended_cmap", blended_colors)
        
        # Update the colormap
        gradient.set_cmap(new_cmap)

        # Every 50 frames, select a new target colormap
        if frame % 50 == 0:
            cmap1, cmap2 = cmap2, random_cmap()

        return gradient,
    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=False)


=======
def getPlot(colors):
    
#  Define the figure and axis
    fig, ax = plt.subplots()

# Initial probability values
    probability = np.linspace(0, 1, 100)

    # Create two initial colormaps
    cmap1 = random_cmap()
    cmap2 = random_cmap()

    # Display the initial gradient
    gradient = ax.imshow([probability], aspect="auto", cmap=cmap1, extent=[0, 1, 0, 1])
    ax.axis("off")

# Create the animation
    ani = animation.FuncAnimation(fig, update, frames=200, interval=50, blit=False)

>>>>>>> 422631397da581b70082ffb415e46a3506a53077
    return plt