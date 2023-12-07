""" Investment advisory app, takes users profile and chats with AI advisor """
import uuid
import streamlit as st
import pandas as pd
from sqlalchemy import text


st.set_page_config(
    page_title="Investment Advisory",
    page_icon="💬",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

# Load external CSS file
main_css = open("styles/main_pages.css", encoding='utf-8').read()
st.markdown(f'<style>{main_css}</style>', unsafe_allow_html=True)


def user_details():
    """
    Display a user details form using Streamlit.

    The function prompts the user to input their personal details and select 
    best answer from a set of multiple questions. It then generates a random UUID
    as a hidden variable and calculates a total score based on the selected options.

    Parameters:
    - None

    Returns:
    - None
    """
    # Center-aligned Title
    st.markdown("<h1 style='text-align: center;'>💰Investment Advisory</h1>",
                unsafe_allow_html=True)

    st.write('\n')

    # Introduction Note
    introduction_text = """
    **Welcome to the journey of shaping your investment future!** 
    
    Understanding your financial goals and risk tolerance is the first step toward building a robust investment portfolio. Explore the questions below to define your investment preferences, and let's work together to create a strategy that aligns with your aspirations.

    **Key Steps:**
    1. **Goal Exploration:** Delve into your financial objectives.
    2. **Risk Assessment:** Define your attitude toward risk and its impact on your investments.
    3. **Advisor Chat:** Connect with our experienced financial advisor for personalised insights.

    Our advisor is well-versed in the Tanzanian capital market and is here to guide you. Rest assured, your information is confidential and will only be used to tailor your investment strategy.

    **Ready to get started on your investment journey?** Answer the questions below and unlock a world of financial possibilities!

    **Important:** This process assumes you have the money already to invest.
    """

    # Render Introduction Note as Markdown
    st.markdown(introduction_text, unsafe_allow_html=True)

    st.write('\n')
    st.divider()
    st.divider()

    # ---- INVESTORS'S DETAILS -----

    st.header("Investor's Details")
    st.write('\n')

    full_name = st.text_input("Your Full Name:*")

    def format_with_commas(number):
        """
        Format a numeric value with commas for display purposes.

        Parameters:
        - number (float or int): The numeric value to be formatted.

        Returns:
        - str or None: The formatted string with commas if the input is not None, otherwise None.
        """
        return f"{number:,.0f}" if number is not None else None

    # User input for the amount
    amount_to_invest = st.number_input(
        "Amount to invest (TZS):*", min_value=0, value=None, step=None)
    # Display the formatted amount (with commas) as the user types
    st.markdown(
        f"***The amount you entered: {format_with_commas(amount_to_invest)}***")

    gender = st.radio("Select Gender:*", ["Male", "Female"], index=None)

    # age
    age = st.number_input(
        "Age:*", min_value=0, value=None, step=1)

    # location
    location = st.text_input("Your location (Region):*")

    # phone_number
    phone_number = st.text_input(
        "Enter your phone number:", placeholder="e.g., 0652 000 000")

    # email
    email = st.text_input("Enter your email address:",
                          placeholder="e.g., john.doe@example.com")

    # ocuupation
    occupation = st.text_input(
        "Enter your occupation:*", placeholder="e.g., Doctor")

    st.write('\n')
    st.write('\n')
    st.divider()

    # ----- RISK PROFILE QUESTIONS -----

    st.header("Risk Profile Questions")
    st.markdown(
        "***On a range of 1 to 10, select the most appropriate answer as according to the options provided.***")
    st.write('\n')

    # horizon
    horizon_options = ["In 2 years or less.",
                       "Within 3 - 5 years.",
                       "Within 06 - 08 years.",
                       "9 years or more"
                       ]
    horizon_values = {'In 2 years or less.': 1,
                      'Within 3 - 5 years.': 4,
                      'Within 06 - 08 years.': 7,
                      '9 years or more': 10
                      }
    horizon = st.radio(
        "Qn 1. How long would you invest the majority of your money before you think you would need access to it?",
        horizon_options,
        index=None,
    )

    # security
    security_options = ["Not secure.",
                        "Somewhat secure.",
                        "Fairly secure.",
                        "Very secure."
                        ]
    security_values = {'Not secure.': 1,
                       'Somewhat secure.': 4,
                       'Fairly secure.': 6,
                       'Very secure.': 10
                       }
    security = st.radio(
        "Qn 2. How secure is your current and future income from sources such as salary, pensions or other investments?",
        security_options,
        index=None,
    )

    # net_worth
    net_wealth_options = ["Less than Tshs 100 million",
                          "Between Tshs 100 million and Tshs 300 million",
                          "Between Tshs 300 million and Tshs 500 million",
                          "Between Tshs 500 million and Tshs 1 billion",
                          "Between Tshs 1 billion and Tshs 2 billion",
                          "More than Tshs 2 billion"
                          ]
    net_wealth_values = {'Less than Tshs 100 million': 1,
                         'Between Tshs 100 million and Tshs 300 million': 3,
                         'Between Tshs 300 million and Tshs 500 million': 5,
                         'Between Tshs 500 million and Tshs 1 billion': 7,
                         'Between Tshs 1 billion and Tshs 2 billion': 8,
                         'More than Tshs 2 billion': 10
                         }
    net_wealth = st.radio(
        "Qn 3. What would you estimate your Net Worth to be; that is total assets less liabilities?",
        net_wealth_options,
        index=None,
    )
    # experience
    experience_options = ["I have never borrowed to invest before.",
                          "I experienced an investment loss due to borrowing.",
                          "I paid the loan but with difficulties",
                          "I was generally comfortable with this strategy.",
                          "It met my objectives for creating wealth."
                          ]
    experience_values = {'I have never borrowed to invest before.': 0,
                         'I experienced an investment loss due to borrowing.': 1,
                         'I paid the loan but with difficulties': 3,
                         'I was generally comfortable with this strategy.': 6,
                         'It met my objectives for creating wealth.': 10,
                         }
    experience = st.radio(
        "Qn 4. If you have borrowed before to invest how would you rate your experience?",
        experience_options,
        index=None,
    )

    # familiar
    familiar_options = ["Not familiar at all with investments and feel uncomfortable with the complexity.",
                        "Not very familiar when it comes to investments.",
                        "Somewhat familiar. I don’t fully understand investments, including the share-market.",
                        "Fairly familiar. I understand the various factors which influence investment performance.",
                        "Very familiar. I use research and other investment information to make investment decisions. I understand the various factors which influence investment performance."
                        ]
    familiar_values = {'Not familiar at all with investments and feel uncomfortable with the complexity.': 1,
                       'Not very familiar when it comes to investments.': 3,
                       'Somewhat familiar. I don’t fully understand investments, including the share-market.': 5,
                       'Fairly familiar. I understand the various factors which influence investment performance.': 7,
                       'Very familiar. I use research and other investment information to make investment decisions. I understand the various factors which influence investment performance.': 9,
                       }
    familiar = st.radio(
        "Qn 5. How familiar are you with investment matters?",
        familiar_options,
        index=None,
    )

    # source
    source_options = ["Margin loan",
                      "Personal injury/compensation payment.",
                      "Inheritance or gift (including prize money).",
                      "Personal savings.",
                      "Income from other investments"
                      ]
    source_values = {'Margin loan': 1,
                     'Personal injury/compensation payment.': 2,
                     'Inheritance or gift (including prize money).': 5,
                     'Personal savings.': 7,
                     'Income from other investments': 9
                     }
    source = st.radio(
        "Qn 6. What is the source of the fund you want to invest?",
        source_options,
        index=None,
    )

    # impact
    impact_options = ["I am always concerned about possible losses.",
                      "I am somewhat concerned about possible losses.",
                      "I usually consider possible gains.",
                      "I always consider possible gains."
                      ]
    impact_values = {'I am always concerned about possible losses.': 2,
                     'I am somewhat concerned about possible losses.': 4,
                     'I usually consider possible gains..': 6,
                     'I always consider possible gains.': 8
                     }
    impact = st.radio(
        "Qn 7. When considering your investments and making investment decisions, do you think about the impact of possible losses or possible gains?",
        impact_options,
        index=None,
    )

    # choice
    choice_options = ["Investment Portfolio A",
                      "Investment Portfolio B",
                      "Investment Portfolio C",
                      "Investment Portfolio D",
                      "Investment Portfolio E"
                      ]
    choice_values = {'Investment Portfolio A': 2,
                     'Investment Portfolio B': 4,
                     'Investment Portfolio C': 6,
                     'Investment Portfolio D': 8,
                     'Investment Portfolio E': 10
                     }
    choice = st.radio(
        "Qn 8. The table below shows the highest one year gain and highest one-year loss on five different hypothetical investments of Tshs 1,000,000. Given the potential gain or loss in any one year, where would you invest your money?",
        choice_options,
        index=None,
    )
    # Create a Pandas DataFrame from the portfolio options data
    df = pd.DataFrame({
        "Investment Portfolio": ["A", "B", "C", "D", "E"],
        "Highest Gain": [100000, 200000, 230000, 400000, 500000],
        "Highest Loss": [20000, 50000, 100000, 200000, 350000]
    })

    # Display the DataFrame using Streamlit
    st.dataframe(df)

    # current_own
    current_own_options = ["I don't own any investment",
                           "Cash investments",
                           "Mutual funds",
                           "Money market funds and/or securities",
                           "VBonds and/or bond funds",
                           "Stocks and/or stock funds",
                           "International securities and/or international funds"
                           ]
    current_own_values = {'I don\'t own any investment': 0,
                          'Cash investments': 1,
                          'Mutual funds': 2,
                          'Money market funds and/or securities': 3,
                          'Bonds and/or bond funds': 5,
                          'Stocks and/or stock funds': 8,
                          'International securities and/or international funds': 9,
                          }
    current_own = st.radio(
        "Qn 9. Select an investment you currently own or have owned in the past",
        current_own_options,
        index=None,
    )

    # action
    action_options = ["Sell all my shares",
                      "Sell some of my shares",
                      "Do nothing",
                      "Buy more shares due fall in price"
                      ]
    action_values = {'Sell all my shares': 1,
                     'Sell some of my shares': 4,
                     'Do nothing': 6,
                     'Buy more shares due fall in price': 10
                     }
    action = st.radio(
        "Qn 10. Imagine that in the past three months, the overall stock market lost 25\\% of its value. An individual stock investment you own also lost 25\\% of its value (that is from Tshs 1,000,000 to Tshs 750,000).",
        action_options,
        index=None,
    )

    st.write('\n')
    st.write('\n')
    st.divider()

    # ----- ADDITIONAL QUESTIONS -----

    st.header("Additional Questions")

    insured = st.radio(
        "Do you feel you are appropriately covered against personal and/or business risks such as accident, illness, trauma or death?:*", ["Yes", "No"], index=None)

    purpose = st.text_area(
        "What is the primary purpose for this portfolio? Why do you want to invest this money?")

    st.write('\n')
    st.write('\n')

    # ----- END OF FORM FOR THE USER ------

    # Generate a random UUID as a hidden variable
    hidden_variable = str(uuid.uuid4())

    # Calculate total score
    total_score = horizon_values.get(
        horizon, 0) + security_values.get(security, 0) + net_wealth_values.get(net_wealth, 0) + experience_values.get(experience, 0) + familiar_values.get(familiar, 0) + source_values.get(source, 0) + impact_values.get(impact, 0) + choice_values.get(choice, 0) + current_own_values.get(current_own, 0) + action_values.get(action, 0)

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
