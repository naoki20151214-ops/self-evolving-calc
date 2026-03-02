import streamlit as st
from src.calc import add, sub, mul, div

st.title("Self Evolving Calculator")

a = st.number_input("a", value=1.0)
b = st.number_input("b", value=2.0)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("＋"):
        st.success(add(a, b))
with col2:
    if st.button("－"):
        st.success(sub(a, b))
with col3:
    if st.button("×"):
        st.success(mul(a, b))
with col4:
    if st.button("÷"):
        try:
            st.success(div(a, b))
        except Exception as e:
            st.error(str(e))
