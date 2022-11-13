from numpy import negative, positive
import streamlit as st
from textblob import TextBlob
import pandas as pd
from textblob.en import polarity, subjectivity
from chart import *


#Sentiment analyser
def sentiment(text, corrspell=False):
    blob = TextBlob(text)
    
    #Spelling Corrector
    if corrspell :        
        blob=blob.correct()
        st.markdown("#### Corrected to")
        st.markdown("**"+str(blob)+"**")
  
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def show_stats2(positive, negative, polarity_list, subjectivity_list):
    avg_pol = sum(polarity_list)/len(polarity_list)
    avg_subj = sum(subjectivity_list)/len(subjectivity_list) 
    subj2 = [subjectivity_list[i] for i in range(len(subjectivity_list)) if not polarity_list[i]==0]
    avg_subj2 = sum(subj2)/len(subj2)
    st.markdown("## Estadísticas")
    st.markdown("---")

    
    col1, col2 = st.columns([1, 1])

    with col1:
        if avg_subj<0.3:
            delta1 = "- low"
        elif avg_subj>0.5:
            delta1 = "+ high"
        else:
            delta1 = ""
        
        if avg_subj2<0.5:
            delta2 = "- low"
        else:
            delta2 = "+ high"
        
        st.metric(label = "Average Subjectivity", value = "%0.5f"%(avg_subj), delta =delta1)
        st.metric(label = "Average Average Subjectivity Of Non Neutral Tweets", value = "%0.5f"%(avg_subj2), delta = delta2)
    
    with col2:

        if avg_pol<-0.25:
            delta1 = "- low"

        elif avg_pol>0.25:
            delta1 = "+ high"
        else:
            delta1 = ""
        
        if negative==0 or positive/negative>10:
            delta2 = "+high"
        else:
            delta2 = "- low"
            
        st.metric(label = "Average Polarity", value = "%0.5f"%(avg_pol), delta = delta1)

        if negative!=0:
            st.metric(label="+ve/-ve Ratio", value = "%.5f"%(positive/negative), delta = delta2)
            #st.write(positive/negative)
            
        else:
            #st.write("All positive")
            st.metric("+ve/-ve Ratio", value = "All Positive", delta = delta2)

    return avg_pol, avg_subj


def show_stats(positive, negative, polarity_list, subjectivity_list):
    avg_pol = sum(polarity_list)/len(polarity_list)
    avg_subj = sum(subjectivity_list)/len(subjectivity_list) 
    subj2 = [subjectivity_list[i] for i in range(len(subjectivity_list)) if not polarity_list[i]==0]
    avg_subj2 = sum(subj2)/len(subj2)
    st.markdown("## Estadísticas")
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("###### Polaridad media")
        st.markdown("###### [-1 to 1]")
        st.markdown("")

        st.markdown("###### Subjetividad media")
        st.markdown("###### [0 to 1]")
        st.markdown("")

        st.markdown("###### Subjetividad media")
        st.markdown("###### de Tweerts no neutros ")
        st.markdown("")

        st.markdown("###### Ratio Positivo / Negativo")
        
    with col2:
        st.write(avg_pol)
        st.markdown("")
        st.markdown("")

        st.write(avg_subj)
        st.markdown("")
        st.markdown("")
        st.markdown("")

        st.write(avg_subj2)
        st.markdown("")
        st.markdown("")


        if negative!=0:
            st.write(positive/negative)
        else:
            st.write("All positive")
    
    return avg_pol, avg_subj

def show_analysis(avg_pol, avg_subj):
    st.markdown("## Análisis")
    st.markdown("---")

    st.markdown("##### Nivel de emoción")
    if avg_pol>=0.25:
        st.markdown('''
            La alta polaridad media positiva indica que la mayoría de los tweets tienen opiniones fuertes y positivas sobre el tema buscado
        ''')
    
    elif avg_pol<=-0.25:
        st.markdown('''
            La alta polaridad media negativa indica que la mayoría de los tweets tienen opiniones fuertes y negativas sobre el tema buscado
        ''')

    else:
        st.markdown('''
            La polaridad media moderada indica que la mayoría de los tweets son algo neutrales sobre el tema buscado y no muestran opiniones fuertes al respecto
        ''')
    
    st.markdown("##### Nivel de subjetividad")
    if avg_subj>=0.35:
        st.markdown('''
            Una subjetividad media alta indica que la mayoría de los tweets son muy subjetivos para la persona que tuitea sobre el tema buscado
        ''')

    else:
        st.markdown('''
            La subjetividad media moderada indica que la mayoría de los tweets son más bien de sentido general que subjetivos sobre el tema buscado
        ''')
    

def tweetSentiment(tweet_df):

    polarity_list=[]
    subjectivity_list=[]
    
    positive=0
    negative=0
    neutral=0

    for i in tweet_df["Polarity"]:
        if i<0:
            negative += 1
            
        elif i>0:
            positive += 1
        
        else:
            neutral += 1

        polarity_list.append(i)
    
    for i in tweet_df["Subjectivity"]:
        subjectivity_list.append(i)
    
    st.markdown("### Distribución de tweets")
    tweetChart(positive, negative, neutral)
    st.markdown("### Proporciones de tweets")
    tweet_pie(positive, negative, neutral)

    #Statistics
    avg_pol, avg_subj = show_stats2(positive, negative, polarity_list, subjectivity_list)
    
    #st.markdown("---")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")

    #Analysis
    show_analysis(avg_pol, avg_subj)
