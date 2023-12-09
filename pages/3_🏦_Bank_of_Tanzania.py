import secrets
import streamlit as st

# Function to format number with commas


# text_input = st.text_input(
#         "Enter some text 👇",
#         label_visibility=hidden,
#         # disabled=st.session_state.disabled,
#         # placeholder=st.session_state.placeholder,
#     )


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


st.session_state.products = products
st.session_state.horizon = horizon
st.session_state.security = security
st.session_state.net_wealth = net_wealth


total_score = horizon_values.get(
    horizon, 0) + security_values.get(security, 0) + net_wealth_values.get(net_wealth, 0)
st.session_state.total_score = total_score


st.write("You selected:", total_score)


random_string = secrets.token_hex(20)
st.write(random_string)
