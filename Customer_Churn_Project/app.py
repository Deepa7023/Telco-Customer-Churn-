import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# -------- Load and Clean Data --------
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Asus\Downloads\Customer_Churn_Project\UseC-Telco-Customer-Churn.csv")
    # Convert TotalCharges to numeric and fill missing values
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    # Encode target variable
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    # Drop customerID as it's not needed
    if 'customerID' in df.columns:
        df.drop(columns='customerID', inplace=True)
    return df

data = load_data()

# -------- Page Setup --------
st.set_page_config(page_title="Telco Churn Dashboard", layout="wide")
st.title("📊 Telco Customer Churn Dashboard")

# -------- Key Metrics --------
col1, col2, col3 = st.columns(3)
col1.metric("Churn Rate", f"{data['Churn'].mean()*100:.2f}%")
col2.metric("Average Tenure", f"{data['tenure'].mean():.1f} months")
col3.metric("Average Monthly Charge", f"${data['MonthlyCharges'].mean():.2f}")

# -------- Filters --------
st.sidebar.header("Filter Customers")
selected_contracts = st.sidebar.multiselect("Contract Type", data['Contract'].unique(), default=data['Contract'].unique())
selected_payment = st.sidebar.multiselect("Payment Method", data['PaymentMethod'].unique(), default=data['PaymentMethod'].unique())
selected_senior = st.sidebar.multiselect("Senior Citizen", [0,1], default=[0,1])
selected_internet = st.sidebar.multiselect("Internet Service", data['InternetService'].unique(), default=data['InternetService'].unique())

# Apply filters to the dataset
filtered_data = data[
    (data['Contract'].isin(selected_contracts)) &
    (data['PaymentMethod'].isin(selected_payment)) &
    (data['SeniorCitizen'].isin(selected_senior)) &
    (data['InternetService'].isin(selected_internet))
]

# -------- Visualizations --------

# 1. Churn by Contract
st.markdown("### Churn by Contract Type")
contract_churn = filtered_data.groupby('Contract')['Churn'].mean().reset_index()
fig1 = px.bar(contract_churn, x='Contract', y='Churn', text_auto=True, labels={'Churn':'Churn Rate'})
st.plotly_chart(fig1, use_container_width=True)

# 2. Monthly Charges vs Churn
st.markdown("### Monthly Charges Distribution by Churn")
fig2 = px.histogram(filtered_data, x='MonthlyCharges', color='Churn', nbins=30,
                    barmode='overlay', labels={'Churn':'Churn'})
st.plotly_chart(fig2, use_container_width=True)

# 3. Tenure vs Churn
st.markdown("### Churn Rate by Tenure")
tenure_churn = filtered_data.groupby('tenure')['Churn'].mean().reset_index()
fig3 = px.line(tenure_churn, x='tenure', y='Churn', labels={'Churn':'Churn Rate'})
st.plotly_chart(fig3, use_container_width=True)

# 4. Correlation Heatmap
st.markdown("### Correlation Between Features")
numeric_cols = filtered_data.select_dtypes(include='number')
fig4, ax = plt.subplots(figsize=(10,6))
sns.heatmap(numeric_cols.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig4)

# 5. Churn by Internet Service
st.markdown("### Churn by Internet Service")
internet_churn = filtered_data.groupby('InternetService')['Churn'].mean().reset_index()
fig5 = px.bar(internet_churn, x='InternetService', y='Churn', text_auto=True, labels={'Churn':'Churn Rate'})
st.plotly_chart(fig5, use_container_width=True)

# -------- Key Takeaways --------
st.markdown("## 💡 Key Insights")
st.markdown("""
1. Customers with month-to-month contracts are the most likely to churn.
2. Higher monthly charges seem to increase the risk of churn.
3. Senior citizens using fiber optic internet show a higher churn tendency.
""")


