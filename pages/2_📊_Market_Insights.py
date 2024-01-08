""" An app for DSE market data visualisation """
import os
import streamlit as st
import pandas as pd
import pymysql
from streamlit_option_menu import option_menu
from pandasai import SmartDataframe
# from pandasai import BaseCallback
from pandasai.llm import OpenAI
from pandasai.responses.response_parser import ResponseParser
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(
    page_title="DSE Market Insights",
    page_icon="📊",
    layout="wide",
    # initial_sidebar_state="expanded",
)

# Load external CSS file
main_css = open("styles/main_pages.css", encoding='utf-8').read()
st.markdown(f'<style>{main_css}</style>', unsafe_allow_html=True)

# Title
st.title("DSE Market Insights")
st.write('\n')
st.write('\n')

selected = option_menu(
    menu_title=None,  # required
    options=["Home", "Market Performance", "Technical Analysis",
             "Fundamental Analysis", "Chat"],  # required
    icons=["house-fill", "bar-chart-line-fill",
           "bar-chart-line-fill", "bar-chart-line-fill", "chat-dots-fill"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
)

if selected == "Home":
    st.title(f"You have selected {selected}")
if selected == "Market Performance":
    st.title(f"You have selected {selected}")
    st.write("brian")
if selected == "Technical Analysis":
    st.title(f"You have selected {selected}")
if selected == "Fundamental Analysis":
    st.title(f"You have selected {selected}")
if selected == "Chat":
    st.title("Chat with data")

    # class StreamlitCallback(BaseCallback):
    #     def __init__(self, container) -> None:
    #         """Initialize callback handler."""
    #         self.container = container

    #     def on_code(self, response: str):
    #         self.container.code(response)

    class StreamlitResponse(ResponseParser):
        def __init__(self, context) -> None:
            super().__init__(context)

        def format_dataframe(self, result):
            st.dataframe(result["value"])
            return

        def format_plot(self, result):
            st.image(result["value"])
            return

        def format_other(self, result):
            st.write(result["value"])
            return

    # Retrieve connection details from secrets
    db_secrets = st.secrets["insights_mysql"]
    host = db_secrets["host"]
    port = db_secrets["port"]
    database = db_secrets["database"]
    user = db_secrets["username"]
    password = db_secrets["password"]

    # Establish a connection to your MySQL database
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )

    # Construct query for preview
    query2 = """
    SELECT trade_date, company_tick_name, opening_price, closing_price, high_price, 
        low_price, turnover, deals, outstanding_bids, outstanding_offers, volume, 
        market_cap
    FROM stocks_daily_report
    WHERE trade_date = '2022-12-30'
    ORDER BY company_tick_name ASC
    """

    # Establish a connection to your MySQL database using SQLAlchemy
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

    # Execute query and load data into a DataFrame
    df2 = pd.read_sql(query2, engine)

    with st.expander("🔎 Data Preview for 2022-12-30"):
        st.write(df2.tail(28))

    # Construct query for user chat
    query = """
    SELECT trade_date, company_tick_name, opening_price, closing_price, high_price, 
        low_price, turnover, deals, outstanding_bids, outstanding_offers, volume, 
        market_cap
    FROM stocks_daily_report
    WHERE trade_date BETWEEN '2018-01-01' AND '2022-12-31'
    """

    # Execute query and load data into a DataFrame
    df = pd.read_sql(query, engine)

    query3 = st.text_area("🗣️ Chat with Dataframe")
    container = st.container()

    if query3:
        llm = OpenAI(api_token=os.getenv('OPENAI_API_KEY'))
        query_engine = SmartDataframe(
            df,
            config={
                "llm": llm,
                "response_parser": StreamlitResponse,
                # "callback": StreamlitCallback(container),
            },
        )

        answer = query_engine.chat(query3)

    # # Close the database connection
    # conn.close()
    engine.dispose()
