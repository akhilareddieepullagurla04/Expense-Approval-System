import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Initialize session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

menu = st.sidebar.selectbox(
    "Menu",
    ["Submit", "View", "Approve/Reject", "Summary"]
)

# -------- Submit -------- #
if menu == "Submit":
    st.subheader("Submit Expense")

    amount = st.number_input("Amount")
    category = st.selectbox(
    "Category",
    ["Food", "Travel", "Rent", "Shopping", "Bills", "Medical", "Other"]
)

    if st.button("Submit"):
        st.session_state["expenses"].append({
            "amount": amount,
            "category": category,
            "status": "Pending"
        })
        st.success("Expense added!")

# -------- View -------- #
elif menu == "View":
    st.subheader("View Expenses")
    st.write(st.session_state["expenses"])

# -------- Approve -------- #
elif menu == "Approve/Reject":
    st.subheader("Approve / Reject")

    data = st.session_state["expenses"]

    if len(data) == 0:
        st.warning("No expenses to review")
    else:
        for i, expense in enumerate(data):
            st.write(f"{expense['category']} - ₹{expense['amount']} - {expense['status']}")

            col1, col2 = st.columns(2)

            if col1.button(f"Approve {i}"):
                st.session_state["expenses"][i]["status"] = "Approved"

            if col2.button(f"Reject {i}"):
                st.session_state["expenses"][i]["status"] = "Rejected"

# -------- Summary -------- #
elif menu == "Summary":
    st.subheader("📊 Dashboard")

    data = st.session_state["expenses"]

    if len(data) == 0:
        st.warning("No data available")
    else:
        df = pd.DataFrame(data)
        approved_df = df[df["status"] == "Approved"]

        if approved_df.empty:
            st.warning("No approved expenses yet")
        else:
            total_expense = approved_df["amount"].sum()
            income = 50000
            balance = income - total_expense

            st.success("Summary Generated Successfully ✅")
            st.write(f"Total Income: {income}")
            st.write(f"Total Expense: {total_expense}")
            st.write(f"Balance: {balance}")

            category_sum = approved_df.groupby("category")["amount"].sum()

            fig, ax = plt.subplots()
            ax.bar(category_sum.index, category_sum.values)
            st.pyplot(fig)
