import pandas as pd
import plotly.express as px
import streamlit as st

def chart(po, su):
        
        #Define Colors
        if po>=0:
            c1="#42f598"
        else:
            c1="#fa7066"
        
        #Convert lists to Pandas Datafram
        data = pd.DataFrame(
            [[po,0],[0,su]],
            index = ["Polarity", "Subjectivity"],
            columns = ["Polarity", "Subjectivity"]
        )
        
        #Make Figure
        fig = px.bar(
            data,
            labels  = {
                "index" : "",
                "value" : "value"
            },
            color_discrete_sequence=[c1,"#16d3f5"]
        )
        
        #Plot Fig
        st.plotly_chart(fig)

def tweetChart(positive, negative, neutral):
    data = pd.DataFrame(
            [[positive,0, 0],[0,negative, 0], [0, 0, neutral]],
            index = ["Positive", "Negative", "Neutral"],
            columns = ["No Of Positive Tweets", "No Of Negative Tweets", "No Of Neutral Tweets"]
        )
    
    #Make Figure
    fig = px.bar(
        data,
        labels  = {
            "index" : "Sentiment",
            "value" : "Number Of Tweets"
        },
        color_discrete_sequence=["#42f598", "#fa7066", "#16d3f5"]
    )
    
    #Plot Fig
    st.plotly_chart(fig)