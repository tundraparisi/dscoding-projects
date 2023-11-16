import pandas as pd
import streamlit as st
from PIL import Image


st.title('BGG Project')
st.text(
    "Name and surname: Linh Chi Hoang \n"
    "Matriculation number: "
)
st.markdown('##### Introduction to the project\n'
            '- The project aims to propose a different method in sorting various types of board games besides '
            'focusing on the comparison between their Average scores.\n'
            '- The project is going to use the data provided on The Board Game Geek (BGG) website, in which players '
            'are going to give comments and rates those games on the scale from 0 to 10.\n')
original_data = pd.read_csv('bgg.csv')
st.write(original_data)
st.markdown('##### The idea on the project\n'
            '- Instead of creating a ranking table based on the Average scores of the games, the project is using the '
            'Bayesian Average to make comparisons.\n'
            '- In real life, there are lots of cases in which people use Bayesian Average in costume ranking, '
            'for example on movies or a specific product.')

st.latex(r'''
Bayesian Average = \frac{(Prior weight * Prior mean) + (Average score * Number of votes)}
{Prior weight + Number of votes}
''')
st.markdown('##### Brief description about the steps:\n'
            '- Cleaning the data\n  '
            '+ The goal is to sort the data which is necessary for calculating The Bayesian Average score of each '
            'game. In order to apply the formula, we need to calculate:\n   '
            '   + Prior mean - The average of average scores of every game\n  '
            '   + Prior weight - The average of voting number of every game\n   '
            '   + Average rating score of each game\n   '
            '   + Number of votes of each game\n'
            '- Visualizing the data\n   '
            '+ The goal is to graphically spot the difference between using Average scores and Bayesian Average '
            'scores in sorting the ranking.')

st.markdown('##### The Game ranking table based on Average scores')
average_table = pd.read_csv('average_table.csv')
st.write(average_table)

st.markdown('##### The Game ranking table based on Bayesian Average scores')
bayesian_table = pd.read_csv('bayesian_table.csv')
st.write(bayesian_table)

st.markdown('##### Scatter plot "Game ratings based on Average scores"')
image1 = Image.open('Visualization1.png')
st.image(image1)

st.markdown('##### Scatter plot "Game ratings based on Bayesian Average scores"')
image2 = Image.open('Visualization2.png')
st.image(image2)
