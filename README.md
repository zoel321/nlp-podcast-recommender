## NLP Project Write-Up

**Abstract**

The goal of this project was to create a content-based recommender for mental health podcasts. Descriptions for 350 Spotify podcast shows along with their episode descriptions were retrieved then cleaned and preprocessed using various NLP packages/tools. The topic models derived from the text data for podcasts and episodes were then used to develop the recommendation system. The user will receive a podcast or episode recommendation based on their input. 

**Design**

I focused on mental health podcasts for this project because it is a specific topic (narrows down scope) yet also contains a wide variety of subtopics. Target users may have an idea of what topic interests them but have trouble finding another related episode manually due to the millions of episodes that exist in the Spotify podcast catalog. The description data for podcasts and episodes were cleaned and preprocessed/tokenized and then vectorized to matrices of token counts, before undergoing dimensionality reduction to find the topics. The quality of the topics was determined subjectively using personal observation/judgment. The document-topic matrices for podcasts and episodes were then used to build the content-based recommendation system. This was done using cosine similarity as the distance metric.

 

**Data**

This project’s data was retrieved using Spotipy, a Python library for the Spotify Web API.

The initial podcast dataset contained 350 shows, along with their descriptions and Spotify show ID. After removing duplicates, this resulted in 344 shows. The initial episode dataset contained 20745 episodes, along with their descriptions, podcast name, Spotify episode ID, and published date. After removing duplicates, this resulted in 18115 episodes. The text preprocessing and topic modeling steps were performed separately for these datasets before incorporating the results into the recommendation system. 

**Algorithms**

Preprocessing: 

I used Regex to remove digits, punctuation, symbols, and extraneous non-English characters. The words were then converted to lowercase and lemmatized. Stop words (default and custom) were incorporated during the vectorization process. For the episodes, I used spaCy to locate proper nouns, so that I could later tokenize them as compound words (such as combining first and last name, for a guest interviewed on a podcast). For the podcasts, I grouped some frequent compound terms (e.g., personal development, mental health, social media).

 

Vectorization and Topic Modeling:

I tried Non-Negative Matrix Factorization and Latent Semantic Allocation combinations with CV and TF-IDF vectorizers. Granularity was ultimately prioritized over interpretability. For episodes, I used the TF-IDF vectorizer with LSA, which resulted in 15 topics. For podcasts, I used the TF-IDF vectorizer with NMF, which resulted in 10 topics (overall interpretable: story, relationship, fitness, women, school, weight loss, art, therapy).

 

Recommendation system:

A content-based recommendation system was built using cosine similarity as the distance metric, to find the most similar episodes and podcasts within their respective document-topic matrices. The user can choose if they want an episode or podcast recommendation. If the user wants to find a similar episode, they can also specify if they want a recommendation from the same podcast, different podcast, or any. If from a different podcast, the cosine similarity scores from the podcast document-topic matrix and the episode document-topic matrix are combined to find the lowest (closest) score.  

 

**Tools**

-  Spotipy for data retrieval 
- Pandas for data analysis/cleaning
- NLTK, spaCy for text preprocessing
- Scikit-learn for vectorization, dimensionality reduction/topic modeling

**Communication**

The data and code are in this repo, along with the final slides. The recommender was deployed to Streamlit and can be accessed here: https://share.streamlit.io/zoel321/nlp-podcast-recommender/main/Spotify-Podcast-Recommender-Streamlit.py







