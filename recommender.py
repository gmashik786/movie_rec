import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown("<h1 style='text-align: center; color: black;'><b> Simple Movie Recommender App</b></h1>", unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
corrmat = pd.read_pickle('corrmat.pkl')
tr = pd.read_pickle('tr.pkl')
mmatrix=pd.read_pickle('mmatrix.pkl')
temp_list=list(corrmat.columns)
movie_list=[]
for i in temp_list:
    movie_list.append(i)
    #print(i)
movie_list.insert(0,'Select a movie')
Name_of_the_movie=st.selectbox('Please select a movie from the list',movie_list)
n=st.select_slider("Number of recommendation",[5,6,7,8,9,10],value=5)
n=int(n)
#@title Enter a movie name or it will choose a random movie and suggest similar movie to that
#Name_of_the_movie = "Star Wars (1977)" #@param {type:"string"}
def rec_engine(Name_of_the_movie,n=5):
    i=0
    x=100000
    for c in corrmat.columns:
        if corrmat.columns[i]==Name_of_the_movie:
            x=i
            break
        i=i+1
    if x==100000:
        x=np.random.choice(range(1,1664))
        st.write("Didn't find the exact match. So suggesting you a random movie and simimar movies")
    temp1=corrmat[corrmat.columns[x]].sort_values(ascending=False)
    temp2=pd.DataFrame(temp1)
#temp2['num_of_ratings']=corrmat['num_of_rating']
    temp2=temp2.join(corrmat['num_of_rating'])
    temp2=temp2.join(tr['rating'])
    temp2.dropna(inplace=True)
    
    temp3=temp2[temp2['num_of_rating']>100]
    temp4=pd.DataFrame(temp3['rating'].head(n))
    #temp4=temp4.style.background_gradient(cmap = 'copper')
    return temp4
if Name_of_the_movie!='Select a movie':
    st.write("Movie name:",Name_of_the_movie)
    st.write(str(n)+" related movies with ratings are: \n")
    rec_m=rec_engine(Name_of_the_movie,n)
    rec_m=rec_m.style.background_gradient(cmap = 'copper')
    st.dataframe(rec_m)
    # if rec_m.shape[0]==0:
    #     st.write("There is no similar movies found in the datadase")
    # else:
    #    
st.markdown("<h2 style='text-align: center; color: red;'><b> Netflix Style Movie Recommendation</b></h2>", unsafe_allow_html=True)
st.write("**Please select some movies for recommendations.**")
nfl=st.multiselect('Add movies here:',movie_list,["Star Wars (1977)", "12 Angry Men (1957)"])
if len(nfl)!=0:
    l=[]
    r=[]
    for m in nfl:
        tempdf=pd.DataFrame()
        tempdf=rec_engine(m,n=3)
        tl=list(tempdf.index)
        trr=list(tempdf['rating'])
        l=l+tl
        r=r+trr
    findf=pd.DataFrame({"Movie Name":l,"Rating":r})
    findf.set_index("Movie Name",inplace=True)
    st.write("**Recommended movies for you**")
    st.dataframe(findf.sort_values(by="Rating",ascending=False).style.background_gradient(cmap = 'ocean_r'))
else:
    st.write("**Please enter some movie above.**")