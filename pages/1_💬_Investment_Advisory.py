""" Investment advisory app, takes users profile and chats with AI advisor """
import uuid
import time
import os
import json
import pandas as pd
from sqlalchemy import text
import streamlit as st
import openai
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(
    page_title="Investment Advisory",
    page_icon="💬",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

# Load external CSS file
main_css = open("styles/main_pages.css", encoding='utf-8').read()
st.markdown(f'<style>{main_css}</style>', unsafe_allow_html=True)

#### ---- INVESTOR FORM -----########


def user_details():
    """
    Captures and processes user details for investment advisory form.

    This function displays the form and gathers the following information from the user:
        * Full name
        * Amount to invest
        * Gender
        * Age
        * Location
        * Phone number
        * Email address
        * Occupation
        * Risk profile questions
            * Investment horizon
            * Income security
            * Net worth
            * Investment experience
            * Investment familiarity
            * Source of funds
            * Focus on potential gains vs. losses
            * Choice of investment portfolio
            * Current investment holdings
            * Action taken during market downturn
        * Additional questions
            * Insurance coverage
            * Purpose for the portfolio

    The function validates the user input and saves the information to a database.
    It also calculates the total risk score based on the user's responses to the risk profile questions.
    It also generates a unique id for each client.

    Returns:
        None
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

    # net_wealth
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

    # Generate a random UUID as a investor_uuid (to identify investor)
    investor_uuid = str(uuid.uuid4())

    # Calculate total score
    total_score = horizon_values.get(
        horizon, 0) + security_values.get(security, 0) + net_wealth_values.get(net_wealth, 0) + experience_values.get(experience, 0) + familiar_values.get(familiar, 0) + source_values.get(source, 0) + impact_values.get(impact, 0) + choice_values.get(choice, 0) + current_own_values.get(current_own, 0) + action_values.get(action, 0)

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    def callback():
        if not full_name or not amount_to_invest or not gender or not age or not location or not phone_number or not email or not occupation or not horizon or not security or not net_wealth or not experience or not familiar or not source or not impact or not choice or not current_own or not action or not insured or not purpose:
            st.warning("Please fill in all fields.")
            return

        st.session_state.button_clicked = True
        st.session_state.step = "Chat"

        st.session_state.full_name = full_name
        st.session_state.amount_to_invest = amount_to_invest
        st.session_state.gender = gender
        st.session_state.age = age
        st.session_state.location = location
        st.session_state.phone_number = phone_number
        st.session_state.email = email
        st.session_state.occupation = occupation
        st.session_state.horizon = horizon
        st.session_state.security = security
        st.session_state.net_wealth = net_wealth
        st.session_state.experience = experience
        st.session_state.familiar = familiar
        st.session_state.source = source
        st.session_state.impact = impact
        st.session_state.choice = choice
        st.session_state.current_own = current_own
        st.session_state.action = action
        st.session_state.insured = insured
        st.session_state.purpose = purpose
        st.session_state.investor_uuid = investor_uuid
        st.session_state.total_score = total_score

        # Create a dictionary with the user details
        user_details_dict = {
            "full_name": full_name,
            "amount_to_invest": amount_to_invest,
            "gender": gender,
            "age": age,
            "location": location,
            "phone_number": phone_number,
            "email": email,
            "occupation": occupation,
            "horizon": horizon,
            "security": security,
            "net_wealth": net_wealth,
            "experience": experience,
            "familiar": familiar,
            "source": source,
            "impact": impact,
            "choice": choice,
            "current_own": current_own,
            "action": action,
            "insured": insured,
            "purpose": purpose,
            "investor_uuid": investor_uuid,
            "total_score": total_score,
        }

        save_to_database(**user_details_dict)

    if (
        st.button(label="Done") or st.session_state.button_clicked
    ):
        # Process user details and move to the next step
        if st.button("Submit Form",
                     on_click=callback):
            # st.balloons()
            st.session_state.step = "Chat"
            if st.session_state.step == "Chat":
                chat(full_name, amount_to_invest, gender, age, location, phone_number, email, occupation, horizon, security, net_wealth,
                     experience, familiar, source, impact, choice, current_own, action, insured, purpose, investor_uuid, total_score)

    warning_message = "<div style='color: red;'>Please fill all the fields, if not, the submit button would disappear</div>"
    st.markdown(warning_message, unsafe_allow_html=True)

##### ------- SEND FORM DATA TO DATABASE -------######


def save_to_database(full_name, amount_to_invest, gender, age,
                     location, phone_number, email, occupation, horizon, security, net_wealth,
                     experience, familiar, source, impact, choice, current_own, action,
                     insured, purpose, investor_uuid, total_score):
    """
    Saves investor data to the MySQL database.

    Args:
        full_name (str): Full name of the investor
        amount_to_invest (str): Amount the investor intends to invest
        gender (str): Gender of the investor
        age (str): Age of the investor
        location (str): Location of the investor
        phone_number (str): Phone number of the investor
        email (str): Email address of the investor
        occupation (str): Occupation of the investor
        horizon (str): Investment horizon of the investor
        security (str): Security preferences of the investor
        net_wealth (str): Net wealth of the investor
        experience (str): Investment experience of the investor
        familiar (str): Familiarity with crypto investments
        source (str): Source of information about the advisory service
        impact (str): Importance of impact investing
        choice (str): Preferred investment choice
        current_own (str): Currently owned investments
        action (str): Preferred next action
        insured (str): Preference for insurance
        purpose (str): Purpose of investment
        investor_uuid (str): Unique identifier for the investor
        total_score (str): Total score from the risk assessment

    Returns:
        None

    Raises:
        Exception: If any errors occur while saving data to the database.
    """
    try:
        # Display a spinner while sending data
        with st.spinner("Sending data to MySQL database..."):
            # Establish a connection to MySQL
            conn = st.connection('advisory_client_mysql', type='sql')

            # Convert variables from string to interger
            amount_to_invest_int = int(amount_to_invest)
            age_int = int(age)
            total_score_int = int(total_score)

            with conn.session as s:
                # Prepare the data to be sent to MySQL
                data = {
                    "full_name": [full_name],
                    "amount_to_invest_int": [amount_to_invest_int],
                    "gender": [gender],
                    "age_int": [age_int],
                    "location": [location],
                    "phone_number": [phone_number],
                    "email": [email],
                    "occupation": [occupation],
                    "horizon": [horizon],
                    "security": [security],
                    "net_wealth": [net_wealth],
                    "experience": [experience],
                    "familiar": [familiar],
                    "source": [source],
                    "impact": [impact],
                    "choice": [choice],
                    "current_own": [current_own],
                    "action": [action],
                    "insured": [insured],
                    "purpose": [purpose],
                    "investor_uuid": [investor_uuid],
                    "total_score_int": [total_score_int],
                }

                for i in range(len(data["full_name"])):
                    s.execute(
                        text('INSERT INTO investor_profile (full_name, amount_to_invest_int, gender, age_int, location, phone_number, email, occupation, horizon, security, net_wealth, experience, familiar, source, impact, choice, current_own, action, insured, purpose, investor_uuid, total_score_int) VALUES (:full_name, :amount_to_invest_int, :gender, :age_int, :location, :phone_number, :email, :occupation, :horizon, :security, :net_wealth, :experience, :familiar, :source, :impact, :choice, :current_own, :action, :insured, :purpose, :investor_uuid, :total_score_int);'),
                        params={
                            "full_name": data["full_name"][i],
                            "amount_to_invest_int": data["amount_to_invest_int"][i],
                            "gender": data["gender"][i],
                            "age_int": data["age_int"][i],
                            "location": data["location"][i],
                            "phone_number": data["phone_number"][i],
                            "email": data["email"][i],
                            "occupation": data["occupation"][i],
                            "horizon": data["horizon"][i],
                            "security": data["security"][i],
                            "net_wealth": data["net_wealth"][i],
                            "experience": data["experience"][i],
                            "familiar": data["familiar"][i],
                            "source": data["source"][i],
                            "impact": data["impact"][i],
                            "choice": data["choice"][i],
                            "current_own": data["current_own"][i],
                            "action": data["action"][i],
                            "insured": data["insured"][i],
                            "purpose": data["purpose"][i],
                            "investor_uuid": data["investor_uuid"][i],
                            "total_score_int": data["total_score_int"][i],
                        }
                    )

                s.commit()

            # st.success("Data successfully processed.")

    except Exception as e:
        st.error(f"Error: {e}")


def chat(full_name, amount_to_invest, gender, age, location, phone_number, email, occupation, horizon, security, net_wealth,
         experience, familiar, source, impact, choice, current_own, action, insured, purpose, investor_uuid, total_score):
    """
    This function facilitates a chat conversation between the user and an OpenAI Assistant.

    Args:
        full_name (str): Full name of the user.
        amount_to_invest (str): Amount the user intends to invest.
        gender (str): Gender of the user.
        age (int): Age of the user.
        location (str): User's location.
        phone_number (str): User's phone number.
        email (str): User's email address.
        occupation (str): User's occupation.
        horizon (int): Investment horizon chosen by the user.
        security (int): User's income security rating.
        net_wealth (int): User's estimated net worth.
        experience (int): User's experience with investing.
        familiar (int): Level of user's familiarity with investment matters.
        source (str): Source of the funds the user wants to invest.
        impact (str): User's preference for considering potential losses or gains.
        choice (str): User's investment choice based on a hypothetical scenario.
        current_own (str): Investment currently owned by the user.
        action (str): User's action towards a hypothetical market loss scenario.
        insured (str): User's insurance coverage status.
        purpose (str): User's primary purpose for investing.
        investor_uuid (str): Unique identifier for the investor.
        total_score (float): Total score obtained from the user's responses.

    Returns:
        None: This function doesn't return any value, but it updates the state of the conversation with the assistant.
    """

    received_variables = {
        "My Full Name:": full_name,
        "Amount to invest (TZS):": amount_to_invest,
        "My Gender": gender,
        "Age": age,
        "location": location,
        "occupation": occupation,
        "Qn 1. How long would you invest the majority of your money before you think you would need access to it? My answer": horizon,
        "Qn 2. How secure is your current and future income from sources such as salary, pensions or other investments? My answer": security,
        "Qn 3. What would you estimate your Net Worth to be; that is total assets less liabilities? My answer": net_wealth,
        "Qn 4. If you have borrowed before to invest how would you rate your experience? My answer": experience,
        "Qn 5. How familiar are you with investment matters? My answer": familiar,
        "Qn 6. What is the source of the fund you want to invest? My answer": source,
        "Qn 7. When considering your investments and making investment decisions, do you think about the impact of possible losses or possible gains? My answer": impact,
        "Qn 8. The table below shows the highest one year gain and highest one-year loss on five different hypothetical investments of Tshs 1,000,000. Given the potential gain or loss in any one year, where would you invest your money? My answer": choice,
        "Qn 9. Select an investment you currently own or have owned in the past My answer": current_own,
        "Qn 10. Imagine that in the past three months, the overall stock market lost 25\\% of its value. An individual stock investment you own also lost 25\\% of its value (that is from Tshs 1,000,000 to Tshs 750,000). My answer": action,
        "Do you feel you are appropriately covered against personal and/or business risks such as accident, illness, trauma or death? My answer": insured,
        "What is the primary purpose for this portfolio? Why do you want to invest this money? My answer": purpose,
        "total_score My answer:": total_score
    }

    investor_statement = {key: value for key,
                          value in received_variables.items() if value is not None}

    investor_statement_string = json.dumps(investor_statement)

    assistant_instruction = """
    you are an investment advisor based in Tanzania for clients who have money to invest in the Tanzanian capital market and they need to know the strategy they use to invest, where to invest and also mostly of these clients do not have knowledge about the Tanzania capital market, you will respond to their questions that seeks to understand the tanzanian capital market. The ares of focus are the stock market (Dar es Salaam Stock Exchange), commercial banks (cash investments such as fixed deposits) and the Bank of Tanzania (government bonds and government bills)
    you will be as a chatbot in the application, but before an investor gets to you, they must first fill the form to determine their investor profile. Among the documents attached, there is an investor profile questionnaire pdf, this pdf is the inspiration of the form investors will fill. from the pdf you can see different investor profiles based on the total score from a series of multiple choices, where each choice carries a mask. there are five profiles; Conservative (score 0 to 20), moderate (score 21 to 40), balanced (score 41 to 60), Assertive/Growth (score 61 to 80) and Aggressive (score 81 to 100).
    so, before an investor chats with you, they will first share their details, all risk profile questions and their answers, additional questions and answers and their total score. and this is what you will do;
    1. Introduction:
    - Greet and welcome the investor, introducing yourself as an Artificial Intelligent Investment Advisor with in-depth knowledge of the Tanzanian capital market.
    - Assure them that their data is secure.

    2. Investor Profile:
    - Based on their total score, categorize them into one of five investor profiles: Conservative, Moderate, Balanced, Assertive/Growth, or Aggressive (as indicated on the investor profile questionnaire pdf in the files).
    - Provide a brief description and investment strategy for their respective profile.
    - Suggest an allocation strategy for the amount they want to invest and give examples of investment securities available in the Tanzanian capital market.

    3. Insights Based on Score:
    - Explain that the total score provides a general overview.
    - Briefly outline the factors contributing to their score.
    - Clarify that the advice is based on a general perspective.

    4. Detailed Advice:
    provide more advice based on:
    - Consider their investment horizon: Suggest equity market for long-term (>2 years) investments, emphasizing knowledge requirements.
    - Assess occupation-related risks: In case of significant risks, inquire about life insurance and recommend subscribing before investing.
    - Evaluate the primary purpose for the portfolio: Provide tailored advice on the best-fit investment based on their goals.
    """
    # Your chat interface here
    st.title("Chat with your Investment Advisor")
    st.text("You can start by asking: What is my investor profile?")
    st.text("What is my investment strategy?")

    st.write('\n')
    st.divider()

    # Set your OpenAI Assistant ID here
    assistant_id = os.getenv('ASSISTANT_ID')

    # Initialize the OpenAI client (ensure to set your API key in the sidebar within the app)
    client = openai

    # Initialize session state variables for file IDs and chat control
    if "file_id_list" not in st.session_state:
        st.session_state.file_id_list = []

    if "start_chat" not in st.session_state:
        st.session_state.start_chat = True

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    # Get the OPENAI API Key
    openai_api_key_env = os.getenv('OPENAI_API_KEY')
    openai_api_key = openai_api_key_env

    if openai_api_key:
        openai.api_key = openai_api_key

    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id
    # st.write("thread id: ", thread.id)

    # Define the function to process messages with citations

    def process_message_with_citations(message):
        message_content = message.content[0].text.value
        return message_content

        # Send the initial message from investor_statement
    if investor_statement_string:
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=investor_statement_string
        )

    # Only show the chat interface if the chat has been started
    if st.session_state.start_chat:
        # st.write(getStockPrice('AAPL'))
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display existing messages in the chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input for the user
        if prompt := st.chat_input("How can I help you?"):
            # Add user message to the state and display it
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add the user's message to the existing thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )

            # Create a run with additional instructions
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_id,
                instructions=assistant_instruction
            )

            # Poll for the run to complete and retrieve the assistant's messages
            while run.status not in ["completed", "failed"]:
                st.sidebar.write(run.status)
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
            st.sidebar.write(run.status)

            # Retrieve messages added by the assistant
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )

            # Process and display assistant messages
            assistant_messages_for_run = [
                message for message in messages
                if message.run_id == run.id and message.role == "assistant"
            ]
            for message in assistant_messages_for_run:
                full_response = process_message_with_citations(message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response})
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)


def main():
    """
    This function manages the main flow of the application.

    **Steps:**

    1. **Check session state for current step:**
        - If "step" is not found, set it to "User Details".
    2. **Execute the appropriate function based on the current step:**
        - If "step" is "User Details":
            - Call the `user_details` function to collect user information.
        - If "step" is "Chat":
            - Call the `chat` function with user information stored in session state.
    """
    if "step" not in st.session_state:
        st.session_state.step = "User Details"

    if st.session_state.step == "User Details":
        user_details()
    elif st.session_state.step == "Chat":
        chat(st.session_state.full_name,
             st.session_state.amount_to_invest,
             st.session_state.gender,
             st.session_state.age,
             st.session_state.location,
             st.session_state.phone_number,
             st.session_state.email,
             st.session_state.occupation,
             st.session_state.horizon,
             st.session_state.security,
             st.session_state.net_wealth,
             st.session_state.experience,
             st.session_state.familiar,
             st.session_state.source,
             st.session_state.impact,
             st.session_state.choice,
             st.session_state.current_own,
             st.session_state.action,
             st.session_state.insured,
             st.session_state.purpose,
             st.session_state.investor_uuid,
             st.session_state.total_score)


if __name__ == "__main__":
    main()
