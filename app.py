import time
import os
import base64
import json
from turtle import width
import requests

import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from st_clickable_images import clickable_images
from streamlit_option_menu import option_menu


TENSAI_HEADER_PNG = './utils/imgs/static/tensai_header.png'

NAV_MENU = ["Home", "Games", "Commands", "Mechanics", "Character Styles", "The Project"]

LEO_AVATAR = './utils/imgs/static/leo_avatar.png'
YAMADA_AVATAR = './utils/imgs/static/yamada_avatar.png'
P1_VS_P2 = './utils/imgs/static/p1_vs_p2.png'
P1_AVATAR = './utils/imgs/static/p1.png'
P2_AVATAR = './utils/imgs/static/p2.png'
VERSUS_AVATAR = './utils/imgs/static/versus.png'

DEFAULT_LOTTIE_QUALITY = 'high'
LOTTIE_LOCAL_JSON_PATH_START_ARCADE = './utils/imgs/animated/87120-progress-screen-gif-arcade.json'
LOTTIE_LOCAL_GIT_PATH_START_ARCADE = './utils/imgs/animated/87120-progress-screen-gif-arcade.gif'
LOTTIE_LOCAL_JSON_PATH_FIGHTING = './utils/imgs/animated/26868-fighting.json'
LOTTIE_LOCAL_JSON_PATH_JOYSTICK = './utils/imgs/animated/110018-wave.json'
LOTTIE_LOCAL_JSON_PATH_CHOOSE = './utils/imgs/animated/19659-sliced-text-choose-your-fighter.json'
LOTTIE_LOCAL_JSON_PATH_OHAYOU = './utils/imgs/animated/93881-morning-greeting.json'
LOTTIE_LOCAL_JSON_PATH_TYPING = './utils/imgs/animated/93884-typing.json'
LOTTIE_LOCAL_JSON_PATH_SHIBA_YATTA = './utils/imgs/animated/86964-shiba-happy.json'

SOCIAL_GITHUB_LOGO = './utils/imgs/animated/81333-github.gif'
SOCIAL_LINKEDIN_LOGO = './utils/imgs/animated/49413-linkedin-icon.gif'
SOCIAL_TWITTER_LOGO = './utils/imgs/animated/49409-twitter-icon.gif'

SFV_LOGO = './utils/imgs/static/games_logos/SF5_logo.jpg'
DBFZ_LOGO = './utils/imgs/static/games_logos/DBFZ_logo.png'
GBVS_LOGO = './utils/imgs/static/games_logos/GBVS_logo.png'
GGS_LOGO = './utils/imgs/static/games_logos/GGS_logo.png'
MK11_LOGO = './utils/imgs/static/games_logos/MK11_logo.png'
TEKKEN7_LOGO = './utils/imgs/static/games_logos/Tekken7_logo.png'

SFV_PHOTOS_PATH = './utils/imgs/static/sfv/'
SFV_RYU_AVATAR = './utils/imgs/static/characters_avatares/sfv_ryu_3.jpg'
SFV_CHUNLI_AVATAR = './utils/imgs/static/characters_avatares/sfv_chunli.jpg'
SFV_NASH_AVATAR = './utils/imgs/static/characters_avatares/sfv_nash.jpg'
SFV_MBISON_AVATAR = './utils/imgs/static/characters_avatares/sfv_mbison.jpg'

GGS_PHOTOS_PATH = './utils/imgs/static/ggs/'

ST_PAGE_NAME ='TENSAI!'
ST_PAGE_ICON = '👺'
ST_PAGE_LAYOUT = 'wide' # 'centered' | 'wide'

PADDING_TOP = 0
PADDING_RIGHT = 0.1
PADDING_LEFT = 0.1
PADDING_BOTTOM = 1

BLABLA = '''
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
'''
BLABLABLA = '''
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
'''


def list_directory(path):
    file_name_list = os.listdir(path)
    pathes = []
    for file_name in file_name_list:
        pathes.append(path+file_name)
    return pathes


def build_padding_string(direction,value):
    return '<style>div.block-container{padding-'+direction+':'+str(value)+'rem;}</style>'


def session_break(times):
    for i in range(times):
        st.write('')


def block_break():
    st.markdown('---')


def title(text,size,align,color):
    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;color:{color};text-align:{align};">{text}</h1>',unsafe_allow_html=True)


def header(text):
    st.markdown(f"<p style='color:black;'>{text}</p>",unsafe_allow_html=True)


def generate_page_header():
    # centered page header
    header_col1, header_col2, header_col3 = st.columns((1,1,1))

    with header_col1:
        pass
    with header_col2:
        st.image(TENSAI_HEADER_PNG)
    with header_col3:
        pass
    

st.set_page_config(
    page_title=ST_PAGE_NAME,
    page_icon=ST_PAGE_ICON,
    layout=ST_PAGE_LAYOUT
)
st.markdown(""" <style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

st.markdown(build_padding_string('top',PADDING_TOP), unsafe_allow_html=True)
st.markdown(build_padding_string('right',PADDING_RIGHT), unsafe_allow_html=True)
st.markdown(build_padding_string('left',PADDING_LEFT), unsafe_allow_html=True)
st.markdown(build_padding_string('bottom',PADDING_BOTTOM), unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code


@st.cache(allow_output_mutation=True)
def get_social_media_href(social_medias):
    html_code = '<div class="images">'
    for local_img_path, target_url in social_medias:
        img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
        bin_str = get_base64_of_bin_file(local_img_path)
        html_code += f'''
            <div style="float:left;margin-right:0px;">
            <a href="{target_url}" target="_blank">
                <img width="100px" src="data:image/{img_format};base64,{bin_str}"/>
            </a>
            </div>'''
    html_code += '</div>'
    return html_code


def load_lottie_json(json_path: str):
    with open(json_path, encoding="utf8") as json_file:
        return json.load(json_file)


def start():
    with st_lottie_spinner(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_START_ARCADE), quality=DEFAULT_LOTTIE_QUALITY, height=500, key="Arcade"):
        time.sleep(2)


def main():
    if 'game_selected' not in st.session_state:
        st.session_state['game_selected'] = None  

    # Start!
    if 'app_started' not in st.session_state:
        st.session_state['app_started'] = False

    if st.session_state['app_started'] is False:
        start()
        st.session_state['app_started'] = True

    # Header
    generate_page_header()

    game_clicked = None

    if 'tab_selected' not in st.session_state:
        st.session_state['tab_selected'] = 0

    selected = option_menu("",
        NAV_MENU, 
        icons=['house', 'controller', 'dpad', 'gear-fill', 'caret-right-square', 'github'],
        orientation='horizontal',
        default_index=0
    )

    # print(list_directory(SFV_PHOTOS_PATH+'avatares/'))

    # Page: Home
    if selected == NAV_MENU[0]:
        # About Us
        home_about_us_col1, home_about_us_col2, home_about_us_col3, home_about_us_col4, home_about_us_col5 = st.columns((0.2,2,0.3,1,0.3))
        with home_about_us_col2:
            title('About Us',40,'left','black')
            st.markdown(BLABLABLA)
        with home_about_us_col4:
            st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_OHAYOU),
                quality=DEFAULT_LOTTIE_QUALITY,
                loop=True,
                height=300,
                # width=500,
                key="Ohayou"
            )
        block_break()

        # Our Mission
        home_mission_col1, home_mission_col2, home_mission_col3, home_mission_col4, home_mission_col5 = st.columns((0.2,1.2,0.15,2,0.15))
        with home_mission_col2:
            st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_TYPING),
                quality=DEFAULT_LOTTIE_QUALITY,
                loop=True,
                height=300,
                # width=500,
                key="Joy"
            )
        with home_mission_col4:
            title('Our Mission',40,'left','black')
            st.markdown(BLABLABLA)

        block_break() 

        # The Team
        home_team_header_col1, home_team_header_col2, home_team_header_col3, home_team_header_col4, home_team_header_col5 = st.columns((0.2,2,1,0.3,0.3))
        with home_team_header_col2:
            title('The Team',40,'left','black')

        home_team_vs_col1, home_team_vs_col2, home_team_vs_col3, home_team_vs_col4, home_team_vs_col5 = st.columns((0.9,1,1,1,0.5))
        with home_team_vs_col2:
            with open(P1_AVATAR, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
            st.markdown(f'<img width="200px" src="data:image/jpeg;base64,{encoded}" alt="Versus" class="center">', unsafe_allow_html=True)
        with home_team_vs_col3:
            with open(VERSUS_AVATAR, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
            st.markdown(f'<img width="200px" src="data:image/jpeg;base64,{encoded}" alt="Versus" class="center">', unsafe_allow_html=True)
        with home_team_vs_col4:
            with open(P2_AVATAR, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
            st.markdown(f'<img width="200px" src="data:image/jpeg;base64,{encoded}" alt="Versus" class="center">', unsafe_allow_html=True)      

        home_team_members_col1, home_team_members_col2, home_team_members_col3, home_team_members_col4, home_team_members_col5 = st.columns((0.2,1.5,0.2,1.5,0.2))
        with home_team_members_col2:
            title('Leo Bertella (CEO) 💭',35,'center','black')
            st.markdown(BLABLA)
            st.markdown('Social Medias')
            st.markdown(get_social_media_href([(SOCIAL_GITHUB_LOGO,'https://github.com/lmassaoy/'),(SOCIAL_LINKEDIN_LOGO,'https://www.linkedin.com/in/luis-yamada/'),(SOCIAL_TWITTER_LOGO,'https://twitter.com/massaoyamada')]), unsafe_allow_html=True)
        with home_team_members_col4:
            title('Luis Yamada (CTO) 💻',35,'center','black')
            st.markdown(BLABLA)
            st.markdown('Social Medias')
            st.markdown(get_social_media_href([(SOCIAL_GITHUB_LOGO,'https://github.com/lmassaoy/'),(SOCIAL_LINKEDIN_LOGO,'https://www.linkedin.com/in/luis-yamada/'),(SOCIAL_TWITTER_LOGO,'https://twitter.com/massaoyamada')]), unsafe_allow_html=True)

        block_break() 

        # Support Us
        home_support_col1, home_support_col2, home_support_col3, home_support_col4, home_support_col5 = st.columns((0.2,2,0.3,1,0.3))
        with home_support_col2:
            title('Support Us 🥰',40,'left','black')
            st.markdown('Together **WE** are stronger.')
            st.markdown(BLABLABLA)
        with home_support_col4:
            st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_SHIBA_YATTA),
                quality=DEFAULT_LOTTIE_QUALITY,
                loop=True,
                # height=300,
                # width=500,
                key="Yatta"
            )


    # Page: Games
    if selected == NAV_MENU[1]:
        games_logos = []
        for file in [SFV_LOGO,DBFZ_LOGO,GBVS_LOGO,GGS_LOGO,MK11_LOGO,TEKKEN7_LOGO]:
            with open(file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                games_logos.append(f"data:image/jpeg;base64,{encoded}")

        game_clicked = clickable_images(
            games_logos,
            titles=[f"{str(i)}" for i in range(5)],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "width": "250px"},
        )
        games_col1, games_col2, games_col3, games_col4, games_col5 = st.columns((0.7,1.8,2,0.3,0.3))
        with games_col2:
            st.markdown(f'## {game_clicked}')
            st.markdown(BLABLABLA)

        game_clicked
        if game_clicked != -1:
            st.session_state['game_selected'] = game_clicked
            st.session_state['tab_selected'] = selected

    # Page: Commands
    if selected == NAV_MENU[2] or st.session_state['tab_selected'] == selected:
        title('GAMES',60,'center','black')
        
        # with st_lottie_spinner(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_CHOOSE), quality=DEFAULT_LOTTIE_QUALITY, height=600):
        #     time.sleep(3)
            # if st.session_state['game_selected'] is None or st.session_state['game_selected'] == -1:
            #     st.markdown('# CHOOSE A GAME IN "Games" TAB')
            # else:
            #     st.markdown(f"# {st.session_state['game_selected']}")
        games_col1, games_col2, games_col3 = st.columns((0.2,5,0.2))
        with games_col2:
            games_logos = []
            for file in [SFV_LOGO,DBFZ_LOGO,GBVS_LOGO,GGS_LOGO,MK11_LOGO,TEKKEN7_LOGO]:
                with open(file, "rb") as image:
                    encoded = base64.b64encode(image.read()).decode()
                    games_logos.append(f"data:image/jpeg;base64,{encoded}")

            game_clicked = clickable_images(
                games_logos,
                titles=[f"{str(i)}" for i in range(5)],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "width": "300px"},
                key='games'
            )

            block_break()
        if game_clicked != -1:
            title('CHARACTERS',60,'center','black')
            if game_clicked == 0:
                characters_avatares = []
                for file in list_directory(SFV_PHOTOS_PATH+'avatares/'):
                    with open(file, "rb") as image:
                        encoded = base64.b64encode(image.read()).decode()
                        characters_avatares.append(f"data:image/jpeg;base64,{encoded}")

                character_click = clickable_images(
                    characters_avatares,
                    titles=[f"{str(i)}" for i in range(len(list_directory(SFV_PHOTOS_PATH+'avatares/')))],
                    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                    img_style={"margin": "5px", "height": "194px"},
                    key='characters'
                )
                character_click

                if character_click != -1:
                    if character_click == 0:
                        st.markdown('# Ryu')
                    elif character_click == 1:
                        st.markdown('# Chun-Li')
                    elif character_click == 2:
                        st.markdown('# Nash')
                    elif character_click == 3:
                        st.markdown('# M. Bison')

            if game_clicked == 3:
                characters_avatares = []
                for file in list_directory(GGS_PHOTOS_PATH+'avatares/'):
                    with open(file, "rb") as image:
                        encoded = base64.b64encode(image.read()).decode()
                        characters_avatares.append(f"data:image/jpeg;base64,{encoded}")

                character_click = clickable_images(
                    characters_avatares,
                    titles=[f"{str(i)}" for i in range(len(list_directory(SFV_PHOTOS_PATH+'avatares/')))],
                    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                    img_style={"margin": "5px", "height": "224px"},
                    key='characters'
                )
                character_click

if __name__ == "__main__":
    main()