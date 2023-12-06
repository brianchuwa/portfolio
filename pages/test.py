import uuid
import streamlit as st
from sqlalchemy import text


def user_details():
    st.title("User Details Form")

    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    onboarding_date = st.date_input(label="Onboarding Date", value=None)
    products = st.multiselect(
        "Products Offered", ['Green', 'Yellow', 'Red', 'Blue'], default=None)

    # Generate a random UUID as a hidden variable
    hidden_variable = str(uuid.uuid4())

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    def callback():
        if not user_name or not user_email:
            st.warning("Please fill in all fields before starting the chat.")
            return
        st.session_state.button_clicked = True
        st.session_state.step = "Chat"
        st.session_state.user_name = user_name
        st.session_state.user_email = user_email
        st.session_state.onboarding_date = onboarding_date
        st.session_state.products = products
        st.session_state.hidden_variable = hidden_variable  # Store in session state

        save_to_database(user_name, user_email,
                         hidden_variable, onboarding_date, products)

    if (
        st.button(label="Next") or st.session_state.button_clicked
    ):
        # Process user details and move to the next step
        if st.button("Start Chat",
                     on_click=callback):
            # st.balloons()
            st.session_state.step = "Chat"
            if st.session_state.step == "Chat":
                # save_to_database(user_name, user_email)
                chat(user_name, user_email)


def save_to_database(user_name, user_email, hidden_variable, onboarding_date, products):
    try:
        # Display a spinner while sending data
        with st.spinner("Sending data to MySQL database..."):
            # Establish a connection to MySQL
            conn = st.connection('advisory_client_mysql', type='sql')

            # Convert the date to the desired format
            formatted_onboarding_date = onboarding_date.strftime("%Y-%m-%d")

            # Join selected products into a single string
            formatted_products = ", ".join(products)

            with conn.session as s:
                # Assuming 'client_details' is the table name
                # s.execute(text(
                #     'CREATE TABLE IF NOT EXISTS client_details (user_name TEXT, user_email TEXT, hidden_variable TEXT, onboarding_date TEXT, products TEXT);'))
                # s.execute(text('DELETE FROM client_details;'))

                # Prepare the data to be sent to MySQL
                data = {
                    "user_name": [user_name],
                    "user_email": [user_email],
                    "hidden_variable": [hidden_variable],
                    "onboarding_date": [formatted_onboarding_date],
                    "products": [formatted_products],
                }

                for i in range(len(data["user_name"])):
                    s.execute(
                        text('INSERT INTO client_details (user_name, user_email, hidden_variable, onboarding_date, products) VALUES (:user_name, :user_email, :hidden_variable, :onboarding_date, :products);'),
                        params={
                            "user_name": data["user_name"][i],
                            "user_email": data["user_email"][i],
                            "hidden_variable": data["hidden_variable"][i],
                            "onboarding_date": data["onboarding_date"][i],
                            "products": data["products"][i],
                        }
                    )

                s.commit()

            st.success("Data successfully saved to the MySQL database.")

    except Exception as e:
        st.error(f"Error: {e}")


def chat(user_name, user_email):
    st.title("Chat with ChatGPT")

    st.write(
        f"Hello {user_name} ({user_email})!")
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
        # st.session_state.user_name = None
        # st.session_state.user_email = None

    if st.session_state.step == "User Details":
        user_details()
    elif st.session_state.step == "Chat":
        chat(st.session_state.user_name, st.session_state.user_email)


if __name__ == "__main__":
    main()
