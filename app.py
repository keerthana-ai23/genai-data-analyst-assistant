import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="GenAI-Powered Data Analyst Assistant",
    layout="wide"
)

# -------------------------------
# GEMINI CONFIG
# -------------------------------

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# -------------------------------
# TITLE
# -------------------------------

st.title("🤖 GenAI-Powered Data Analyst Assistant")

st.write(
    "Upload any CSV file and receive automated analysis, visualizations, AI insights, and recommendations."
)

# -------------------------------
# FILE UPLOAD
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # -------------------------------
    # DATASET PREVIEW
    # -------------------------------

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # -------------------------------
    # DATASET SHAPE
    # -------------------------------

    st.subheader("📊 Dataset Shape")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # -------------------------------
    # MISSING VALUES
    # -------------------------------

    st.subheader("⚠ Missing Values")

    missing_df = pd.DataFrame(
        df.isnull().sum(),
        columns=["Missing Values"]
    )

    st.dataframe(missing_df)

    # -------------------------------
    # DUPLICATES
    # -------------------------------

    st.subheader("🔁 Duplicate Records")

    duplicate_count = df.duplicated().sum()

    st.metric(
        "Duplicate Rows",
        duplicate_count
    )

    # -------------------------------
    # COLUMN INFORMATION
    # -------------------------------

    st.subheader("📝 Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(info_df)

    st.subheader("📋 Dataset Columns")

    st.write(list(df.columns))

    # -------------------------------
    # DATASET STATISTICS
    # -------------------------------

    st.subheader("📈 Dataset Statistics")

    try:
        st.dataframe(
            df.describe(include="all")
        )
    except:
        st.dataframe(
            df.describe()
        )

    # -------------------------------
    # HEALTH SCORE
    # -------------------------------

    st.subheader("💚 Dataset Health Score")

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    health_score = round(
        ((total_cells - missing_cells) / total_cells) * 100,
        2
    )

    st.metric(
        "Health Score",
        f"{health_score}%"
    )

    # -------------------------------
    # VISUALIZATION
    # -------------------------------

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_cols) > 0:

        st.subheader("📉 Histogram")

        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        fig, ax = plt.subplots(
            figsize=(8, 4)
        )

        df[selected_col].hist(
            ax=ax
        )

        ax.set_title(
            f"Distribution of {selected_col}"
        )

        st.pyplot(fig)

        # -------------------------------
        # BOX PLOT
        # -------------------------------

        st.subheader("📦 Box Plot")

        fig, ax = plt.subplots(
            figsize=(8, 4)
        )

        sns.boxplot(
            x=df[selected_col],
            ax=ax
        )

        st.pyplot(fig)

    # -------------------------------
    # CORRELATION HEATMAP
    # -------------------------------

    if len(numeric_cols) > 1:

        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        st.pyplot(fig)

    # -------------------------------
    # AI SUMMARY
    # -------------------------------

    st.subheader("🤖 AI Dataset Summary")

    if st.button("Generate AI Summary"):

        try:

            with st.spinner(
                "Generating AI insights..."
            ):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                sample_data = (
                    df.head(20)
                    .to_string()
                )

                prompt = f"""
                Analyze this dataset:

                {sample_data}

                Provide:

                1. Dataset Overview
                2. Key Trends
                3. Data Quality Issues
                4. Business Recommendations
                5. Important Insights
                """

                response = model.generate_content(
                    prompt
                )

                st.success(
                    "AI Summary Generated"
                )

                st.write(
                    response.text
                )

        except Exception as e:
            st.error(str(e))

    # -------------------------------
    # ASK GEMINI
    # -------------------------------

    st.subheader(
        "💬 Ask Questions About Your Dataset"
    )

    with st.form("chat_form"):

        question = st.text_input(
            "Ask anything about your uploaded dataset"
        )

        submit = st.form_submit_button(
            "Ask Gemini"
        )

    if submit and question:

        try:

            with st.spinner(
                "Thinking..."
            ):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                sample_data = (
                    df.head(50)
                    .to_string()
                )

                prompt = f"""
                Dataset:

                {sample_data}

                User Question:

                {question}

                Answer clearly and professionally.
                """

                response = model.generate_content(
                    prompt
                )

                st.success(
                    "Answer Generated"
                )

                st.write(
                    response.text
                )

        except Exception as e:
            if "429" in str(e):
                st.error(
                    "Gemini free quota exceeded. Please try again later or use a new API key."
                    )
            else:
                st.error(str(e))
    # -------------------------------
    # DOWNLOAD REPORT
    # -------------------------------

    st.subheader(
        "⬇ Download Analysis Report"
    )

    report = (
        df.describe(
            include="all"
        )
        .to_csv()
    )

    st.download_button(
        label="Download Report",
        data=report,
        file_name="analysis_report.csv",
        mime="text/csv"
    )

else:

    st.info(
        "Please upload a CSV file to begin analysis."
    )