import praw
import os
import random
from gtts import gTTS
from moviepy.editor import  AudioFileClip,vfx
import time


import json


def Scrapper ():
    start = time.time()

    def unique_filename(filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filename):
            filename = f"{base}_{counter}{ext}"
            counter += 1
        return filename

    def word_count(text):
        return len(text.split())


    # Set up Reddit API credentials
    f = open("API.json")
    jsondata = json.load(f)

    client_id = jsondata["client_id"] 
    client_secret =  jsondata["client_secret"] 
    user_agent =  jsondata["user_agent"]
    f.close()

    # Initialize praw instance
    reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent)

    # Set up the target subreddit and output file
    subreddit_name = 'AskReddit'
    output_file = 'temp_files/askreddit.txt'
    output_file = unique_filename(output_file)
    
    # Fetch a random top post from the "all time" filter
    subreddit = reddit.subreddit(subreddit_name)
    top_posts_alltime = list(subreddit.top('all', limit=20))
    random_top_post = random.choice(top_posts_alltime)


    end = time.time()
    print(f"Time taken: {(end-start)*10**3/1000:.02f} seconds")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{random_top_post.title}\n")
        print(random_top_post.score)

        # Fetch post comments
        random_top_post.comments.replace_more(limit=0)

        # Find the most popular comment with at least 50 words
        top_comment = None
        for comment in random_top_post.comments:
            if word_count(comment.body) >= 100:
                if top_comment is None or comment.score > top_comment.score:
                    top_comment = comment

        if top_comment:
            f.write(f"{top_comment.author}: {top_comment.body}\n\n")
            

        else:
            print("This post has no comments that meet the criteria; searching for new post")
            Scrapper()


    print(f"Data saved in {output_file}.")
    return output_file

def tts_converter(prev_output):
    # Set input text file and output mp3 file
    input_file = prev_output
    output_file = 'temp_files/askreddit.mp3'

    # Read the content of the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Create a gTTS object and save the output as an MP3 file
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("temp_files/temp.mp3")
    audio = AudioFileClip("temp_files/temp.mp3").fx(vfx.speedx,1.2).write_audiofile(output_file)
    

    print(f"Audio saved in {output_file}.")





print("Searching for popular posts")


tts_converter(Scrapper())




print("Converting file to mp3")

