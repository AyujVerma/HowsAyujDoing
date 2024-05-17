# Moodify
**Website:** https://ayuj.onrender.com/

**Winter 2023:** 
I wanted to learn more backend development. Combining my interests in music, I created a Flask application that uses Spotify RESTful APIs to retrieve the current track on my Spotify player. I displayed the song's name, artist(s), album cover, and randomly generated a mood and "background color" (more on the last two later). I also handled podcast episodes and advertisements (#broke). The application polls Spotify's APIs every 15 seconds, and if nothing is actively playing, then I also handle that as well. Feeling satisfied with what I had learned, I hosted my project on Render and thought that was it...

**Summer 2024:** 
After coming home, I was already bored at home. Fueled by my interests in NLP and ML, I wanted to classify a song's mood by its lyrics and audio features instead of just randomly assigning it a mood.

**The Process:**

**1) Data Collection:**
   I used Spotify's "Get Audio Features" API to get a wide variety of traits include "danceability", "energy", "loudness", and more. Getting lyrics was much, much more difficult. Spotify doesn't provide the lyrics to its songs, so I had to use the Genius API. However, Genius doesn't give the lyrics either; it simply just returns the URL to the song's webpage. I had to use Python's Beautiful Soup to scrape the lyrics from the HTML, which didn't always work (more on that later).
   In terms of the songs, I looked at official Spotify playlists under their "mood" category and chose playlists from under the "If you're feeling happy" and "When you are feeling down" categories. I roughly had 980 songs from both, which was almost 2000 songs.
   2000 songs was a lot, so I kept on getting rate limited from both Spotify and Genius. To get around this, I added exponential retries, which would add a progressively add a larger and larger delay if a request failed. Collecting the audio features took one night and scraping the lyrics took another night.
   
**2) Data Pre-Processing Part 1:**
   After collecting data, I thought everything was smooth sailing from here... I couldn't be more wrong. I didn't really look at the playlists I was collecting data from, so I had to remove a bunch of non-english songs, instrumentals, and "Tik Tok" songs. Note: in this generation where "popular sounds" are being made everyday, Genius sometime hasn't curated the lyrics or even know who the artist is. For songs that did exist, especially remasters, Genius would scrape some random thing like a chapter of Harper Lee's *To Kill a Mockingbird*, so I would manually have to overwrite the song's lyrics. Ensuring all songs were valid and their lyrics weren't garbage took a whole day. In the end, I had 1698 songs to work with.
   For the 90% of songs that were scraped properly, there were still issues. Beautiful Soup scraped metadata tags that Genius puts on all their songs like the number of contributors, the available languages the song can be translated in, and even the ads on the website. After removing these, all the songs were ready to be processed, so they can be used in NLP models.
   
**3) Data Pre-Processing Part 2:**
   NLP can't handle punctuation well, so I have to remove it. Replacing most punctuation is easy, but apostrophes have a lot of issues. Apostrophes are used to combine two words or shorten a word.
   
   a) Here is where I quickly realized how complicated the English langauge is: contractions. The word "ain't" has all these meanings and it ain't pretty folks: "am not", "are not", "is not", "has not", and "have not." I made a dictionary to simply replace a contraction with its expanded form; it is not the most accurate solution, but it is a good enough heuristic.
   
   b) "We gon' have a good time" would become "We gon (?) have a good time" without converting all postfixes of *-n'* to *-ing*.
   
After removing punctuation, I also removed swear words because they have multiple meanings based on context. Different genres use them differently and some have more "unique" ones. As a result, it is easier to get rid of them altogether.

I also removed any choruses/background voices that were scraped. These were found in brackets and parentheses.
I then tokenized the cleaned lyrics and removed stop words, which are words that provide none to little sematic value.
Finally, I lemmatized each token, which involves tagging each token with it's part of speech and then reducing it to its lemma (root). For example, "running" becomes "run." This is better than stemming because stemming would take "stories" and reduce it to "stori" while lemmatization reduces it properly to "story."

**4) Model Training:**
   Non-Lyrical:
   I first wanted to see how good audio features alone are. My best classifiers were a neural network and a random forests; both had accuracies around 78%.

   Lyrical (Trained on Google Colab):
   When using lyrics, a computer can only understand numbers, so I took each list of tokens and converted it to a vector embedding. I had two models:
   
     1. Gensim's Word2Vec model.
     2. Hugging Face's Roberta model.
     
When using the Word2Vec embeddings, I also added the TF-IDF as a feature set with the audio features and got an 80% accuracy on both a neural network and a random forest. The TF-IDF helps show how relevant a word is among an entire corpus (text). In this case, each word in a song was compared to the lyrics of ALL the songs. I restricted the TF-IDF feature set to only include the vectorizations of the top 84 words because there was a noticeable drop-off from the 84th most frequent word and the 85th most frequent word.

When using the Roberta model's encodings with a neural network, my best tests gave me 81% accuracy. However, this model used up all my free GPU resources on Google Colab, and running this on a CPU took impossibly long.

**Conclusions:**
My website is currently up and running! I enjoyed being able to combine my interests in music with NLP, ML, and full-stack development!

**How Can I Join?**
1. Clone the project and create a .env file.
2. Create a Spotify developer account and make a project.
3. In the .env file, input your "SPOTIFY_ACCESS_TOKEN", "SPOTIFY_REFRESH_TOKEN", "SPOTIFY_CLIENT_ID", and "SPOTIFY_CLIENT_SECRET."
4. In App.js, fetch responses from your local host instead of my website.
5. Now you can run the app locally!
