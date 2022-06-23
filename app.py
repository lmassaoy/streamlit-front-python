import time
import os
import base64
import json
import requests

import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from st_clickable_images import clickable_images
# from st_on_hover_tabs import on_hover_tabs
from streamlit_option_menu import option_menu


TENSAI_HEADER_PNG = './utils/imgs/static/tensai_header.png'

DEFAULT_LOTTIE_QUALITY = 'high'
LOTTIE_LOCAL_JSON_PATH_START_ARCADE = './utils/imgs/animated/87120-progress-screen-gif-arcade.json'
LOTTIE_LOCAL_GIT_PATH_START_ARCADE = './utils/imgs/animated/87120-progress-screen-gif-arcade.gif'
LOTTIE_LOCAL_JSON_PATH_FIGHTING = './utils/imgs/animated/26868-fighting.json'

ST_PAGE_NAME ='TENSAI!'
ST_PAGE_ICON = '👺'
ST_PAGE_LAYOUT = 'wide'

PADDING_TOP = 0
PADDING_RIGHT = 0.1
PADDING_LEFT = 0.1
PADDING_BOTTOM = 1


def build_padding_string(direction,value):
    return '<style>div.block-container{padding-'+direction+':'+str(value)+'rem;}</style>'


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
    with st_lottie_spinner(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_START_ARCADE), key="Arcade"):
        time.sleep(1.5)


def main():
    # st.title('TENSAI')  
    # st_lottie(load_lottie_json(LOTTIE_LOCAL_JSON_PATH_START_ARCADE),
    #     quality=DEFAULT_LOTTIE_QUALITY,
    #     key="Arcade"
    # )

#    st.markdown(get_img_with_href(LOTTIE_LOCAL_GIT_PATH_START_ARCADE, 'https://github.com/lmassaoy'), unsafe_allow_html=True)
    
    # sample to use the grid for game titles
    # st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

    # st.markdown('# Started')
    
    if 'app_started' not in st.session_state:
        st.session_state['app_started'] = False

    if st.session_state['app_started'] is False:
        start()
        st.session_state['app_started'] =True

    st.image(TENSAI_HEADER_PNG)

    selected = option_menu("",
        ["Home", "Games", "Command Lists", "Special Mechanics", "Character Styles", "The TENSAI project"], 
        icons=['house', 'controller', 'dpad', 'gear-fill', 'caret-right-square', 'github'],
        # menu_icon="joystick",
        orientation='horizontal',
        default_index=0)
    # selected



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