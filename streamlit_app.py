import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# Konfigurasi Halaman
# ===============================
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 HR Analytics Dashboard")
st.markdown("### Dashboard Intelijen Bisnis")

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_HR_Analytics.csv")
    return df

df = load_data()

st.success("Dataset berhasil dimuat.")

st.write(df.head())
# ===============================
# Sidebar
# ===============================

st.sidebar.header("Filter Dashboard")

department = st.sidebar.multiselect(
    "Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

attrition = st.sidebar.multiselect(
    "Attrition",
    options=df["Attrition"].unique(),
    default=df["Attrition"].unique()
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["Attrition"].isin(attrition))
]
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Employee",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Age",
        round(filtered_df["Age"].mean(),1)
    )

with col3:
    st.metric(
        "Average Salary",
        f"${filtered_df['MonthlyIncome'].mean():,.0f}"
    )

with col4:
    attrition_rate = (
        filtered_df["Attrition"]
        .value_counts(normalize=True)
        .get("Yes",0)*100
    )

    st.metric(
        "Attrition Rate",
        f"{attrition_rate:.1f}%"
    )
    
st.markdown("## Employee Attrition")

fig = px.pie(
    filtered_df,
    names="Attrition",
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Set2
)

st.plotly_chart(fig,use_container_width=True)
# ==========================================
# Department Analysis
# ==========================================

st.markdown("---")
st.subheader("📂 Department Analysis")

col1, col2 = st.columns(2)

with col1:

    department_count = (
        filtered_df["Department"]
        .value_counts()
        .reset_index()
    )

    department_count.columns = [
        "Department",
        "Employee"
    ]

    fig = px.bar(
        department_count,
        x="Department",
        y="Employee",
        color="Department",
        text="Employee",
        title="Employee by Department"
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    with col2:

    gender_count = (
        filtered_df["Gender"]
        .value_counts()
        .reset_index()
    )

    gender_count.columns = [
        "Gender",
        "Employee"
    ]

    fig = px.pie(
        gender_count,
        names="Gender",
        values="Employee",
        hole=0.45,
        title="Gender Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    st.markdown("---")

st.subheader("🎂 Age Distribution")

fig = px.histogram(
    filtered_df,
    x="Age",
    nbins=20,
    color="Gender",
    title="Employee Age Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
