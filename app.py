import streamlit as st
from joblib import load
from sklearn.metrics.pairwise import cosine_similarity


# Load Saved Files

anime = load("anime.pkl")
tfidf = load("tfidf.pkl")

# Regenerate Feature Matrix

matrix = tfidf.transform(anime['features'])

# Regenerate Similarity Matrix

similarity = cosine_similarity(matrix)

st.set_page_config(
    page_title="Anime Recommendation System",
    layout="wide"
)

st.markdown(""" <style> .stApp{ background: linear-gradient( 135deg, #FFE6F0, #243B55 ); } </style> """, unsafe_allow_html=True)



# Create Index

indices = dict(
    zip(
        anime["name"],
        anime.index
    )
)

# Recommendation Function

def recommend(anime_name):

    if anime_name not in indices:
        return None
    
    idx = indices[anime_name]

    score = list(
        enumerate(
            similarity[idx]
        )
    )

    score = sorted(score, key=lambda x:x[1], reverse=True )

    score = score[1:11]

    ids = [
        i[0] for i in score
    ]

    return anime[[
            "name",
            "genre",
            "rating"
        ]
    ].iloc[ids]

# UI

st.set_page_config(
    page_title="Anime Recommendation System",
    layout = "wide"
)

st.title("Anime Recommendation System")

st.write("Select an Anime and get similar recommendations")

selected = st.selectbox(
    "Choose Anime", sorted(anime["name"])
)

if st.button("Recommend"):
    result = recommend(selected)

    if result is None:
        st.error("Anime not found")

    else:
        st.subheader("Recommend Anime")

        st.dataframe(result, use_container_width=True)
