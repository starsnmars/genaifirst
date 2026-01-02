from dotenv import load_dotenv
import os
from openai import AzureOpenAI
import streamlit as st
import pandas as pd
from utils import clean_text
import altair as alt

@st.cache_data
def get_response(user_prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Please answer in brief with one sentence.",
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ],
    max_completion_tokens=16384,
    #temperature=0.1,
    #max_tokens_per_request=100,
    model=deployment
)
    return response.choices[0].message.content

# Load environment variables from .env file
load_dotenv()
def get_dataset_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_dir, "data", "customer_reviews.csv")
    return csv_file_path

st.title("Hello, GenAI")
st.write("This is a my first simple Sreamlit app")
user_prompt = st.text_input("Ask me anything:", "")

#Layout two buttons side by side
col1, col2 = st.columns(2)
with col1:
    if st.button("🕹️ Ingest Dataset"):
        st.write("Ingest Clicked")
        try:
            csv_path = get_dataset_path()
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success("Dataset Loaded Successfully! 👍")
        except FileNotFoundError:
            st.error("File not found. 🤷🏼‍♂️ Please check the path and try again.")  
with col2:
    if st.button("🧹Parse Reviews"):
        if "df" in st.session_state:
            df = st.session_state["df"]
            if "cleaned_review" not in df.columns:
                df["cleaned_review"] = df["SUMMARY"].apply(clean_text)
                st.session_state["df"] = df
                st.success("Reviews Cleaned Successfully! 🧼")
            else:
                st.info("Reviews are already cleaned. ℹ️")
# Display the dataset if it exists in session state
if "df" in st.session_state:
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product:", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    st.subheader(f"📁 Dataset Preview:")
    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
        st.dataframe(filtered_df)
    else:
        filtered_df = st.session_state["df"]
        st.dataframe(st.session_state["df"])

    st.subheader("📊 Dataset Statistics:Sentiment Score by Product")
    grouped = (
    st.session_state["df"]
    .groupby("PRODUCT")["SENTIMENT_SCORE"]
    .mean()
    .reset_index()
    )

    st.bar_chart(grouped, x='PRODUCT', y='SENTIMENT_SCORE')
### Display the Altair Chart
    chart = (alt.Chart(grouped)
        .mark_bar()
        .encode(
            x='PRODUCT',
            y='SENTIMENT_SCORE',
            color='PRODUCT'
        )
        .properties(
            title='Average Sentiment Score by Product'
        )
    )
    st.altair_chart(chart, use_container_width=True)

### Add Slider for temperature
#temperature = st.slider("Select Temperature:", 0.0, 1.0, 0.7, 0.1)

endpoint = "https://pstestopenaidply-atwznrvwj734e.openai.azure.com/"
model_name = "gpt-5-mini"
deployment = "pstestopenaidply-atwznrvwj734e"

subscription_key = os.getenv("SUBSCRIPTION_KEY")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

with st.spinner("AI is Cooking..."):
    response = get_response(user_prompt)
    st.write(response)
# Display the dataset

#         },
#         {
#             "role": "user",
#             "content": user_prompt,
#         }
#     ],
#     max_completion_tokens=16384,
#     #temperature=0.1,
#     #max_tokens_per_request=100,
#     model=deployment
# )

#st.write(response.choices[0].message.content)

