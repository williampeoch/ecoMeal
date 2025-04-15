import streamlit as st
import pandas as pd
from Person import Person
import main

st.title("EcoMeal - Générateur de Repas Personnalisés")

# Interface utilisateur pour les informations personnelles
st.header("Vos Informations")

col1, col2 = st.columns(2)

with col1:
    sex = st.radio("Sexe", ["male", "female"])
    weight = st.number_input("Poids (kg)", min_value=30, max_value=200, value=70)
    height = st.number_input("Taille (cm)", min_value=100, max_value=250, value=170)

with col2:
    age = st.number_input("Âge", min_value=15, max_value=100, value=30)
    activity_levels = {
        "Sédentaire (peu ou pas d'exercice)": "0",
        "Légèrement actif (exercice léger 1-3 fois/semaine)": "1",
        "Modérément actif (exercice modéré 3-5 fois/semaine)": "2",
        "Très actif (exercice intense 6-7 fois/semaine)": "3",
        "Extrêmement actif (exercice très intense, travail physique)": "4"
    }
    level_activity = st.selectbox(
        "Niveau d'activité",
        options=list(activity_levels.keys())
    )

# Création de l'objet Person et calcul des besoins
if st.button("Calculer mes besoins"):
    person = Person(
        sex=sex,
        weight=weight,
        height=height,
        age=age,
        level_activity=activity_levels[level_activity]
    )
    
    needs = person.calculate_needs()
    
    st.header("Vos Besoins Nutritionnels Quotidiens")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Calories", f"{needs['calories']} kcal")
    with col2:
        st.metric("Protéines", f"{needs['protein']} g")
    with col3:
        st.metric("Lipides", f"{needs['fat']} g")
    with col4:
        st.metric("Glucides", f"{needs['carb']} g")
    
    # Génération des repas
    st.header("Génération de Repas")
    if st.button("Générer des repas"):
        with st.spinner("Génération des repas en cours..."):
            # Utilisation de l'algorithme de main.py pour générer les repas
            population, generations = main.run_evolution(
                populate_func=partial(
                    main.generate_population,
                    size=10,
                    genome_length=len(main.aliments)
                ),
                fitness_func=lambda genome: main.fitness(
                    genome,
                    main.aliments,
                    needs['calories'],
                    needs['protein'],
                    needs['fat'],
                    needs['carb']
                ),
                fitness_limit=1000,
                generation_limit=100
            )
            
            # Affichage des repas générés
            best_solution = population[0]
            meals = main.genome_to_aliments(best_solution, main.aliments)
            macros = main.calculate_macros(best_solution, main.aliments)
            
            st.subheader("Repas Proposé")
            for meal in meals:
                st.write(f"• {meal}")
            
            st.subheader("Valeurs Nutritionnelles du Repas")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calories", f"{macros['calories']:.0f} kcal")
            with col2:
                st.metric("Protéines", f"{macros['protein']:.0f} g")
            with col3:
                st.metric("Lipides", f"{macros['fat']:.0f} g")
            with col4:
                st.metric("Glucides", f"{macros['carb']:.0f} g")