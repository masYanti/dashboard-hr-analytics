import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 HR Analytics Dashboard")
st.subheader("Dashboard Intelijen Bisnis")

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_HR_Analytics.csv")

df = load_data()

# =========================
# Decode Data
# =========================

df["Department"] = df["Department"].replace({
    1: "Human Resources",
    2: "Research & Development",
    3: "Sales"
})

df["Gender"] = df["Gender"].replace({
    0: "Female",
    1: "Male"
})

df["Attrition"] = df["Attrition"].replace({
    0: "No",
    1: "Yes"
})

df["OverTime"] = df["OverTime"].replace({
    0: "No",
    1: "Yes"
})

# =========================
# Sidebar
# =========================

st.sidebar.header("Filter")

dept = st.sidebar.multiselect(
    "Department",
    options=df["Department"].dropna().unique().tolist(),
    default=df["Department"].dropna().unique().tolist()
)

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].dropna().unique().tolist(),
    default=df["Gender"].dropna().unique().tolist()
)

attrition = st.sidebar.multiselect(
    "Attrition",
    options=df["Attrition"].dropna().unique().tolist(),
    default=df["Attrition"].dropna().unique().tolist()
)

filtered_df = df[
    (df["Department"].isin(dept)) &
    (df["Gender"].isin(gender)) &
    (df["Attrition"].isin(attrition))
]

# =========================
# KPI
# =========================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("Total Employee",len(filtered_df))

with c2:
    st.metric("Average Age",round(filtered_df["Age"].mean(),1))

with c3:
    st.metric(
        "Average Salary",
        f"${filtered_df['MonthlyIncome'].mean():,.0f}"
    )

with c4:
    rate = (
        filtered_df["Attrition"]
        .eq("Yes")
        .mean()*100
    )
    st.metric(
        "Attrition Rate",
        f"{rate:.1f}%"
    )

st.divider()

# =========================
# Pie Chart
# =========================

col1,col2 = st.columns(2)

with col1:

    fig = px.pie(
        filtered_df,
        names="Attrition",
        hole=.45,
        title="Employee Attrition"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    dep = (
        filtered_df["Department"]
        .value_counts()
        .reset_index()
    )

    dep.columns=[
        "Department",
        "Employee"
    ]

    fig = px.bar(
        dep,
        x="Department",
        y="Employee",
        color="Department",
        text="Employee",
        title="Employee by Department"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# Gender
# =========================

col1,col2 = st.columns(2)

with col1:

    gen = (
        filtered_df["Gender"]
        .value_counts()
        .reset_index()
    )

    gen.columns=[
        "Gender",
        "Employee"
    ]

    fig = px.pie(
        gen,
        names="Gender",
        values="Employee",
        hole=.45,
        title="Gender Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.histogram(
        filtered_df,
        x="Age",
        color="Gender",
        nbins=20,
        title="Age Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# Salary
# =========================

fig = px.box(
    filtered_df,
    x="Department",
    y="MonthlyIncome",
    color="Department",
    title="Salary by Department"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Scatter
# =========================

fig = px.scatter(
    filtered_df,
    x="Age",
    y="MonthlyIncome",
    color="Department",
    title="Age vs Monthly Income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Data
# =========================

st.subheader("Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.download_button(
    "Download CSV",
    filtered_df.to_csv(index=False),
    "filtered_hr.csv",
    "text/csv"
)
