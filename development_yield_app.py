import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Development Yield Explorer",
    page_icon="🏗️",
    layout="centered"
)

# --- TITLE & INTRO ---
st.title("🏗️ Development Yield Explorer")
st.markdown("""

Merk at alt innhold er laget av ChatGPT uten noen som helst sjekk!                         

This app helps you **understand development yield** —  
a key metric in property development showing how much **annual rental income**
a project generates compared to its **total development cost**.
""")

# Display the formula using LaTeX
st.latex(r"""
\text{Development Yield (\%)} = \frac{\text{Annual Rent}}{\text{Total Development Cost}} \times 100
""")

st.divider()

# --- INPUT SECTION ---
st.header("📥 Enter Your Project Details")

col1, col2 = st.columns(2)

with col1:
    land_cost = st.number_input("Land Cost (NOK)", min_value=0, value=6_000_000, step=100_000)
    construction_cost = st.number_input("Construction Cost (NOK)", min_value=0, value=10_000_000, step=100_000)

with col2:
    professional_fees = st.number_input("Professional Fees (NOK)", min_value=0, value=1_000_000, step=50_000)
    other_costs = st.number_input("Other Costs (Permits, Marketing, etc.) (NOK)", min_value=0, value=500_000, step=50_000)

annual_rent = st.number_input("Expected Annual Rent (NOK)", min_value=0, value=1_400_000, step=50_000)

# --- CALCULATIONS ---
total_development_cost = land_cost + construction_cost + professional_fees + other_costs

if total_development_cost > 0:
    development_yield = (annual_rent / total_development_cost) * 100
else:
    development_yield = 0

# --- OUTPUT SECTION ---
st.divider()
st.header("📊 Results")

st.metric(
    label="Development Yield",
    value=f"{development_yield:.2f} %",
    delta=None
)

# Show the formula applied with the numbers (LaTeX)
st.latex(rf"""
\text{{Development Yield (\%)}} = \frac{{{annual_rent:,}}}{{{total_development_cost:,}}} \times 100 = {development_yield:.2f}\%
""")

st.write(f"**Total Development Cost:** {total_development_cost:,.0f} NOK")
st.write(f"**Annual Rent:** {annual_rent:,.0f} NOK")

# --- INTERPRETATION ---
st.subheader("🧠 Interpretation")
if development_yield < 6:
    st.error("Low yield (<6%) — may only work in premium or low-risk areas.")
elif 6 <= development_yield <= 8:
    st.warning("Moderate yield (6–8%) — typical for residential projects.")
else:
    st.success("Strong yield (>8%) — good return for most developments!")

# --- VISUALIZATION ---
st.subheader("📈 Yield Sensitivity to Rent")

# Generate a range of rents +/- 25% to visualize yield sensitivity
rent_values = [annual_rent * (1 + i/100) for i in range(-25, 26, 5)]
yield_values = [(r / total_development_cost) * 100 for r in rent_values]

df = pd.DataFrame({"Annual Rent (NOK)": rent_values, "Development Yield (%)": yield_values})
fig = px.line(df, x="Annual Rent (NOK)", y="Development Yield (%)",
              title="How Yield Changes with Rent Level",
              markers=True)
st.plotly_chart(fig, use_container_width=True)

# --- LEARNING SECTION ---
with st.expander("💬 Learn More About Development Yield"):
    st.markdown("""
    **Development Yield** measures how much rental income a completed property produces
    each year, compared to the total cost of developing it.

    - **Higher yield** → Better return on development cost  
    - **Lower yield** → Lower return or higher project risk  
    - Used by developers, investors, and banks to assess project viability

    **Typical ranges:**
    - <6% → Low yield  
    - 6–8% → Moderate yield (common for residential)  
    - >8% → High yield (often commercial or value-add projects)
    """)

st.caption("Created with ❤️ using Streamlit and Plotly")