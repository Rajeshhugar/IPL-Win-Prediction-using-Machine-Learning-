import streamlit as st
import pickle
import pandas as pd


#Title of the page with CSS
#st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏", layout="wide")

st.markdown("<h1 style='text-align: center; color: white;'> IPL Win Predictor </h1>", unsafe_allow_html=True)

#Add background image
bg1='https://p.imgci.com/db/PICTURES/CMS/196500/196525.3.jpg'
bg2='https://www.insidesport.in/wp-content/uploads/2021/04/WhatsApp-Image-2021-04-26-at-11.53.00-AM.jpeg'
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url('https://images.unsplash.com/photo-1512719994953-eabf50895df7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1929&q=80');
             background-attachment: fixed;
             background-size: cover;
              background-color: rgba(0, 0, 0, 0.8);
         }}
         </style>
         """,
         unsafe_allow_html=True
     )



# Add content to the app

teams = ['Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bangalore','Kolkata Knight Riders','Kings XI Punjab','Chennai Super Kings','Rajasthan Royals','Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))


# Set title
#st.title('IPL Win Predictor')

# Create columns
col1, col2 = st.columns(2)

# Create team selection dropdowns
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

# Create city selection dropdown
selected_city = st.selectbox('Select host city', sorted(cities))

# Create target slider
#target = st.slider('Select target score', min_value=1, max_value=250)
target = st.number_input('Select target score', min_value=0, max_value=350, step=1)


# Create score slider
score = st.slider('Select current score', min_value=0, max_value=target-1)

# Create overs slider
overs = st.slider('Select overs completed', min_value=0, max_value=20)

# Create wickets slider
wickets = st.slider('Select wickets out', min_value=0, max_value=10)

# Create button to predict win probability
if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    
    if overs > 0:
        crr = score/overs
    else:
        crr = 0
    if balls_left > 0:
        rrr = (runs_left*6)/balls_left
    else:
        rrr = 0


    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")
