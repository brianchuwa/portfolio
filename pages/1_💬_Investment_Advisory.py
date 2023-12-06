from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Investment Advisory",
    page_icon="💬",
    layout="wide",
    # initial_sidebar_state="expanded",
)

# st.write("# Coming Soon! ")

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir.parent / "styles" / "main.css"

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


st.title("Start your investing journey")

st.write('\n')
st.write('\n')


def streamlit_menu():
    selected = option_menu(
        menu_title=None,  # required
        options=["Overview", "Chat"],  # required
        icons=["house", "chat"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
        styles={
            "container": {"background-color": "#444E56"},
            "icon": {"color": "white"},
        }
    )
    return selected


selected = streamlit_menu()

if selected == "Overview":
    st.title(f"You have selected {selected}")


if selected == "Chat":
    st.title(f"You have selected {selected}")

    # col1, buff, col2 = st.beta_columns([1, 0.5, 3])

    # option_names = ["Overview", "Questions", "Chat"]

    # next = st.button("Next option")

    # if next:
    #     if st.session_state["radio_option"] == 'Overview':
    #         st.session_state.radio_option == 'Questions'
    #     elif st.session_state["radio_option"] == 'Questions':
    #         st.session_state.radio_option == 'Chat'
    #     else:
    #         st.session_state.radio_option == 'Overview'

    # option = col1.radio("Pick an option", option_names, key="radio_option")
    # st.session_state

    # if option == 'Overview':
    #     col2.write("You picked overvie")
    # elif option == 'Questions':
    #     col2.write("You picked Qns")
    # else:
    #     col2.write("you picked chat")


# if selected == "Chat":
#     st.title(f"You have selected {selected}")
