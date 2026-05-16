# IMPORT LIBRARIES
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Tutorial Centre Dashboard",
    layout="wide"
)

# ==========================================
# LOAD DATASET
# ==========================================

# Use read_csv and tell it the separator is a tab ('\t') 
data = pd.read_csv("cleaned_dataset.xls", sep='\t')

# ==========================================
# DASHBOARD TITLE
# ==========================================

st.title("TUTORIAL CENTRE BUSINESS INTELLIGENCE DASHBOARD")

st.markdown("---")

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("FILTERS")

# Gender Filter
sex_filter = st.sidebar.multiselect(
    "Select Gender",
    options=data["Sex"].unique(),
    default=data["Sex"].unique()
)

# Exam Type Filter
exam_filter = st.sidebar.multiselect(
    "Select Exam Type",
    options=data["Exam_type"].unique(),
    default=data["Exam_type"].unique()
)

# Payment Status Filter
payment_filter = st.sidebar.multiselect(
    "Select Payment Status",
    options=data["Payment_Status"].unique(),
    default=data["Payment_Status"].unique()
)

# School Type Filter
school_filter = st.sidebar.multiselect(
    "Select School Type",
    options=data["Last_School_type"].unique(),
    default=data["Last_School_type"].unique()
)

# ==========================================
# FILTER DATASET
# ==========================================

filtered_data = data[
    (data["Sex"].isin(sex_filter)) &
    (data["Exam_type"].isin(exam_filter)) &
    (data["Payment_Status"].isin(payment_filter)) &
    (data["Last_School_type"].isin(school_filter))
]

# ==========================================
# KPI CALCULATIONS
# ==========================================

Total_Students = len(filtered_data)

Total_Revenue = filtered_data["Amount Charged"].sum()

Total_Amount_Paid = filtered_data["Amount Paid"].sum()

Total_Balance = filtered_data["Payment_Balance"].sum()

Total_Expenditure = filtered_data["Expenditure"].sum()

Gain_Before_Balance = filtered_data["Gain_b4_balance"].sum()

Gain_After_Balance = filtered_data["Gain_after_balance"].sum()

Average_BMI = round(filtered_data["BMI"].mean(), 2)

Average_Gain_Ratio1 = round(
    filtered_data["Gain_ratio1"].mean() * 100,
    2
)

Average_Gain_Ratio2 = round(
    filtered_data["Gain_ratio2"].mean() * 100,
    2
)

Payment_Completion_Rate = round(
    (Total_Amount_Paid / Total_Revenue) * 100,
    2
)

# ==========================================
# KPI SECTION
# ==========================================

st.subheader("KEY PERFORMANCE INDICATORS")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Students",
    Total_Students
)

col2.metric(
    "Total Revenue",
    f"₦{Total_Revenue:,.0f}"
)

col3.metric(
    "Amount Paid",
    f"₦{Total_Amount_Paid:,.0f}"
)

col4.metric(
    "Outstanding Balance",
    f"₦{Total_Balance:,.0f}"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Total Expenditure",
    f"₦{Total_Expenditure:,.0f}"
)

col6.metric(
    "Gain Before Balance",
    f"₦{Gain_Before_Balance:,.0f}"
)

col7.metric(
    "Gain After Balance",
    f"₦{Gain_After_Balance:,.0f}"
)

col8.metric(
    "Average BMI",
    Average_BMI
)

col9, col10, col11 = st.columns(3)

col9.metric(
    "Payment Completion Rate",
    f"{Payment_Completion_Rate}%"
)

col9.metric(
    "Payment Completion Rate",
    f"{Payment_Completion_Rate}%"
)

col10.metric(
    "Gain Ratio Before Balance",
    f"{Average_Gain_Ratio1}%"
)

col11.metric(
    "Gain Ratio After Balance",
    f"{Average_Gain_Ratio2}%"
)

st.markdown("---")

# ==========================================
# DEMOGRAPHIC ANALYSIS
# ==========================================

st.header("DEMOGRAPHIC ANALYSIS")

col12, col13 = st.columns(2)

# Gender Distribution
with col12:

    st.subheader("Gender Distribution")

    fig1, ax1 = plt.subplots()

    gender_counts = filtered_data["Sex"].value_counts()

    ax1.pie(
        gender_counts,
        labels=gender_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig1)

# Age Distribution
with col13:

    st.subheader("Age Distribution")

    fig2, ax2 = plt.subplots()

    ax2.hist(
        filtered_data["Age"],
        bins=10
    )

    ax2.set_xlabel("Age")

    ax2.set_ylabel("Frequency")

    st.pyplot(fig2)

st.markdown("---")

# ==========================================
# EXAM ANALYSIS
# ==========================================

st.header("EXAM ANALYSIS")

col14, col15 = st.columns(2)

# Exam Type Distribution
with col14:

    st.subheader("Exam Type Distribution")

    fig3, ax3 = plt.subplots(figsize=(8,5))

    sns.countplot(
        x="Exam_type",
        data=filtered_data,
        ax=ax3
    )

    plt.xticks(rotation=45)

    st.pyplot(fig3)

# Revenue by Exam Type
with col15:

    st.subheader("Revenue by Exam Type")

    revenue_exam = filtered_data.groupby(
        "Exam_type"
    )["Amount Charged"].sum()

    fig4, ax4 = plt.subplots(figsize=(8,5))

    revenue_exam.plot(
        kind="bar",
        ax=ax4
    )

    ax4.set_ylabel("Revenue")

    st.pyplot(fig4)

st.markdown("---")

# ==========================================
# PAYMENT ANALYSIS
# ==========================================

st.header("PAYMENT ANALYSIS")

col16, col17 = st.columns(2)

# Payment Status
with col16:

    st.subheader("Payment Status Distribution")

    payment_counts = filtered_data[
        "Payment_Status"
    ].value_counts()

    fig5, ax5 = plt.subplots()

    ax5.pie(
        payment_counts,
        labels=payment_counts.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig5)

# Exam Type vs Payment Status
with col17:

    st.subheader("Exam Type vs Payment Status")

    cross_tab = pd.crosstab(
        filtered_data["Exam_type"],
        filtered_data["Payment_Status"]
    )

    fig6, ax6 = plt.subplots(figsize=(8,5))

    cross_tab.plot(
        kind="bar",
        stacked=True,
        ax=ax6
    )

    st.pyplot(fig6)

st.markdown("---")

# ==========================================
# BMI ANALYSIS
# ==========================================

st.header("BMI ANALYSIS")

col18, col19 = st.columns(2)

# BMI Category
with col18:

    st.subheader("BMI Category Distribution")

    fig7, ax7 = plt.subplots(figsize=(8,5))

    sns.countplot(
        x="BMI_Category",
        data=filtered_data,
        ax=ax7
    )

    st.pyplot(fig7)

# BMI by Gender
with col19:

    st.subheader("BMI by Gender")

    fig8, ax8 = plt.subplots(figsize=(8,5))

    sns.boxplot(
        x="Sex",
        y="BMI",
        data=filtered_data,
        ax=ax8
    )

    st.pyplot(fig8)

st.markdown("---")

# ==========================================
# SCHOOL TYPE ANALYSIS
# ==========================================

st.header("SCHOOL TYPE ANALYSIS")

col20, col21 = st.columns(2)

# School Type Distribution
with col20:

    st.subheader("School Type Distribution")

    fig9, ax9 = plt.subplots(figsize=(8,5))

    sns.countplot(
        x="Last_School_type",
        data=filtered_data,
        ax=ax9
    )

    st.pyplot(fig9)

# Parent Occupation Distribution
with col21:

    st.subheader("Parent Occupation Distribution")

    occupation_counts = filtered_data[
        "Parent's_Occupation"
    ].value_counts()

    fig10, ax10 = plt.subplots(figsize=(8,6))

    occupation_counts.plot(
        kind="barh",
        ax=ax10
    )

    st.pyplot(fig10)

st.markdown("---")

# ==========================================
# FINANCIAL ANALYSIS
# ==========================================

st.header("FINANCIAL ANALYSIS")

col22, col23 = st.columns(2)

# Revenue vs Expenditure
with col22:

    st.subheader("Revenue vs Expenditure")

    finance_data = pd.Series({
        "Revenue": Total_Revenue,
        "Expenditure": Total_Expenditure
    })

    fig11, ax11 = plt.subplots()

    finance_data.plot(
        kind="bar",
        ax=ax11
    )

    st.pyplot(fig11)

# Gain Analysis
with col23:

    st.subheader("Gain Analysis")

    gain_data = pd.Series({
        "Before Balance": Gain_Before_Balance,
        "After Balance": Gain_After_Balance
    })

    fig12, ax12 = plt.subplots()

    gain_data.plot(
        kind="bar",
        ax=ax12
    )

    st.pyplot(fig12)

st.markdown("---")

# ==========================================
# DATASET DISPLAY
# ==========================================

st.header("CLEANED DATASET")

st.dataframe(filtered_data)

st.markdown("---")

# ==========================================
# FOOTER
# ==========================================

st.write(
    "Advanced Python Data Analytics Project Dashboard"
)