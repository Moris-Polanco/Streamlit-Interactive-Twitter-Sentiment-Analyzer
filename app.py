import streamlit as st
from sentiment_analysis_spanish import sentiment_analysis
from chart import *
from Scrape import *
import datetime

from PIL import Image
import corpora
#Page Config
st.set_page_config(page_title="SIAST")
st.markdown("# Sistema interactivo de análisis de sentimiento de textos")
st.markdown("")
st.sidebar.markdown("# Menú")
show_page = st.sidebar.selectbox(label="Elija la página", options=["Welcome", "Type In Prompt", "Scrape From Twitter"])



if show_page=="Welcome":
    '''
        ##### Bienvenido. Esta aplicación web interactiva tiene como objetivo demostrar el funcionamiento del análisis de sentimiento de texto.
    '''
    image = Image.open('Photos/photo-1523961131990-5ea7c61b2107.jpeg')
    st.image(image)
    
    '''
        ---
        ##### Para empezar:
        - ###### Vaya al menú de la columna izquierda.
        - ###### Elija el método que se utilizará para el análisis de sentimientos [Seleccione la página deseada en el menú desplegable].
        - ###### Pruebe los distintos métodos y vea el análisis.
        ---
        ##### Agunas cosas para tener en cuenta
        
        - ###### Por ahora, el sistema solamente analiza tweets en inglés
        - ###### La polaridad se refiere a la fuerza de la emoción. 
            - -1 es fuertemente negativo y
            - +1 es fuertemente positivo
        - ###### La subjetividad, como su nombre indica, se refiere al grado de subjetividad del texto.
            - 0 es completamente objetivo
            - 1 es completamente subjetivo 
        - ###### Como todos los sistemas de aprendizaje automático, no será 100% preciso y podría tener sesgos.
        - ###### Sistema creado por Jayan Taneja y adaptado para asesorialinguistica.online por Moris Polanco.
        ---
    '''

elif show_page=="Type In Prompt":

    image = Image.open("Photos/photo-1529236183275-4fdcf2bc987e.jpeg")
    st.image(image)

    st.markdown("### Evalúe su texto personalizado")

    txt = st.text_area(label="Introduzca el texto")
    corrspell = st.checkbox(label="Use corrector ortográfico (en inglés)")
    evaluate = st.button(label="Calcule el sentimiento")

    #main
    if evaluate and txt!="":
        
        with st.spinner("Computing Sentiment"):
            
            po,su = sentiment(txt, corrspell)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write("Polaridad: ")
                st.write(po)
                
            with col2:
                st.write("Subjetividad")
                st.write(su)
            
            chart(po, su)

else:

    image = Image.open('Photos/sdfsf.png')
    st.image(image)

    st.markdown("### Evalúe el texto obtenido en Twitter")
    txt = st.text_area(label="Introduzca lo que desea buscar")
    tweetCount = st.slider(label="Elija el número de tweets que se van a raspar", min_value=1, value=10, max_value=1150)
    
    
    #Date Picker
    col1, col2 = st.columns([1, 1])
    with col1:
        begin=st.date_input(label="Fecha inicial", value=datetime.date.today()-datetime.timedelta(days=1), min_value=datetime.date.today()-datetime.timedelta(days=1000), max_value=datetime.date.today()-datetime.timedelta(days=1))
    
    with col2:
        finish=st.date_input(label="Fecha final", value=datetime.date.today(), min_value=datetime.date.today()-datetime.timedelta(days=999), max_value=datetime.date.today())
    
    #Ensure starting date before finishing date
    if finish<=begin:
        st.error("Error \nLa fecha de inicio debe ser < Fecha de finalización") 
        st.stop()
    get_tweet = st.button(label="Raspe y analice los tweets")
    
    if get_tweet:

        if txt=="":
            st.error("Error \nCadena de búsqueda vacía")
            st.stop()
    
        with st.spinner("Cargando"):
            

            data, data_clean = scrape_tweets(txt, tweetCount, begin, finish)
            
            if len(data)==0:
                st.error("No data")
                st.stop()

            st.markdown("")
            st.markdown("")
            st.markdown("")

            st.markdown("## Resultado")
            st.markdown("---")
            
            tweetSentiment(data_clean)

            with st.expander("Mostrar los tweets de Twitter raspados"):
                                
                st.markdown("#### Crudo")
                st.write(data)
                
                st.markdown("#### Procesado")
                st.write(data_clean)


