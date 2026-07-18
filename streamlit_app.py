
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard",page_icon="📊",layout="wide")
st.title("📊 HR Analytics Dashboard")
st.caption("Dashboard Intelijen Bisnis")

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_HR_Analytics.csv")

df=load_data()

maps={
"Attrition":{0:"No",1:"Yes"},
"Gender":{0:"Female",1:"Male"},
"Department":{1:"Human Resources",2:"Research & Development",3:"Sales"},
"OverTime":{0:"No",1:"Yes"}
}
for c,m in maps.items():
    if c in df.columns:
        df[c]=df[c].map(m).fillna(df[c])

st.sidebar.header("Filter")
dept=st.sidebar.multiselect("Department",sorted(df["Department"].dropna().unique()),default=sorted(df["Department"].dropna().unique()))
gen=st.sidebar.multiselect("Gender",sorted(df["Gender"].dropna().unique()),default=sorted(df["Gender"].dropna().unique()))
att=st.sidebar.multiselect("Attrition",sorted(df["Attrition"].dropna().unique()),default=sorted(df["Attrition"].dropna().unique()))
f=df[df.Department.isin(dept)&df.Gender.isin(gen)&df.Attrition.isin(att)]

c1,c2,c3,c4=st.columns(4)
c1.metric("Employees",len(f))
c2.metric("Avg Age",round(f.Age.mean(),1))
c3.metric("Avg Salary",f"${f.MonthlyIncome.mean():,.0f}")
c4.metric("Attrition %",f"{(f.Attrition.eq('Yes').mean()*100):.1f}%")

st.divider()
a,b=st.columns(2)
with a:
    st.plotly_chart(px.pie(f,names="Attrition",title="Attrition",hole=.45),use_container_width=True)
with b:
    d=f.Department.value_counts().reset_index()
    d.columns=["Department","Employee"]
    st.plotly_chart(px.bar(d,x="Department",y="Employee",color="Department",text="Employee",title="Department"),use_container_width=True)

c,d=st.columns(2)
with c:
    g=f.Gender.value_counts().reset_index()
    g.columns=["Gender","Employee"]
    st.plotly_chart(px.pie(g,names="Gender",values="Employee",hole=.4,title="Gender"),use_container_width=True)
with d:
    st.plotly_chart(px.histogram(f,x="Age",color="Gender",nbins=20,title="Age Distribution"),use_container_width=True)

e,h=st.columns(2)
with e:
    st.plotly_chart(px.box(f,x="Department",y="MonthlyIncome",color="Department",title="Salary by Department"),use_container_width=True)
with h:
    st.plotly_chart(px.scatter(f,x="Age",y="MonthlyIncome",color="Department",hover_data=["JobRole"],title="Age vs Income"),use_container_width=True)

st.subheader("Data")
st.dataframe(f,use_container_width=True)
st.download_button("Download Filtered CSV",f.to_csv(index=False),"filtered_hr.csv","text/csv")
