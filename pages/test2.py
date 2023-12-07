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
    horizon_options = ["In 2 years or less.",
                       "Within 3 - 5 years.", "Within 06 - 08 years."]
    horizon_values = {'In 2 years or less.': 1,
                      'Within 3 - 5 years.': 5, 'Within 06 - 08 years.': 8}
    horizon = st.radio(
        "1. How long would you invest the majority of your money before you think you would need access to it?",
        horizon_options,
        index=None,
    )

    security_options = ["Not secure.", "Somewhat secure.", "Fairly secure."]
    security_values = {'Not secure.': 1,
                       'Somewhat secure.': 5, 'Fairly secure.': 8}
    security = st.radio(
        "2. How secure is your current and future income from sources such as salary, pensions or other investments?",
        security_options,
        index=None,
    )

    net_wealth_options = ["Less than Tshs 100 million", "Between Tshs 100 million and Tshs 300 million",
                          "Between Tshs 300 million and Tshs 500 million"]
    net_wealth_values = {'Less than Tshs 100 million': 1, 'Between Tshs 100 million and Tshs 300 million': 5,
                         'Between Tshs 300 million and Tshs 500 million': 8}
    net_wealth = st.radio(
        "3. What would you estimate your Net Worth to be; that is total assets less liabilities?",
        net_wealth_options,
        index=None,
    )

    # Generate a random UUID as a hidden variable
    hidden_variable = str(uuid.uuid4())

    # Define investor profiles, descriptions, and strategies; these are categories of the total score
    investor_profiles = {
        "0-20": "Conservative",
        "21-40": "Moderate",
        "41-60": "Balanced",
        "61-80": "Assertive",
        "81-100": "Aggressive",
    }
    profile_descriptions = {
        "0-20": "Conservative investors primarily seek capital preservation and are willing to accept lower potential investment returns in exchange. They may invest in government bonds, corporate bonds, and cash investments.",
        "21-40": "Moderate investors seek a balance between capital growth and capital security. They may invest in a mix of government bonds, corporate bonds, large-cap equity, and cash investments.",
        "41-60": "Balanced investors seek capital growth while also preserving a portion of their capital. They may invest in a mix of large-cap equity, corporate bonds, and government bonds.",
        "61-80": "Assertive investors prioritize capital growth and are willing to take on more risk to achieve it. They may invest in a mix of large-cap equity, small-cap equity, corporate bonds, and government bonds.",
        "81-100": "Aggressive investors are willing to take on the highest level of risk in pursuit of capital growth. They may invest in a mix of large-cap equity, small-cap equity, and corporate bonds.",
    }
    strategies = {
        "0-20": "50\\% Government Bonds; 20% Corporate Bonds; 30% Cash Investments",
        "21-40": "50\\% Government Bonds; 25% Corporate Bonds; 15\\% Large-Cap Equity; 10% Cash Investments",
        "41-60": "45\\% Large-Cap Equity; 35\\% Government Bonds; 15% Corporate Bonds; 5% Cash Investments",
        "61-80": "45\\% Large-Cap Equity; 20% Corporate Bonds; 15\\% Government Bonds; 15% Small-Cap Equity; 5% Cash Investments",
        "81-100": "60\\% Large-Cap Equity; 25% Small-Cap Equity; 10% Corporate Bonds; 5% Cash Investments",
    }

    # Calculate total score
    total_score = horizon_values.get(
        horizon, 0) + security_values.get(security, 0) + net_wealth_values.get(net_wealth, 0)

    # Determine investor profile based on total score
    investor_profile = investor_profiles.get(str(total_score)[:2])

    # Define profile_description and strategy before the conditional statement
    profile_description = None
    strategy = None

    # Move the assignment of profile_description and strategy within the conditional statement
    if investor_profile:
        profile_description = profile_descriptions.get(investor_profile)
        strategy = strategies.get(investor_profile)
    else:
        # Handle case where profile_description is None
        st.error("Unable to determine profile description.")

    # Add variables to session state
    st.session_state["investor_profile"] = investor_profile
    st.session_state["profile_description"] = profile_description
    st.session_state["strategy"] = strategy

    # Display the investor profile, description, and strategy
    st.write(f"Investor profile: {investor_profile}")
    st.write(f"Profile description: {profile_description}")
    st.write(f"Investment strategy: {strategy}")

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
        st.session_state.horizon = horizon
        st.session_state.security = security
        st.session_state.net_wealth = net_wealth
        st.session_state.hidden_variable = hidden_variable  # Store in session state

        st.session_state.total_score = total_score

        # Create a dictionary with the user details
        user_details_dict = {
            "user_name": user_name,
            "user_email": user_email,
            "onboarding_date": onboarding_date,
            "products": products,
            "horizon": horizon,
            "security": security,
            "net_wealth": net_wealth,
            "hidden_variable": hidden_variable,
            "total_score": total_score,
        }

        save_to_database(**user_details_dict)

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
                chat(user_name, user_email, hidden_variable,
                     onboarding_date, products, horizon, security, net_wealth, total_score)


def save_to_database(user_name, user_email, hidden_variable, onboarding_date, products, horizon, security, net_wealth, total_score):
    try:
        # Display a spinner while sending data
        with st.spinner("Sending data to MySQL database..."):
            # Establish a connection to MySQL
            conn = st.connection('advisory_client_mysql', type='sql')

            # Convert the date to the desired format
            formatted_onboarding_date = onboarding_date.strftime("%Y-%m-%d")

            # Join selected products into a single string
            formatted_products = ", ".join(products)

            total_score_int = int(total_score)

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
                    "horizon": [horizon],
                    "security": [security],
                    "net_wealth": [net_wealth],
                    "total_score_int": [total_score_int],
                }

                for i in range(len(data["user_name"])):
                    s.execute(
                        text('INSERT INTO client_details (user_name, user_email, hidden_variable, onboarding_date, products, horizon, security, net_wealth, total_score_int) VALUES (:user_name, :user_email, :hidden_variable, :onboarding_date, :products, :horizon, :security, :net_wealth, :total_score_int);'),
                        params={
                            "user_name": data["user_name"][i],
                            "user_email": data["user_email"][i],
                            "hidden_variable": data["hidden_variable"][i],
                            "onboarding_date": data["onboarding_date"][i],
                            "products": data["products"][i],
                            "horizon": data["horizon"][i],
                            "security": data["security"][i],
                            "net_wealth": data["net_wealth"][i],
                            "total_score_int": data["total_score_int"][i],
                        }
                    )

                s.commit()

            st.success("Data successfully saved to the MySQL database.")

    except Exception as e:
        st.error(f"Error: {e}")


def chat(user_name, user_email, hidden_variable,
         onboarding_date, products, horizon, security, net_wealth, total_score):
    st.title("Chat with ChatGPT")

    st.write(net_wealth)
    st.write(total_score)

    st.write(
        f"Name: {user_name}\nEmail: {user_email}\nHidden Variable: {hidden_variable}\nOnboarding Date: {onboarding_date}\nProducts: {products}\nSecurity: {security}\nHorizon: {horizon}\nNet Wealth: {net_wealth}\nTotal Score: {total_score}"
    )
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
        chat(st.session_state.user_name,
             st.session_state.user_email,
             st.session_state.hidden_variable,
             st.session_state.onboarding_date,
             st.session_state.products,
             st.session_state.horizon,
             st.session_state.security,
             st.session_state.net_wealth,
             st.session_state.total_score)


if __name__ == "__main__":
    main()
