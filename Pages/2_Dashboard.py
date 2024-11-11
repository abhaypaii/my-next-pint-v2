import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("processed_data/embedded_list.csv")

with st.sidebar:
    styles = st.multiselect("Choose from "+ str(len(df["style"].drop_duplicates()))+" beer styles", df["style"].drop_duplicates().values, placeholder="All styles")
    if not styles:
        styles = df["style"].values
    data = df[df["style"].isin(styles)]

    abvdata = data["abv"].sort_values().values
    startabv, endabv = st.select_slider("ABV (%)", options=abvdata, value =(min(abvdata), max(abvdata)))
    data = data[(data["abv"] <= endabv) & (data["abv"] >= startabv)]

    startrating, endrating = st.select_slider("Rating", options=[1,2,3,4,5], value=(1,5))
    data = data[(data["score"] <= endrating) & (data["score"] >= startrating)]

#Row 1
with st.container(key="popular"):
    c1,c2 = st.columns([1.7,1])
    with c1:
        value = data.sort_values(by="count", ascending=False)[:1].values[0]
        st.metric(label="Most popular beer", value=value[1], delta=str(value[8])+ " reviews")
    with c2:
        value = data[["brewery", "count"]].groupby("brewery").sum().sort_values(by="count", ascending=False).reset_index().values[0]
        st.metric(label="Most popular brewery", value=value[0], delta=str(value[-1])+ " reviews")

#Row 2
fig1 = px.bar(data.sort_values(by="count", ascending=False)[:7], x="count", y="beer", text= "beer", color="count", color_continuous_scale="ylorbr", text_auto=True, orientation="h", height=300)
fig1.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, title="Reviews per beer")
fig1.update_traces(texttemplate = '%{y} (%{x})', textposition = "inside")
fig1.update_yaxes(showticklabels=False)

numcols = ['overall', 'smell', 'look', 'taste', 'feel', 'abv']
review_corr = data[numcols].corr()["overall"].drop("overall").sort_values(ascending=False).reset_index()
review_corr = review_corr.rename(columns={"index": "factor", "overall":"correlation"})
review_corr["correlation"] = round(review_corr["correlation"],2)

fig2 = px.bar(review_corr, x="correlation", y="factor", color="correlation", color_continuous_scale="ylorbr", text_auto=True, orientation="h", height=300)
fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, title="Factors affecting overall rating")
fig2.update_traces(texttemplate = '%{y} (%{x})', textposition = "inside")
fig2.update_yaxes(showticklabels=False)

with st.container(key="middlecharts", height=300, border=True):
    c1,c2, col3 = st.columns(3, vertical_alignment="top")
    c1.plotly_chart(fig1)

    with c2.container(key="ratings", border=False, height = 225):
        st.write("**Average Ratings**")
        c1, c2, c3, c4 = st.columns([1,4,4,4])
        c2.metric(label="Overall", value=round(data["overall"].mean(), 2))
        c2.metric(label="Aroma", value=round(data["smell"].mean(), 2))
        c3.metric(label="Appearance", value=round(data["look"].mean(), 2))
        c3.metric(label="Palate", value=round(data["taste"].mean(), 2))
        c4.metric(label="Feel", value=round(data["feel"].mean(), 2))
    
    col3.plotly_chart(fig2)

#Row 3
data_avg = data[numcols].groupby("abv").median().reset_index()

bins = [1.0, 3.0, 5.0, 8.0, 10.0, 12.0, 15.0,18.0, 25.0, 30.0, 40.0, 50.0, 60.0]
labels = [f"{bins[i]}-{bins[i + 1]}" for i in range(len(bins) - 1)]

data_avg["abv_bins"] = pd.cut(data_avg['abv'], bins=bins, labels=labels, right=False)
data_avg = data_avg.groupby("abv_bins").median().reset_index()

colorscale=["#f0e76e", "#cda037", "#b38e2e", "#9a751e", "#755e14"]

fig3 = px.line(data_avg[:9], x="abv_bins", y=["overall", "taste", "look", "smell", "feel"], height=370, color_discrete_sequence=colorscale)
fig3.update_layout(title="Customer preference changing by ABV", showlegend=False, width=900, xaxis=dict(range=[0, 10]), yaxis=dict(range=[1,4.48]))

fig3.update_yaxes(showgrid=False)
for i, d in enumerate(fig3.data):
    fig3.add_scatter(x=[d.x[-1]], y = [d.y[-1]],
                    mode = 'markers+text',
                    text = f"{d.name}: {d.y[-1]:.2f}",
                    textfont = dict(color=d.line.color),
                    textposition='middle right',
                    marker = dict(color = d.line.color, size = 12),
                    legendgroup = d.name,
                    showlegend=False)
    
with st.container(key="bottomcharts"):  
    c1, c2=st.columns([1.3,2])
    c1.write("**Data**")
    c1.dataframe(data.drop(columns=["cluster", "features"]), height=300, hide_index=True)
    c2.plotly_chart(fig3)
