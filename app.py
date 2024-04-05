import streamlit as st
import pandas as pd
import numpy as np
from fuzzywuzzy import process, fuzz


@st.cache_data
def get_data():
    return pd.read_csv('./anime_data_2006_2022_cleaned.csv'), pd.read_pickle('./anime_similarity_v2.pkl')


def build_input():
    return st.text_input('Enter an anime title you wanna find')


def anime_recommendation(ititle, titles, ani_df, ani_sim):
    ani_name = process.extract(
        ititle, titles, scorer=fuzz.token_set_ratio)[0][0]
    # number = 1
    try:
        # for anime in ani_sim.sort_values(by=ani_name, ascending=False).index[1:6]:
        #     st.write(
        #         f'#{number} => {anime}, {round(ani_sim[anime][ani_name]*100,2)}% match')
        #     number += 1
        similar_animes = ani_sim.sort_values(
            by=ani_name, ascending=False).index[1:7]
        # print(similar_animes)
        similar_animes = pd.DataFrame(similar_animes)
        # print(similar_animes)
        similar_animes['similar_score'] = similar_animes['title'].apply(
            lambda x: round(ani_sim[x][ani_name]*100, 2))
        # print(similar_animes)
        result = pd.merge(ani_df, similar_animes, how='inner', on='title')
        result = result.sort_values(by='similar_score', ascending=False)
        # st.write(result)
        st.write(f'If you like {ani_name}, how about watching these 🤗 :\n')
        return result, True
    except:
        return None, False


def read_custom_css():
    with open('./style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def show_result(df):
    result_str = ''
    for index, row in df.iterrows():
        result_str += f'''
            <div class="anime">
                <article class="poster">
                    <img src="{row['image_url']}" alt="" class="img">
                </article>
                <article class="info">
                    <div class="body">
                        <div class="header">
                            <h3>{row['title']}</h3>
                            <h4>{row['studios']}</h4>
                            <p>
                                {', '.join(row['genres'].split(','))} <br>
                                {row['type']} &middot; {int(row['episodes'])} episodes
                            </p>
                        </div>
                        <div class="synopsis">
                            <p>
                                {row['synopsis']}
                            </p>
                        </div>
                    </div>
                </article>
            </div>'''
    st.markdown(
        f'<section class="anime-list">{result_str}</section>', unsafe_allow_html=True)


def main():
    # st.set_page_config(layout='wide', initial_sidebar_state='expanded')

    animes, ani_sim = get_data()
    animes = animes[animes['type'] == 'TV']
    titles = animes['title'].unique().tolist()

    read_custom_css()
    st.title('Searching Similar Animes (2006 - 2022)')

    input_title = build_input()

    if input_title:
        result, isTrue = anime_recommendation(
            input_title, titles, animes, ani_sim)
        if isTrue:
            show_result(result)
        else:
            st.write('No anime is found.')


if __name__ == '__main__':
    main()
