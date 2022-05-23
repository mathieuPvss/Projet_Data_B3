
from ast import With
from cProfile import label
from turtle import left
from pyrsistent import  v
import streamlit.components.v1 as components

import streamlit as st
from streamlit_lottie import st_lottie

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import requests 
import os 
import pandas as pd
import numpy as np


# fonctions:
def load_lottiesUrl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.cache
def load_data(data):
    data = pd.read_csv(data)
    return data
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# template for result of search
HTML_TEMPLATE_PLAYERS = """
<div>
    <h3>{} <img src='{}' </h3> 
    <img src='{}'>
    <img src='{}'>
    <p>Note: {}</p>
    <p>Position: {}</p>
</div>
"""
HTML_TEMPLATE_PLAYERS_DESC = """
<div>
    <p>Prix: {}€</p>
    <p>Age: {} ans</p>
    <p>Date anniversaire: {}</p>
    <p>Taille: {}cm </p>
    <p>Poid: {}kg </p>
</div>
"""

HTML_TEMPLATE_PLAYERs_basic_stat = """
<div>
    <p>Note général: {}</p>
    <p>Vitesse: {} </p>
    <p>Tire: {}</p>
    <p>Passe: {} </p>
    <p>Drible: {} </p>
    <p>Défense: {} </p>
    <p>Physique: {} </p>
    <p>Total: {} </p>
</div>
"""

HTML_TEMPLATE_PLAYERs_ingame_stat = """                             
<div>
    <p>Accélération: {}</p>
    <p>Vitesse sprint: {} </p>
    <p>Position: {}</p>
    <p>Finition: {} </p>
    <p>Puissance de frappe: {} </p>
    <p>Frappe longue: {} </p>
    <p>Frappe en volé: {} </p>
    <p>Pénalty: {} </p>
    <p>Vision: {} </p>
    <p>Crossing: {} </p>
    <p>Précision coup franc : {} </p>
    <p>Passe courte: {} </p>
    <p>Passe longuue: {} </p>
    <p>Curve: {} </p>
    <p>Agilité: {} </p>
    <p>Équilibre: {} </p>
    <p>Reaction: {} </p>
    <p>Contrôle de balle: {} </p>
    <p>Dribbling: {} </p>
    <p>Sang froid: {} </p>
    <p>Interception: {} </p>
    <p>Précision de la tête: {} </p>
    <p>Conscience deffensive: {} </p>
    <p>Tacle glissé: {} </p>
    <p>Tacle debout: {} </p>
    <p>Saut du joueur: {} </p>
    <p>Endurance: {} </p>
    <p>Force: {} </p>
</div>
"""

HTML_TEMPLATE_PLAYERs_infos_joueur = """
<div>
    <p>Nom complet: {}</p>
    <p>Club: {} <img src='{}'></p>
    <p>League: {}</p>
    <p>Position: {} </p>
    <p>Geste technique: {}/5 </p>
    <p>Mauvais pied: {}/5 </p>
    <p>Pied préféré: {} </p>
    <p>Age: {} ans</p>
    <p>Hauteur: {} cm</p>
    <p>Poid: {} kg<p>
    <p>Date d'anniversaire: {} </p>
</div>
"""

# ------------load url---------------

Animation1 =load_lottiesUrl("https://assets8.lottiefiles.com/packages/lf20_e4mqXr/ball_04.json")
Animation2 =load_lottiesUrl("https://assets5.lottiefiles.com/packages/lf20_x17ybolp.json")

st.set_page_config(page_title="My Project")
st.title('Analyse des jeux Fifa :')

def main():
    menu = ["Acceuil","Analyse jeux", "Comparateur de joueurs", "Rechercher un joueur"]
    choice = st.sidebar.selectbox("Menu:", menu)
    
    #Pour choisir son dataset : 
    path_origin = "/Users/mathieu-p/Documents/Ynov/projet_data/archive"
    liste = [os.path.splitext(filename)[0] for filename in os.listdir(path_origin)]
    liste.remove('.DS_Store')

    select_dataset = st.sidebar.selectbox('Choisir son Dataset:', liste)
    path_dataset = "/Users/mathieu-p/Documents/Ynov/projet_data/archive/{}.csv".format(select_dataset)
    df = load_data(path_dataset)

    if choice == "Acceuil":
        with st.container():
            st.subheader("Bonjour, ")
            st.write("Vous trouverez dans notre application les differentes analyses qu'on a pu faire sur les joueurs de foot à partir des données des jeux FIFA.")
            st.write ("Ci dessous le lien de notre DataSet avec lequelles nous avons travailler :")
            st.write("[Kaggle >](https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset?resource=download&select=players_22.csv)")

        with st.container():
            st.write('---')
            left_column, right_column = st.columns(2)
            with left_column:
                st.header('Objectifs :')
                st.write('##')
                st.write(
                    """
                    Les objectifs de cette application sont de pouvoir:
                    - faire des analyses en fonction du jeu sélectionner.
                    - afficher des graphiques qui pourront nous servir à interpréter nos données.
                    - appliqué des modèles  de machines learning.
                    - Pouvoir fair des recherches en appliquant des filtres afin de retrouver une liste de joueurs par exemple.     
                    - comparaison des statistiques entre des joueurs sélectinner.
                    """
                )
            with right_column:
                st_lottie(Animation2,height=400)
          

    elif choice == "Analyse jeux":
        st.subheader("Voici les differents résultats qu'on a pu avoir avoir nos analyses:")

        df_analyse = df
        # suppression des colonnes qui ne nous interessent pas
        df_analyse = df_analyse.drop(columns=['sofifa_id', 'player_url', 'long_name', 'dob', 'club_loaned_from', 'club_joined', 'league_name','league_level','club_position','club_contract_valid_until','club_team_id','value_eur','nationality_id', 'nation_team_id', 'nation_position', 'nation_jersey_number', 'real_face', 'ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram', 'lm', 'lcm', 'cm', 'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb', 'lb', 'lcb', 'cb', 'rcb', 'rb', 'gk', 'player_face_url', 'club_logo_url', 'club_flag_url', 'nation_logo_url', 'nation_flag_url'])
        
        #dupliquer le dataframe
        df_player22 = df_analyse.copy()
        

        indexNames = df_player22[(df_player22['shooting'] == 'NaN') & (df_player22['passing'] == 'NaN') & (df_player22['dribbling'] == 'NaN') & (df_player22['defending'] == 'NaN') & (df_player22['physic'] == 'NaN')].index
        df_player22.drop(indexNames, inplace=True)
        
        import seaborn as sns
        # Relation entre potential et wage
        st.subheader("Relation entre potential et wage:")
        plt.figure(figsize=(7, 5))
        ax = sns.scatterplot(x =df_player22['potential'], y = df_player22['wage_eur'])
        plt.xlabel("Potential") 
        plt.ylabel("Wage EUR")
        plt.title("Potential & wage", fontsize = 18)
        st.pyplot(plt)

        # Relation entre potentiel et wage par reputation internationale
        st.subheader('Relation entre potentiel et wage par reputation internationale:')
        plt.figure(figsize=(7, 5))
        ax = sns.scatterplot(x =df_player22['potential'], y = df_player22['wage_eur'], hue = df_player22['international_reputation'])
        plt.xlabel("Potential") 
        plt.ylabel("Wage EUR")
        plt.title("Potential & wage", fontsize = 18)
        st.pyplot(plt)

        # relation entre potentiel et l'age 
        st.subheader('relation entre potentiel et l\'age:')
        fig, ax = plt.subplots(figsize = (8,5))
        ax = sns.scatterplot(x =df_player22['height_cm'], y = df_player22['potential'])
        plt.xlabel("Height") 
        plt.ylabel("Potential")
        plt.title("Relationship between Height and Potential", fontsize = 16)
        st.pyplot(plt)

        # distribution of key metrics
        st.subheader('Distribution:')
        fig, axes = plt.subplots(2, 2, figsize=(13, 9))
        axes[0,0].hist(df_player22['wage_eur'])
        axes[0,0].set_xlabel('Wages in Euro')
        axes[0,0].set_ylabel('Count')
        axes[0,0].set_title('Distribution of Wages in Euros')

        axes[0,1].hist(df_player22['age'], bins = 15)
        axes[0,1].set_xlabel('Age of Players')
        axes[0,1].set_ylabel('Count')
        axes[0,1].set_title('Distribution of Players Ages')



        axes[1,0].set_title('Distribution of Height of Players')
        sns.histplot(df_player22, x='height_cm', ax=axes[1,0], kde=True)
        axes[1,0].set_xlabel('Height in Centimeters')
        axes[1,0].set_ylabel('Count')


        axes[1,1].set_title('Distribution of Weight of Players')
        sns.histplot(df_player22, x='weight_kg', ax=axes[1,1], kde=True)
        axes[1,1].set_xlabel('Weight in kg')
        axes[1,1].set_ylabel('Count')


        plt.tight_layout(pad=2)
        st.pyplot(plt)

        #Quel pied les footballers utilisent le plus en global sinon quel pied ils preferent
        st.subheader("Quel pied les footballers utilisent le plus en global:")
        preferred_foot_labels = df_player22["preferred_foot"].value_counts().index 
        preferred_foot_values = df_player22["preferred_foot"].value_counts().values 
        explode = (0, 0.1) #separer les elemnets sur le schema

        # Visualisation en schema

        plt.figure(figsize = (7,7))
        plt.pie(preferred_foot_values, labels=preferred_foot_labels,autopct='%1.2f%%')
        plt.title('Football Players Preferred Feet',color = 'black',fontsize = 15)
        plt.legend()
        st.pyplot(plt)
        

    
    elif choice == "Comparateur de joueurs":
        st.subheader("Comparateur de joueurs :")
        with st.container():
            left_column, midle_column, right_column = st.columns([4, 5, 5])
            with left_column:
                st.subheader("Selectionnez les joueurs à comparer.")

                players = list(df['short_name'].drop_duplicates())
                players.insert(0,'Selectionnez ')
                players_choice1 = st.selectbox('Choisir le joueur 1 à comparer:', players)
                players_choice2 = st.selectbox('Choisir le joueur 2 à comparer:', players)

                boutton_compare = st.button("Comparé")
                if boutton_compare:
                    result = df.loc[(df["short_name"]==players_choice1),:]
                    st.session_state.player1 = result.iloc[[0],:] 
                    result2 = df.loc[(df["short_name"]==players_choice2),:]
                    st.session_state.player2 = result2.iloc[[0],:]
            with midle_column:
                st.subheader("Joueur sélectionné 1:")
                if boutton_compare:
                    index=["result"]
                    st.session_state.player1.index = index
                    st.write(st.session_state.player1)
                     
                    #   Player infos
                    short_name = st.session_state.player1.iloc[0, 2]
                    flag_player = st.session_state.player1.iloc[0, 109]
                    image_player = st.session_state.player1.iloc[0, 105]
                    poste_player = st.session_state.player1.iloc[0, 4]
                    note_player = st.session_state.player1.iloc[0, 5]
                    team_player = st.session_state.player1.iloc[0, 106]
                    
                    st.markdown(HTML_TEMPLATE_PLAYERS.format(short_name, flag_player, image_player,team_player,note_player, poste_player ),
                                        unsafe_allow_html=True)


                    #basic stat:
                    vitesse_player = st.session_state.player1.iloc[0, 37]
                    tire_player = st.session_state.player1.iloc[0, 38]
                    passe_player = st.session_state.player1.iloc[0, 39]
                    drible_player = st.session_state.player1.iloc[0, 40]
                    def_player = st.session_state.player1.iloc[0, 41]
                    phy_player = st.session_state.player1.iloc[0, 42]
                    total_basic_stat = vitesse_player+tire_player+passe_player+drible_player+def_player+phy_player


                    #stat en jeu:
                    acceleration = st.session_state.player1.iloc[0, 53]
                    vitesse_sprint = st.session_state.player1.iloc[0, 54]
                    Position = st.session_state.player1.loc["result", "mentality_positioning"]
                    Finition = st.session_state.player1.loc["result", "attacking_finishing"]
                    force_frappe = st.session_state.player1.loc["result", "power_shot_power"]
                    frappe_longue = st.session_state.player1.loc["result", "power_long_shots"]
                    frappe_volé = st.session_state.player1.loc["result", "attacking_volleys"]
                    penalti = st.session_state.player1.loc["result", "mentality_penalties"]
                    vision = st.session_state.player1.loc["result", "mentality_vision"]
                    crossing = st.session_state.player1.loc["result", "attacking_crossing"]
                    precision_coup_franc = st.session_state.player1.loc["result", "skill_fk_accuracy"] 
                    passe_courte = st.session_state.player1.loc["result", "attacking_short_passing"]
                    passe_longue = st.session_state.player1.loc["result", "skill_long_passing"] 
                    curve = st.session_state.player1.loc["result", "skill_curve"]
                    agilité = st.session_state.player1.loc["result", "movement_agility"]
                    equilibre = st.session_state.player1.loc["result", "movement_balance"]
                    reaction = st.session_state.player1.loc["result", "movement_reactions"]
                    controle_balle = st.session_state.player1.loc["result", "skill_ball_control"] 
                    dribles = st.session_state.player1.loc["result", "skill_dribbling"]
                    sang_froid = st.session_state.player1.loc["result", "mentality_composure"]
                    interception = st.session_state.player1.loc["result", "mentality_interceptions"]
                    precision_tête = st.session_state.player1.loc["result", "attacking_heading_accuracy"] 
                    def_inteligence = st.session_state.player1.loc["result", "defending_marking_awareness"]
                    tacle_glissé = st.session_state.player1.loc["result", "defending_sliding_tackle"]
                    tacle_debout = st.session_state.player1.loc["result", "defending_standing_tackle"]
                    saut = st.session_state.player1.loc["result", "power_jumping"]
                    endurance = st.session_state.player1.loc["result", "power_stamina"]
                    force = st.session_state.player1.loc["result", "mentality_aggression"]
                    
                    #infos joueur``
                    long_name = st.session_state.player1.iloc[0, 3]
                    team_player = st.session_state.player1.loc["result", "club_name"]
                    team_player_img = st.session_state.player1.loc["result", "club_logo_url"]
                    ligue = st.session_state.player1.loc["result", "league_name"]
                    poste_player = st.session_state.player1.loc["result", "player_positions"]
                    skill_star = st.session_state.player1.loc["result", "skill_moves"]
                    week_foot = st.session_state.player1.loc["result", "weak_foot"]
                    good_foot = st.session_state.player1.loc["result", "preferred_foot"]
                    age_player = st.session_state.player1.loc["result", "age"]
                    height_player = st.session_state.player1.loc["result", "height_cm"]
                    weight_player = st.session_state.player1.loc["result", "weight_kg"]
                    birth_player = st.session_state.player1.loc["result", "dob"]


                    # description:
                    with st.expander("Stat basic:"):
                        st.markdown(HTML_TEMPLATE_PLAYERs_basic_stat.format(
                        note_player, vitesse_player, tire_player, passe_player,drible_player,def_player ,phy_player,total_basic_stat ),unsafe_allow_html=True)

                    with st.expander("Stat en jeu:"):
                        st.markdown(HTML_TEMPLATE_PLAYERs_ingame_stat.format(
                        acceleration, vitesse_sprint, Position, Finition,force_frappe,frappe_longue ,frappe_volé,penalti,vision ,crossing , 
                        precision_coup_franc,passe_courte ,passe_longue ,curve ,agilité ,equilibre ,reaction ,controle_balle ,dribles ,sang_froid ,
                        interception, precision_tête,def_inteligence , tacle_glissé, tacle_debout, saut,endurance,force ),unsafe_allow_html=True)
                    
                    with st.expander("Infos joueur:"):
                        st.markdown(HTML_TEMPLATE_PLAYERs_infos_joueur.format(
                        long_name, team_player, team_player_img, ligue,poste_player,skill_star ,week_foot,good_foot,age_player,height_player ,weight_player ,birth_player),unsafe_allow_html=True)




                
                
            with right_column:
                st.subheader("Joueur sélectionné 2:")
                if boutton_compare:
                    
                    index=["result"]
                    st.session_state.player2.index = index
                    st.write(st.session_state.player2)
                    
                    
                    #   Player infos
                    short_name2 = st.session_state.player2.iloc[0, 2]
                    flag_player = st.session_state.player2.iloc[0, 109]
                    image_player = st.session_state.player2.iloc[0, 105]
                    poste_player = st.session_state.player2.iloc[0, 4]
                    note_player = st.session_state.player2.iloc[0, 5]
                    team_player = st.session_state.player2.iloc[0, 106]
                    
                    st.markdown(HTML_TEMPLATE_PLAYERS.format(short_name2, flag_player, image_player,team_player,note_player, poste_player ),
                                        unsafe_allow_html=True)


                    #basic stat:
                    vitesse_player2 = st.session_state.player2.iloc[0, 37]
                    tire_player2 = st.session_state.player2.iloc[0, 38]
                    passe_player2 = st.session_state.player2.iloc[0, 39]
                    drible_player2 = st.session_state.player2.iloc[0, 40]
                    def_player2 = st.session_state.player2.iloc[0, 41]
                    phy_player2 = st.session_state.player2.iloc[0, 42]
                    total_basic_sta2 = vitesse_player+tire_player+passe_player+drible_player+def_player+phy_player


                    #stat en jeu:
                    acceleration2 = st.session_state.player2.iloc[0, 53]
                    vitesse_sprint2 = st.session_state.player2.iloc[0, 54]
                    Position2 = st.session_state.player2.iloc[0,65]
                    Finition2 = st.session_state.player2.loc["result", "attacking_finishing"]
                    force_frappe2 = st.session_state.player2.loc["result", "power_shot_power"]
                    frappe_longue2 = st.session_state.player2.loc["result", "power_long_shots"]
                    frappe_volé2 = st.session_state.player2.loc["result", "attacking_volleys"]
                    penalti2 = st.session_state.player2.loc["result", "mentality_penalties"]
                    vision2 = st.session_state.player2.loc["result", "mentality_vision"]
                    crossing2 = st.session_state.player2.loc["result", "attacking_crossing"]
                    precision_coup_franc2 = st.session_state.player2.loc["result", "skill_fk_accuracy"] 
                    passe_courte2 = st.session_state.player2.loc["result", "attacking_short_passing"]
                    passe_longue2 = st.session_state.player2.loc["result", "skill_long_passing"] 
                    curve2 = st.session_state.player2.loc["result", "skill_curve"]
                    agilité2 = st.session_state.player2.loc["result", "movement_agility"]
                    equilibre2 = st.session_state.player2.loc["result", "movement_balance"]
                    reaction2 = st.session_state.player2.loc["result", "movement_reactions"]
                    controle_balle2 = st.session_state.player2.loc["result", "skill_ball_control"] 
                    dribles2 = st.session_state.player2.loc["result", "skill_dribbling"]
                    sang_froid2 = st.session_state.player2.loc["result", "mentality_composure"]
                    interception2 = st.session_state.player2.loc["result", "mentality_interceptions"]
                    precision_tête2 = st.session_state.player2.loc["result", "attacking_heading_accuracy"] 
                    def_inteligence2 = st.session_state.player2.loc["result", "defending_marking_awareness"]
                    tacle_glissé2 = st.session_state.player2.loc["result", "defending_sliding_tackle"]
                    tacle_debout2 = st.session_state.player2.loc["result", "defending_standing_tackle"]
                    saut2 = st.session_state.player2.loc["result", "power_jumping"]
                    endurance2 = st.session_state.player2.loc["result", "power_stamina"]
                    force2 = st.session_state.player2.loc["result", "mentality_aggression"]
                    
                    #infos joueur
                    long_name = st.session_state.player2.iloc[0, 3]
                    team_player = st.session_state.player2.loc["result", "club_name"]
                    team_player_img = st.session_state.player2.loc["result", "club_logo_url"]
                    ligue = st.session_state.player2.loc["result", "league_name"]
                    poste_player = st.session_state.player2.loc["result", "player_positions"]
                    skill_star = st.session_state.player2.loc["result", "skill_moves"]
                    week_foot = st.session_state.player2.loc["result", "weak_foot"]
                    good_foot = st.session_state.player2.loc["result", "preferred_foot"]
                    age_player = st.session_state.player2.loc["result", "age"]
                    height_player = st.session_state.player2.loc["result", "height_cm"]
                    weight_player = st.session_state.player2.loc["result", "weight_kg"]
                    birth_player = st.session_state.player2.loc["result", "dob"]


                    # description:
                    with st.expander("Stat basic:"):
                        st.markdown(HTML_TEMPLATE_PLAYERs_basic_stat.format(
                        note_player, vitesse_player2, tire_player2, passe_player2,drible_player2,def_player2 ,phy_player2,total_basic_stat ),unsafe_allow_html=True)

                    with st.expander("Stat en jeu:"):
                        st.markdown(HTML_TEMPLATE_PLAYERs_ingame_stat.format(acceleration2, vitesse_sprint2, Position2, Finition2, force_frappe2, frappe_longue2, 
                        frappe_volé2,penalti2 ,vision2 ,crossing2,precision_coup_franc2 , 
                        passe_courte2,passe_longue2 ,curve2, agilité2,equilibre2 ,reaction2,controle_balle2 ,dribles2,
                        sang_froid2 , interception2,precision_tête2,def_inteligence2 ,tacle_glissé2, tacle_debout2, saut2,endurance2, force2),unsafe_allow_html=True)
                    
                    with st.expander("Infos joueur:"):
                        st.markdown(HTML_TEMPLATE_PLAYERs_infos_joueur.format(
                        long_name, team_player, team_player_img, ligue,poste_player,skill_star ,week_foot,good_foot,age_player,height_player ,weight_player ,birth_player),unsafe_allow_html=True)

        with st.container():
            
            if boutton_compare:
                #Plot -->faire plus de plot + intégrer le taf à shadrack  + powerpoint + story telling
                
                    
                # Radar plot
                categorie =['Vitesse', 'Tir', "Passe", "Drible", "Defense","Physique" ] 

                fig = go.Figure()

                fig.add_trace(go.Scatterpolar(
                    r=[vitesse_player, tire_player, passe_player, drible_player, def_player,phy_player],
                    theta=categorie,
                    fill='toself',
                    name=short_name
                ))
                fig.add_trace(go.Scatterpolar(
                    r=[vitesse_player2, tire_player2, passe_player2, drible_player2, def_player2,phy_player2],
                    theta=categorie,
                    fill='toself',
                    name=short_name2
                ))

                fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                    )),
                showlegend=False,
                title_text="Stats basique de {} et de {} .".format(short_name, short_name2)
                )
                
                st.subheader("Radar plot:")
                st.plotly_chart(fig, use_container_width=True)

                
                
                # bar plot:
                # set width of bars
                barWidth = 0.25
                
                # set heights of bars
                bars1 = [acceleration, vitesse_sprint, Position, Finition, force_frappe, frappe_longue, 
                frappe_volé,penalti ,vision ,crossing,precision_coup_franc , 
                passe_courte,passe_longue ,curve, agilité,equilibre ,reaction,controle_balle ,dribles,
                sang_froid , interception,precision_tête,def_inteligence ,tacle_glissé, tacle_debout, saut,endurance, force]

                bars2 = [acceleration2, vitesse_sprint2, Position2, Finition2, force_frappe2, frappe_longue2, 
                frappe_volé2,penalti2 ,vision2 ,crossing2,precision_coup_franc2 , 
                passe_courte2,passe_longue2 ,curve2, agilité2,equilibre2 ,reaction2,controle_balle2 ,dribles2,
                sang_froid2 , interception2,precision_tête2,def_inteligence2 ,tacle_glissé2, tacle_debout2, saut2,endurance2, force2]
                

                # Set position of bar on X axis
                r1 = np.arange(len(bars1))
                r2 = np.arange(len(bars2))
                
                # Make the plot
                plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label=short_name)
                plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label=short_name2)
                
                
                # Add xticks on the middle of the group bars
                plt.xlabel('Stat en jeu', fontweight='bold')
                plt.xticks([r + 0.5 for r in range(len(bars1))], ["Accélération", "Vitesse sprint", "Position", "Finition", "Puissance de frappe","Frappe longue","Frappe en volé" ,"Pénalty" ,"Vision","Crossing"  ,"Précision coup franc", "Passe courte","Passe longuue" ,"Curve","Agilité" ,
                 "Équilibre","Reaction" ,"Contrôle de balle" ,"Dribbling","Sang froid" ,"Interception","Précision de la tête" ,"Conscience deffensive",
                 "Tacle glissé" ,"Tacle debout" , "Saut du joueur","Endurance","Force"],fontsize='xx-small',rotation=90)
                
                
                # Create legend & Show graphic
                
                plt.legend()
                
                
                st.subheader("Bar plot:")
                plt.title("Stats en jeu de {} et de {} .".format(short_name, short_name2))
                st.pyplot(plt)


                #Word cloud joueur 1:
                # Libraries
                from wordcloud import WordCloud
                
                
                # Create a list of word
                player1_traits = st.session_state.player1.loc["result", "player_traits"]
                
                # Create the wordcloud object
                wordcloud = WordCloud(width=800, height=600, margin=0).generate(player1_traits)

                # Display the generated image:
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                plt.margins(x=0, y=0)
                plt.title("Attribut de {} .".format(short_name))
                st.subheader("Wordcloud joueur 1:")
                st.pyplot(plt)

                #Word cloud joueur 2:
                # Libraries
                from wordcloud import WordCloud
                from PIL import Image    # to import the image
                
                # Create a list of word
                player1_traits2 = st.session_state.player2.loc["result", "player_traits"]
                
                # Create the wordcloud object
                wordcloud = WordCloud(width=800, height=600, margin=0).generate(player1_traits2)

                # Display the generated image:
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                plt.margins(x=0, y=0)
                plt.title("Attribut de {} .".format(short_name2))
                st.subheader("Wordcloud joueur 2:")
                st.pyplot(plt)
                
                
                






     

    elif choice == 'Rechercher un joueur':

        st.subheader("Rechercher un joueur :")

        with st.container():
            left_column, midle_column, right_column = st.columns([4, 6, 5])
            with left_column:
                st.subheader('Filtres:')
                #filtres 
                countrys = list(df['nationality_name'].drop_duplicates())
                countrys.insert(0,'Selectionnez')
                country_choice = st.selectbox('Choose country:', countrys)

                postes = list(df['player_positions'].drop_duplicates())
                postes.insert(0,'Selectionnez')
                postes_choice = st.selectbox('Choose the player possition:', postes)

                leagues = list(df['league_name'].drop_duplicates())
                leagues.insert(0,'Selectionnez')
                league_choice = st.selectbox('Choose the league:', leagues)

                clubs = list(df['club_name'].drop_duplicates())
                clubs.insert(0,'Selectionnez')
                clubs_choice = st.selectbox('Choose the club:', clubs)

                notes_player = list(df['overall'].drop_duplicates())
                notes_choice = st.slider('Note max:', min_value=min(notes_player), max_value=95, step=1, value=0)

                value_eur = list(df['value_eur'].drop_duplicates())
                value_choice = st.slider('Player value max in eur:', min_value=min(value_eur), max_value=max(value_eur), step=100000.0, value=0.0)

                filter_button = st.button("Appliquez les filtres")
                cancel_filter_button = st.button("Enlever les filtres")
                
                
                if filter_button:
                    csv = convert_df(st.session_state.df_filter)

                    st.download_button(
                    "Télecharger le resultat de la recherche",
                    csv,
                    "file_result.csv",
                    "text/csv",
                    key='download-csv'
                    )

                if cancel_filter_button:
                    st.session_state.df_filter = df
                    # essayer de trouver un moyen pour mettre par default les select box
                
                if filter_button:
                    if "df_filter" not in st.session_state:
                        st.session_state.df_filter = df
                        

                    if country_choice != "Selectionnez":
                        st.session_state.df_filter = st.session_state.df_filter.loc[(st.session_state.df_filter["nationality_name"]==country_choice),:]
                        

                    if postes_choice != "Selectionnez":
                        st.session_state.df_filter = st.session_state.df_filter.loc[(st.session_state.df_filter["player_positions"]==postes_choice),:]
                        
                    
                    if league_choice != "Selectionnez":
                        st.session_state.df_filter = st.session_state.df_filter.loc[(st.session_state.df_filter["league_name"]==league_choice),:]
                        
                    
                    if clubs_choice != "Selectionnez":
                        st.session_state.df_filter = st.session_state.df_filter.loc[(st.session_state.df_filter["club_name"]==clubs_choice),:]
                       
                    
                    if notes_choice != 0:
                        st.session_state.df_filter = st.session_state.df_filter.loc[(st.session_state.df_filter["overall"] < notes_choice),:]
                        

                    if value_choice != 0:
                        st.session_state.df_filter = st.session_state.df_filter.loc[(st.session_state.df_filter["value_eur"] < value_choice),:] 
                            


            with midle_column:
                #show result
                st.subheader('Data:')
                if filter_button:
                    st.write(st.session_state.df_filter) 
                else:
                    st.write(df)
                
           
            with right_column:
                
                if filter_button:
                    st.subheader("Nombre de joueur trouvé: {}".format(len(st.session_state.df_filter)))

                    for index in range(len(st.session_state.df_filter)):
                        long_name = st.session_state.df_filter.iloc[index, 3]
                        flag_player = st.session_state.df_filter.iloc[index, 109]
                        image_player = st.session_state.df_filter.iloc[index, 105]
                        poste_player = st.session_state.df_filter.iloc[index, 4]
                        note_player = st.session_state.df_filter.iloc[index, 5]
                        team_player = st.session_state.df_filter.iloc[index, 106]
                        price_player = st.session_state.df_filter.iloc[index, 7]
                        age_player = st.session_state.df_filter.iloc[index, 9]
                        birth_player = st.session_state.df_filter.iloc[index, 10]
                        height_player = st.session_state.df_filter.iloc[index, 11]
                        weight_player = st.session_state.df_filter.iloc[index, 12]
                        
                        st.markdown(HTML_TEMPLATE_PLAYERS.format(long_name, flag_player, image_player,team_player,note_player, poste_player ),
                                    unsafe_allow_html=True)

                        # description
                        with st.expander("Plus d'infos"):
                            st.markdown(HTML_TEMPLATE_PLAYERS_DESC.format(
                            price_player, age_player, birth_player, height_player,weight_player),unsafe_allow_html=True)


if __name__ == '__main__':
    main()