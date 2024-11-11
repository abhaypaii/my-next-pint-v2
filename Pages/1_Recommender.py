import pandas as pd
import numpy as np
import streamlit as st
import ast

st.title("My Next Pint V2")
st.subheader("Beer recommender using over 9M rows of reviews of over 100K beers ")

df = pd.read_csv("processed_data/embedded_list.csv")
df['features'] = df['features'].apply(lambda x: ast.literal_eval(x))

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def similarity(beer_id, df=df):
  # Assuming you have a DataFrame 'df' with columns 'id', 'features', and 'cluster'
  beer_data = df[df['id'] == beer_id]
  beer_cluster = beer_data['cluster'].values[0]
  beer_features = beer_data['features'].values[0]

  # Filter beers in the same cluster
  cluster_beers = df[df['cluster'] == beer_cluster]

  # Calculate cosine similarity for each beer in the cluster
  similarities = []
  for _, row in cluster_beers.iterrows():
      sim = cosine_similarity(beer_features, row['features'])
      similarities.append((row['id'], sim))

  # Sort by similarity and return top 5
  similarities.sort(key=lambda x: x[1], reverse=True)
  return similarities[1:6]

def display_cards(series):
    with st.container(key = series['beer'], border=True):
        st.subheader(series['beer'].values[0])
        st.caption(series['style'].values[0])
        st.write("ABV: "+str(round(series['abv'].values[0], 3))+" | "+str(round(series['count'].values[0], 3))+" reviews | Availability: "+series["availability"].values[0])
        st.write("Brewed by: "+series['brewery'].values[0]+" | Country of Origin: "+series["country"].values[0])
        st.write("**Reviews:**")
        c1, c2 = st.columns(2)
        c1.write("Overall: "+str(round(series['overall'].values[0], 3)))
        c1.write("Look : "+str(round(series['look'].values[0], 3)))
        c1.write("Smell: "+str(round(series['smell'].values[0], 3)))
        c2.write("Taste: "+str(round(series['taste'].values[0], 3)))
        c2.write("Feel: "+str(round(series['feel'].values[0], 3)))

with st.sidebar:
    options = df.sort_values(by="count", ascending=False)["beer"].values.tolist()
    input = st.selectbox("Choose from over 100K beers",options, index=None, placeholder="Select beer...")
    generate = st.button("Generate")

if generate and input:
    cols = st.columns([1,1.2])
    with cols[0]:
        st.header("Chosen beer:")
        choice = df[df["beer"]==input]
        display_cards(choice)
    with cols[1]:
        st.header("Similar beers:")
        id = df[df['beer'] == input]['id'].values[0]
        similar = similarity(id)
        beer_ids = [sim[0] for sim in similar]
        output = df[df['id'].isin(beer_ids)]

        with st.container(border=True, key="recommendations", height=800):
                for index, row in output.iterrows():
                    row = output[output["beer"]==output.loc[index, "beer"]]
                    display_cards(row)