from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="BOT Insights",
    page_icon="🏦",
    layout="wide",
    # initial_sidebar_state="expanded",
)

st.write("# Coming Soon! ")

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir.parent / "styles" / "main.css"

# --- LOAD CSS ---
# with open(css_file) as f:
#     st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


# def overview():
#     st.title("Chat App Overview")
#     st.write("Welcome to our chat app! This is an overview of the app.")
#     if st.button("Next"):
#         st.session_state.step = "User Details"

state = st.session_state.step = "User Details"


def user_details():
    st.title("User Details Form")
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")

    if st.button("Next"):
        # Process user details and move to the next step
        st.success("User details submitted successfully!")
        st.session_state.step = "Chat"


def chat():
    st.title("Chat with ChatGPT")
    # Your chat interface here
    st.title("Echo Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"Echo: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})


def main():
    if "step" not in st.session_state:
        st.session_state.step = "User Details"

    if st.session_state.step == "User Details":
        user_details()
    elif st.session_state.step == "Chat":
        chat()


if __name__ == "__main__":
    main()
