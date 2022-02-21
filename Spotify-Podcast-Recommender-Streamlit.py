
#import functions

import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from PIL import Image

st.title("Mental Health Podcast Recommender")
image = Image.open('app_pic.jpeg')
st.image(image, caption='Source: https://www.thedowneypatriot.com/articles/taking-care-of-your-mental-health-more-important-than-ever')
#get dataframes


podcast_names_df= pd.read_pickle('unique_podcastnames.pkl')

episode_df = pd.read_pickle('mh_podcasts_unique.pkl')

ep_doc_topic_df = pd.read_pickle('doc_topic2.pkl')

podcast_doc_topic_df = pd.read_pickle('podcast_doc_topic.pkl')

#clean episode_df a little for display
episode_df_display = episode_df.drop(columns=['index', 'Ep_id', 'Desc_Processed'])
episode_df_display.rename(columns={"Ep_desc": "Episode Description", "Ep_date": "Episode Date", "Ep_name": "Episode_Name"}, inplace=True)

st.subheader("Here's the list of Spotify podcasts and their episodes:")
st.dataframe(episode_df_display)

podcast_names = episode_df['Podcast_Name'].drop_duplicates()
specify_podcast = st.selectbox('Filter podcast:', podcast_names.sort_values())
episodes = episode_df_display[episode_df_display["Podcast_Name"] == specify_podcast]
st.write(episodes)

# Recommender


def recommend_podcast(podcast_name, pod_df, pod_doc_topic):
    podcast_row = pod_df[pod_df['Podcast_Name'] == podcast_name]
    podcast_index = podcast_row.index[0]
    st.write('Given: ', podcast_name)
    st.write('Description: ', pod_df.iloc[podcast_index]['Podcast_Description'])
    dist = pairwise_distances(np.array(pod_doc_topic.iloc[podcast_index]).reshape(1,-1), pod_doc_topic, metric = 'cosine')
    rec_pod_index = dist.argsort()[0][1]
    rec_pod_name = pod_df.iloc[rec_pod_index]['Podcast_Name']
    st.subheader("Recommendation")
    st.write('Recommended Podcast: ', rec_pod_name)
    st.write('Description: ', pod_df.iloc[rec_pod_index]['Podcast_Description'])
    #return rec_pod_name

@st.cache
def recommend_episode(ep_index, ep_df, ep_doc_topic, shortened_doc_topic=None):
    if shortened_doc_topic is not None:
        dist = pairwise_distances(np.array(ep_doc_topic.iloc[ep_index]).reshape(1,-1), shortened_doc_topic, metric = 'cosine')
        rec_ep_index = dist.argsort()[0][1]
        rec_ep_name = ep_df.reset_index().iloc[rec_ep_index]['Ep_name']
    else: 
        dist = pairwise_distances(np.array(ep_doc_topic.iloc[ep_index]).reshape(1,-1), ep_doc_topic, metric = 'cosine')
        rec_ep_index = dist.argsort()[0][1]
        rec_ep_name = ep_df.iloc[rec_ep_index]['Ep_name']
    return rec_ep_index, rec_ep_name 

@st.cache
def rec_ep_diff_podcast(ep_index, pod_index, ep_df, ep_doc_topic, pod_doc_topic):
    pod_dist = pairwise_distances(np.array(pod_doc_topic.iloc[pod_index]).reshape(1,-1), pod_doc_topic, metric = 'cosine')
    ep_dist =  pairwise_distances(np.array(ep_doc_topic.iloc[ep_index]).reshape(1,-1), ep_doc_topic, metric = 'cosine')
    #making dataframe to organize summed cosine similarity
    start_df = ep_df['Podcast_Name'].to_frame()
    start_df['Pod_Index'] = start_df['Podcast_Name'].map(pod_dict).str[0]
    ep_cos_df = pd.DataFrame(ep_dist.reshape(-1,1), columns=['Cosine Similarity for Episodes'])
    full = start_df.join(ep_cos_df)
    full['Cosine Similarity for Podcasts']= full['Pod_Index'].apply(lambda x: pod_dist[0][x])
    full['Summed Similarity'] = full["Cosine Similarity for Episodes"] + full["Cosine Similarity for Podcasts"]
    #find row for smallest summed similarity, excluding rows with same podcast name
    rec_ep_index = full[full['Pod_Index']!= pod_index].sort_values(by=['Summed Similarity']).index[0]
    return rec_ep_index
    


#dictionary of podcast names to indices
pod_dict = podcast_names_df.groupby('Podcast_Name').indices



##for Different podcast: this does not filter first, but takes everything (both doc-topics) as whole 

def recommender2(ep_index, ep_df, pod_df, ep_doc_topic, pod_doc_topic, podcast_choice):
    episode_name = ep_df.iloc[ep_index]['Ep_name']
    st.subheader("Episode You Chose:")
    st.write('Episode Name: ', episode_name)
    st.write('Episode Date: ', ep_df.iloc[ep_index]['Ep_date'])
    #ep_row = ep_df[ep_df['Ep_Name'] == episode_name]
    #ep_index = ep_row.index[0]
    podcast_name = ep_df.iloc[ep_index]['Podcast_Name']
    st.write('From podcast: ', podcast_name)
    st.write('Description: ', ep_df.iloc[ep_index]['Ep_desc'])
    if podcast_choice == 'Different':
        podcast_index = pod_df[pod_df["Podcast_Name"]== podcast_name].index[0]
        rec_ep_index = rec_ep_diff_podcast(ep_index, podcast_index, ep_df, ep_doc_topic, pod_doc_topic)
        rec_ep_name = ep_df.iloc[rec_ep_index]['Ep_name']
    if podcast_choice == 'Same':
        limited_indices = ep_df.index[ep_df['Podcast_Name'] == podcast_name].tolist()
        limited_ep_df = ep_df.iloc[limited_indices]
        limited_doc_topic = ep_doc_topic.iloc[limited_indices]
        rec_ep_index, _ = recommend_episode(ep_index, limited_ep_df, ep_doc_topic, shortened_doc_topic= limited_doc_topic)
        #updating these because returned indices are from shortened array
        rec_ep_name = limited_ep_df.reset_index().iloc[rec_ep_index]['Ep_name']
        rec_ep_index = limited_ep_df.reset_index().iloc[rec_ep_index]['level_0']
    if podcast_choice == 'Any':
        rec_ep_index, rec_ep_name = recommend_episode(ep_index, ep_df, ep_doc_topic)
    st.subheader("Recommendation")
    st.write('Recommended episode: ', rec_ep_name)
    rec_ep_info = ep_df.iloc[rec_ep_index]
    st.write('From podcast: ', rec_ep_info['Podcast_Name'])
    st.write('Date: ', rec_ep_info['Ep_date'])
    st.write('Description: ', rec_ep_info['Ep_desc'])
        



# Ask user for input

#st.subheader('Tell Me...')
st.markdown('## Tell Me... :eyes:')
rec_type = st.radio(('Want a show recommendation or episode recommendation?'),
                    ('Podcast', 'Episode'))


#if episode 
if rec_type == 'Episode':
    
    given_ep = st.text_input("What episode number? (range 0-18114)")
    st.write('The episode number you chose is: ',given_ep)
    
    
    podcast_choice = st.selectbox(
         'From same podcast, different podcast, or any (closest match)?',
         ('Same', 'Different', 'Any'))
    
    st.write('You selected:', podcast_choice)
    
    if st.button('Recommend another episode!'):
        st.markdown('## Results:headphones:')
        try:
            
            ans = recommender2(int(given_ep), episode_df, podcast_names_df, ep_doc_topic_df, podcast_doc_topic_df, podcast_choice)
            st.write(ans)
        except ValueError:
            st.write('Please enter episode number above')

#if podcast
elif rec_type == 'Podcast':
    pod_choice = st.selectbox('Your podcast:', podcast_names.sort_values())
    st.write('You selected:', pod_choice)
    if st.button('Recommend another podcast!'):
        st.markdown('## Results :headphones:')
        recommend_podcast(pod_choice, podcast_names_df, podcast_doc_topic_df)
        
