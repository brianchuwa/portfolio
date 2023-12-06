import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="DSE Market Insights",
    page_icon="📊",
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


def user_details():
    st.title("User Details Form")

    # Use session state to control the expanded state
    expanded_state = st.session_state.get("expanded_state", True)

    # Expander 1: User Details Section 1
    with st.expander("User Details Section 1", expanded=expanded_state):
        user_name_1 = st.text_input("Your Name (Section 1)")
        user_email_1 = st.text_input("Your Email (Section 1)")

    # Expander 2: User Details Section 2
    with st.expander("User Details Section 2", expanded=expanded_state):
        user_name_2 = st.text_input("Your Name (Section 2)")
        user_email_2 = st.text_input("Your Email (Section 2)")

    # Add a submit button
    if st.button("Next"):
        # Check if required fields are filled
        if not user_name_1 or not user_email_1 or not user_name_2 or not user_email_2:
            st.warning("Please fill in all required fields.")
        else:
            # Process user details and move to the next step
            st.success("User details submitted successfully!")
            st.session_state.expanded_state = False  # Set expanded state to False
            st.session_state.step = "Chat"
            if st.session_state.step == "Chat":
                chat(user_name_1, user_email_1, user_name_2, user_email_2)


def chat(user_name_1, user_email_1, user_name_2, user_email_2):
    st.title("Chat with ChatGPT")
    # Your chat interface here
    st.write(
        f"Hello {user_name_1} ({user_email_1}) and {user_name_2} ({user_email_2})!")

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
    user_details()


if __name__ == "__main__":
    main()
