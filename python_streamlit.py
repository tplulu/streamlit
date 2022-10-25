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
fig, ax = plt.subplots()
fig = sb.relplot(data=pa_small.sample(n=100),x="Cancer", y="emission")
plt.title("nuage de point pour observer les morts par cancers en fonction des emissions de CO2")
st.pyplot(fig)

corr_pa = pa.corr()
fig1, ax = plt.subplots()
ax = sb.heatmap(
    data=corr_pa,
)
plt.title("observation de la corrélation entre plusieurs éléments")
st.pyplot(fig1)
fig2, ax = plt.subplots()
fig2 = sb.lmplot(
    data=pa_small,
    x="Cancer", y="emission",
)
plt.title("On observe une relation négative entre le taux de cancer et le taux de polution d'un pays")
st.pyplot(fig2)
cancer_moye = cancer.groupby(['Period']).mean()
fig2, ax = plt.subplots()
fig2 = sb.relplot(
    data=cancer_moye,
    x="Period", y="First Tooltip", kind="line",
)
plt.title("Progression des morts par cancer en fonction du temps")
st.pyplot(fig2)
co2_moye = co2_origin.groupby(['Year']).mean()
fig2, ax = plt.subplots()
fig2 = sb.relplot(
    data=co2_moye,
    x="Year", y="CO2 emission (Tons)", kind="line",
)
plt.title("Progression des émissions de CO2 en fonction du temps")
st.pyplot(fig2)
st.title('Boite à moustache')
fig2, ax = plt.subplots()
ax = sb.boxplot( 
    data=cancer,
    x="First Tooltip", y="Dim1",
)
plt.title("On observe des valeurs abérantes")
st.pyplot(fig2)

cancer2 = cancer[(cancer["First Tooltip"]<35)]
fig2, ax = plt.subplots()
ax = sb.boxplot(
    data=cancer2,
    x="First Tooltip", y="Dim1",
)
plt.title("suppression des valeurs abérantes")
st.pyplot(fig2)

fig5, ax = plt.subplots()
fig5 = sb.catplot(
    data=cancer2,
    x="Dim1", 
    y="First Tooltip", 
    kind="bar", 
    height=10 
)
plt.title("cancer par genre")
st.pyplot(fig5)

cancer_grp = cancer.groupby(['Dim1']).mean()
cancer2["First Tooltip"].describe()

