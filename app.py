import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Food Delivery Analytics Dashboard",
    page_icon="🍔",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.metric-container{
    background:#1E293B;
    padding:15px;
    border-radius:15px;
}

h1,h2,h3{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/onlinefoods.csv")

    if "Unnamed: 12" in df.columns:
        df.drop(columns=["Unnamed: 12"], inplace=True)

    df["Feedback"] = df["Feedback"].str.strip()

    return df

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🔍 Filters")

gender_filter = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

occupation_filter = st.sidebar.multiselect(
    "Occupation",
    df["Occupation"].unique(),
    default=df["Occupation"].unique()
)

feedback_filter = st.sidebar.multiselect(
    "Feedback",
    df["Feedback"].unique(),
    default=df["Feedback"].unique()
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (
        int(df["Age"].min()),
        int(df["Age"].max())
    )
)

# ==================================================
# FILTERING
# ==================================================

filtered = df[
    (df["Gender"].isin(gender_filter))
    & (df["Occupation"].isin(occupation_filter))
    & (df["Feedback"].isin(feedback_filter))
    & (df["Age"].between(age_range[0], age_range[1]))
]

# ==================================================
# HEADER
# ==================================================

st.title("🍔 Food Delivery Customer Analytics")

st.markdown("""
Comprehensive analysis of customer demographics,
behavior and feedback patterns.
""")

# ==================================================
# KPI SECTION
# ==================================================

positive_rate = round(
    (
        len(filtered[filtered["Feedback"]=="Positive"])
        / len(filtered)
    ) * 100,
    2
)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        len(filtered)
    )

with col2:
    st.metric(
        "Average Age",
        round(filtered["Age"].mean(),1)
    )

with col3:
    st.metric(
        "Avg Family Size",
        round(filtered["Family size"].mean(),1)
    )

with col4:
    st.metric(
        "Positive Feedback %",
        f"{positive_rate}%"
    )

# ==================================================
# DEMOGRAPHICS
# ==================================================

st.subheader("👨‍👩‍👧 Customer Demographics")

col1,col2 = st.columns(2)

with col1:

    fig = px.pie(
        filtered,
        names="Gender",
        title="Gender Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        filtered,
        names="Marital Status",
        title="Marital Status"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# EDUCATION
# ==================================================

st.subheader("🎓 Educational Qualifications")

edu = (
    filtered["Educational Qualifications"]
    .value_counts()
    .reset_index()
)

edu.columns = ["Education","Count"]

fig = px.bar(
    edu,
    x="Education",
    y="Count",
    title="Education Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# OCCUPATION
# ==================================================

st.subheader("💼 Occupation Analysis")

occ = (
    filtered["Occupation"]
    .value_counts()
    .reset_index()
)

occ.columns = ["Occupation","Count"]

fig = px.bar(
    occ,
    x="Occupation",
    y="Count",
    title="Occupation Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# INCOME ANALYSIS
# ==================================================

st.subheader("💰 Income Analysis")

income = (
    filtered["Monthly Income"]
    .value_counts()
    .reset_index()
)

income.columns = ["Income","Count"]

fig = px.bar(
    income,
    x="Income",
    y="Count",
    title="Income Segmentation"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# FEEDBACK ANALYSIS
# ==================================================

st.subheader("⭐ Customer Feedback")

feedback = (
    filtered["Feedback"]
    .value_counts()
    .reset_index()
)

feedback.columns = ["Feedback","Count"]

fig = px.bar(
    feedback,
    x="Feedback",
    y="Count",
    title="Feedback Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# FEEDBACK BY GENDER
# ==================================================

st.subheader("📊 Feedback by Gender")

fig = px.histogram(
    filtered,
    x="Gender",
    color="Feedback",
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# AGE DISTRIBUTION
# ==================================================

st.subheader("📈 Age Distribution")

fig = px.histogram(
    filtered,
    x="Age",
    nbins=20,
    title="Customer Age Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# FAMILY SIZE ANALYSIS
# ==================================================

st.subheader("🏠 Family Size Analysis")

fig = px.box(
    filtered,
    x="Feedback",
    y="Family size",
    title="Family Size vs Feedback"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# GEOGRAPHICAL ANALYSIS
# ==================================================

st.subheader("🗺 Customer Location Map")

fig = px.scatter_mapbox(
    filtered,
    lat="latitude",
    lon="longitude",
    hover_name="Occupation",
    hover_data=["Age","Gender"],
    zoom=10
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0,r=0,t=0,b=0)
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# CORRELATION
# ==================================================

st.subheader("📉 Correlation Analysis")

numeric_cols = [
    "Age",
    "Family size",
    "latitude",
    "longitude"
]

corr = filtered[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# CUSTOMER SEGMENTS
# ==================================================

st.subheader("🎯 Customer Segmentation Insights")

age_group = pd.cut(
    filtered["Age"],
    bins=[15,20,25,30,35],
    labels=["15-20","21-25","26-30","31-35"]
)

segment = (
    filtered.groupby(age_group)
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    segment,
    x="Age",
    y="Count",
    title="Customer Age Segments"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# BUSINESS INSIGHTS
# ==================================================

st.subheader("💡 Business Insights")

top_occupation = filtered["Occupation"].mode()[0]
top_income = filtered["Monthly Income"].mode()[0]
top_education = filtered["Educational Qualifications"].mode()[0]

st.success(f"""
### Executive Insights

• Most customers belong to: **{top_occupation}**

• Dominant income group: **{top_income}**

• Most common education level:
**{top_education}**

• Positive feedback rate:
**{positive_rate}%**

• Customer demographics indicate the
largest market segment for targeted campaigns.

• Geographic clustering helps identify
high-demand delivery zones.

• Family-size trends reveal household ordering behavior.
""")

# ==================================================
# DOWNLOAD DATA
# ==================================================

st.subheader("⬇ Download Filtered Data")

csv = filtered.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    file_name="filtered_customers.csv",
    mime="text/csv"
)

# ==================================================
# RAW DATA
# ==================================================

with st.expander("View Dataset"):
    st.dataframe(
        filtered,
        use_container_width=True
    )
