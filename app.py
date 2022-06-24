from asyncore import loop
import time
import os
import base64
import json
from turtle import width
import requests

import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from st_clickable_images import clickable_images
# from st_on_hover_tabs import on_hover_tabs
from streamlit_option_menu import option_menu


TENSAI_HEADER_PNG = './utils/imgs/static/tensai_header.png'

NAV_MENU = ["Home", "Games", "Commands", "Mechanics", "Character Styles", "The Project"]

DEFAULT_LOTTIE_QUALITY = 'high'
LOTTIE_LOCAL_JSON_PATH_START_ARCADE = './utils/imgs/animated/87120-progress-screen-gif-arcade.json'
LOTTIE_LOCAL_GIT_PATH_START_ARCADE = './utils/imgs/animated/87120-progress-screen-gif-arcade.gif'
LOTTIE_LOCAL_JSON_PATH_FIGHTING = './utils/imgs/animated/26868-fighting.json'
LOTTIE_LOCAL_JSON_PATH_JOYSTICK = './utils/imgs/animated/110018-wave.json'
LOTTIE_LOCAL_JSON_PATH_CHOOSE = './utils/imgs/animated/19659-sliced-text-choose-your-fighter.json'

SFV_LOGO = './utils/imgs/static/games_logos/SF5_logo.jpg'
DBFZ_LOGO = './utils/imgs/static/games_logos/DBFZ_logo.png'
GBVS_LOGO = './utils/imgs/static/games_logos/GBVS_logo.png'
GGS_LOGO = './utils/imgs/static/games_logos/GGS_logo.png'
MK11_LOGO = './utils/imgs/static/games_logos/MK11_logo.png'
TEKKEN7_LOGO = './utils/imgs/static/games_logos/Tekken7_logo.png'

SFV_RYU_AVATAR = './utils/imgs/static/characters_avatares/sfv_ryu_3.jpg'
SFV_CHUNLI_AVATAR = './utils/imgs/static/characters_avatares/sfv_chunli.jpg'
SFV_NASH_AVATAR = './utils/imgs/static/characters_avatares/sfv_nash.jpg'
SFV_MBISON_AVATAR = './utils/imgs/static/characters_avatares/sfv_mbison.jpg'

ST_PAGE_NAME ='TENSAI!'
ST_PAGE_ICON = '👺'
ST_PAGE_LAYOUT = 'wide' # 'centered' | 'wide'

PADDING_TOP = 0
PADDING_RIGHT = 0.1
PADDING_LEFT = 0.1
PADDING_BOTTOM = 1

BLABLABLA = '''
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
    BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla
'''


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


# st.markdown(f""" <style>
#     .reportview-container .main .block-container{{
#         padding-top: {padding}rem;
#         padding-right: {padding}rem;
#         padding-left: {padding}rem;
#         padding-bottom: 2rem;
#     }} </style> """, unsafe_allow_html=True
# )





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


def load_lottie_json(json_path: str):
    with open(json_path) as json_file:
        return json.load(json_file)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# images = []
# for file in [LOTTIE_LOCAL_GIT_PATH_START_ARCADE, LOTTIE_LOCAL_GIT_PATH_START_ARCADE]:
#     with open(file, "rb") as image:
#         encoded = base64.b64encode(image.read()).decode()
#         images.append(f"data:image/jpeg;base64,{encoded}")

# clicked = clickable_images(
#     images,
#     titles=[f"Image #{str(i)}" for i in range(2)],
#     div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
#     img_style={"margin": "5px", "height": "200px"},
# )


def start():
    with st_lottie_spinner(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_START_ARCADE), quality=DEFAULT_LOTTIE_QUALITY, height=500, key="Arcade"):
        time.sleep(2)


def main():
    if 'game_selected' not in st.session_state:
        st.session_state['game_selected'] = None

    # st.title('TENSAI')  
    # st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_CHOOSE),
    #     quality=DEFAULT_LOTTIE_QUALITY,
    #     key="Arcade"
    # )

#    st.markdown(get_img_with_href(LOTTIE_LOCAL_GIT_PATH_START_ARCADE, 'https://github.com/lmassaoy'), unsafe_allow_html=True)
    
    # sample to use the grid for game titles
    # st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

    # st.markdown('# Started')
    

    # Start!
    if 'app_started' not in st.session_state:
        st.session_state['app_started'] = False

    if st.session_state['app_started'] is False:
        start()
        st.session_state['app_started'] = True

    generate_page_header()

    game_clicked = None

    if 'tab_selected' not in st.session_state:
        st.session_state['tab_selected'] = 0

    selected = option_menu("",
        NAV_MENU, 
        icons=['house', 'controller', 'dpad', 'gear-fill', 'caret-right-square', 'github'],
        # menu_icon="joystick",
        orientation='horizontal',
        default_index=0
    )

    if selected == NAV_MENU[0]:
        home_col1, home_col2, home_col3, home_col4, home_col5 = st.columns((0.7,2,1,0.3,0.3))

        with home_col2:
            st.markdown('## About Us')
            st.markdown(BLABLABLA)
            st.markdown('## Team members')
            st.markdown('### Leonardo Bertella - CEO')
        with home_col3:
            st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_JOYSTICK),
                quality=DEFAULT_LOTTIE_QUALITY,
                loop=False,
                height=300,
                key="Joy"
            )

    if selected == NAV_MENU[1]:
        games_logos = []
        for file in [SFV_LOGO,DBFZ_LOGO,GBVS_LOGO,GGS_LOGO,MK11_LOGO,TEKKEN7_LOGO]:
            with open(file, "rb") as image:
                encoded = base64.b64encode(image.read()).decode()
                games_logos.append(f"data:image/jpeg;base64,{encoded}")

        
        # with games_col2:
        #     game_clicked = clickable_images(
        #         games_logos,
        #         titles=[f"{str(i)}" for i in range(5)],
        #         div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        #         img_style={"margin": "5px", "height": "120px"},
        #     )
        #     game_clicked
        #     st.markdown('8===============D')

        # with games_col3:
        #     st.markdown(f'## {game_clicked}')
        #     st.markdown(BLABLABLA)

        game_clicked = clickable_images(
            games_logos,
            titles=[f"{str(i)}" for i in range(5)],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "120px"},
        )
        games_col1, games_col2, games_col3, games_col4, games_col5 = st.columns((0.7,1.8,2,0.3,0.3))
        with games_col2:
            st.markdown(f'## {game_clicked}')
            st.markdown(BLABLABLA)

        game_clicked
        if game_clicked != -1:
            st.session_state['game_selected'] = game_clicked
            st.session_state['tab_selected'] = selected

        # st.markdown('8===============D')

    if selected == NAV_MENU[2] or st.session_state['tab_selected'] == selected:
        # with st_lottie_spinner(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_CHOOSE), quality=DEFAULT_LOTTIE_QUALITY, height=600):
        #     time.sleep(3)
        #     if st.session_state['game_selected'] is None or st.session_state['game_selected'] == -1:
        #         st.markdown('# CHOOSE A GAME IN "Games" TAB')
        #     else:
        #         st.markdown(f"# {st.session_state['game_selected']}")
        games_col1, games_col2, games_col3 = st.columns((0.2,0.9,0.2))
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
                img_style={"margin": "5px", "height": "120px"},
                key='games'
            )

            if game_clicked != -1:
                if game_clicked == 0:
                    characters_avatares = []
                    for file in [SFV_RYU_AVATAR,SFV_CHUNLI_AVATAR,SFV_NASH_AVATAR,SFV_MBISON_AVATAR]:
                        with open(file, "rb") as image:
                            encoded = base64.b64encode(image.read()).decode()
                            characters_avatares.append(f"data:image/jpeg;base64,{encoded}")

                    character_click = clickable_images(
                        characters_avatares,
                        titles=[f"{str(i)}" for i in range(5)],
                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                        img_style={"margin": "4px", "height": "150px"},
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


# def start():
#     if st.session_state['app_started'] is False:
#         start_images = []
#         for file in [LOTTIE_LOCAL_GIT_PATH_START_ARCADE]:
#             with open(file, "rb") as image:
#                 encoded = base64.b64encode(image.read()).decode()
#                 start_images.append(f"data:image/jpeg;base64,{encoded}")

#         start_clicked = clickable_images(
#             start_images,
#             titles=['Click here to begin the journey!'],
#             div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
#             img_style={"margin": "5px", "height": "500px"},
#         )

#         st.markdown(st.session_state['app_started'])

#         if start_clicked == 0:
#             st.session_state['app_started'] = True
#             st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_FIGHTING),
#                 quality=DEFAULT_LOTTIE_QUALITY,
#                 key="Fighting"
#             )
#         else:
#             # st.markdown(start_clicked)
#             pass

#         st.markdown(st.session_state['app_started'])


if __name__ == "__main__":
    main()