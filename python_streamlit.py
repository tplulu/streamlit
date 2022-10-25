import pandas as pd
import numpy as np
import seaborn as sb
import streamlit as st 
import matplotlib.pyplot as plt

cancer = pd.read_csv('30-70cancerChdEtc.csv') 
cancer = pd.DataFrame(cancer)


co2 = pd.read_csv('co2.csv', encoding='latin1') 
co2 = pd.DataFrame(co2)

co2 = co2[(co2["Year"]<2017)&(co2["Year"]>1999)]
co2_origin = co2
co2 = co2.rename(columns={"Country": "Location"})
co2 = co2.rename(columns={"Year": "Period"})
pa = pd.concat( [cancer, co2],axis=0,ignore_index=True)
pa = pa.groupby(['Location', 'Period']).mean()
pa = pa.query("Period==2005 or Period==2000 or Period==2010 or Period==2015 or Period==2016")
pa.head(30)

st.title('Relation entre les emissions de CO2 et les taux de cancers')

pa = pa.rename(columns={"CO2 emission (Tons)": "emission"})
pa = pa.rename(columns={"First Tooltip": "Cancer"})
pa_small = pa.query("emission< 0.20e10")
pa_big = pa.query("emission> 0.20e10")
fig2, ax = plt.subplots()
ax = sb.relplot(
    data=pa_small.sample(n=100),
    x="Cancer", y="emission", 
)
st.pyplot(fig2)
corr_pa = pa.corr()
fig2, ax = plt.subplots()
ax = fig = sb.heatmap(
    data=corr_pa,
)
st.pyplot(fig2)
fig2, ax = plt.subplots()
ax = sb.lmplot(
    data=pa_small,
    x="Cancer", y="emission",
)
st.pyplot(fig2)
cancer_moye = cancer.groupby(['Period']).mean()
fig2, ax = plt.subplots()
ax = sb.relplot(
    data=cancer_moye,
    x="Period", y="First Tooltip", kind="line",
)
st.pyplot(fig2)
co2_moye = co2_origin.groupby(['Year']).mean()
fig2, ax = plt.subplots()
ax = sb.relplot(
    data=co2_moye,
    x="Year", y="CO2 emission (Tons)", kind="line",
)
st.pyplot(fig2)
st.title('Boite à moustache')
fig2, ax = plt.subplots()
ax = sb.boxplot( 
    data=cancer,
    x="First Tooltip", y="Dim1",
)
st.pyplot(fig2)

cancer2 = cancer[(cancer["First Tooltip"]<35)]
fig2, ax = plt.subplots()
ax = sb.boxplot(
    data=cancer2,
    x="First Tooltip", y="Dim1",
)
st.pyplot(fig2)
sb.catplot(
    data=cancer2,
    x="Dim1", y="First Tooltip", kind="bar", height=10 
)

cancer_grp = cancer.groupby(['Dim1']).mean()
cancer2["First Tooltip"].describe()

