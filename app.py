import streamlit as st

st.set_page_config(page_title="Calcul nutrition", layout="centered")

st.title("🧪 Calcul des besoins nutritionnels")

# Section 1 : Durée totale
duree_entrainement = st.slider("⏱️ Durée totale de l'entraînement (en heures)", 1.0, 6.0, 3.0, step=0.25)

# Section 2 : Intensités spécifiques
st.subheader("🎯 Durée des intensités (en minutes)")

z6 = st.number_input("Zone 6/5 (VO2 max)", min_value=0, step=1)
z4 = st.number_input("Zone 4 (Seuil)", min_value=0, step=1)
z3 = st.number_input("Zone 3 (Tempo)", min_value=0, step=1)

# Calcul de l’apport glucidique
def calcul_apport_glucides(duree_h, z6_min, z4_min, z3_min):
    # Apport de base selon durée
    if duree_h <= 1.5:
        base = 20
    elif duree_h >= 6:
        base = 120
    else:
        base = 20 + (duree_h - 1.5) * (100 / 4.5)  # interpolation linéaire entre 1.5h et 6h

    # Glucides totaux de base
    glucides_base_totaux = base * duree_h

    # Ajouts liés aux intensités
    ajout = z6_min * 2 + z4_min * 1 + z3_min * 0.5

    total = glucides_base_totaux + ajout
    total_par_heure = total / duree_h

    if total_par_heure > 120:
        total_par_heure = 120
        total = 120 * duree_h

    return round(total), round(total_par_heure)

def get_ratio_info(glucides_par_heure, total_glucides):
    if glucides_par_heure <= 50:
        ratio = (1, 0)
    elif glucides_par_heure <= 70:
        ratio = (1, 0.5)
    elif glucides_par_heure <= 100:
        ratio = (1, 0.8)
    else:
        ratio = (1, 1)

    glucose_fraction = 1 / (1 + ratio[1])
    fructose_fraction = ratio[1] / (1 + ratio[1])

    glucose_total = round(total_glucides * glucose_fraction)
    fructose_total = round(total_glucides * fructose_fraction)

    return ratio, glucose_total, fructose_total

# Appel à la fonction d'apport glucidique
glucides_totaux, glucides_par_heure = calcul_apport_glucides(duree_entrainement, z6, z4, z3)

# Puis passage dans la fonction du ratio
ratio, glucose_g, fructose_g = get_ratio_info(glucides_par_heure, glucides_totaux)

def recommander_boisson(glucides_par_heure, ratio):
    boisson_ml = 500
    glucides_boisson = 40  # g/h

    if ratio[1] == 0:
        # Glucose seul
        glucose = glucides_boisson
        fructose = 0
        type_boisson = "💧 Eau + glucose (dextrose ou maltodextrine)"
    else:
        # Respecter le ratio
        glucose_fraction = 1 / (1 + ratio[1])
        fructose_fraction = ratio[1] / (1 + ratio[1])

        glucose = round(glucides_boisson * glucose_fraction)
        fructose = round(glucides_boisson * fructose_fraction)

        type_boisson = "💧 Eau + glucose + fructose (respect du ratio)"

    return type_boisson, boisson_ml, glucose, fructose


# Résultat
glucides_totaux, glucides_par_heure = calcul_apport_glucides(duree_entrainement, z6, z4, z3)

st.success(f"💡 Apport total recommandé : {glucides_totaux} g de glucides")
st.info(f"⚖️ Soit environ {glucides_par_heure} g/h")
st.subheader("🔬 Recommandation de répartition Glucose / Fructose")
st.write(f"✅ Ratio recommandé : **{ratio[0]} / {ratio[1]}**")
st.write(f"🍬 Quantité de glucose (ou dextrose ou maltodextrine) : **{glucose_g} g**")
st.write(f"🍭 Quantité de fructose : **{fructose_g} g**")

st.subheader("🚰 Recommandation de boisson par heure")

st.markdown("""
> **Si utilisation de boisson d'effort :**  
> Vérifiez bien la quantité et la répartition de glucides dans votre boisson d’effort **pour chaque dose utilisée**.  
> Si votre apport recommandé est **inférieur à 50 g/h**, vous **n’êtes pas obligé** d’avoir 40 g/h dans la boisson.  
> Mais veillez **toujours à boire 500 mL/h d’eau** pour optimiser l’absorption intestinale.  
""")


type_boisson, volume_ml, glucose_bois, fructose_bois = recommander_boisson(glucides_par_heure, ratio)

st.write(f"✅ Type : {type_boisson}")
st.write(f"🧪 Volume : **{volume_ml} mL/h**")
st.write(f"🍬 Glucose (ou malto ou dextrose) dans boisson : **{glucose_bois} g**")
st.write(f"🍭 Fructose dans boisson : **{fructose_bois} g**")

st.subheader("🍴 Recommandations sur les aliments solides")

st.markdown("""
> **Conseils pratiques :**
>
> - Les **gels** sont souvent le meilleur choix pour compléter l’apport glucidique en dehors de la boisson.  
> - En entraînement, les **rice cakes** sont une excellente option et sont faciles à faire à la maison.  
> - Pour les **barres** ou tout autre produit solide industriel, **vérifiez toujours la composition nutritionnelle** (pour 100 g, indiquée obligatoirement sur l’emballage) :
>   - ❌ Évitez les produits qui dépassent :
>     - **2 g de lipides**
>     - **2 g de protéines**
>     - **2 g de fibres**
>   - Ces nutriments ralentissent l’absorption des glucides et peuvent provoquer des troubles digestifs.  
> - 🚴‍♂️ **En course, utilisez exclusivement des gels** pour garantir une absorption rapide et efficace.
""")

st.subheader("🔍 À propos des produits industriels")

st.markdown("""
> ⚠️ **Information importante :**
>
> Pour les produits industriels, **vérifiez toujours la composition complète**.  
> Certains peuvent contenir des **additifs, colorants, édulcorants ou ingrédients transformés** mauvais pour la santé à long terme.  
> 👉 **C’est pourquoi nous ne recommandons pas les bonbons**, même s’ils contiennent du sucre : leur composition n'est très souvent pas bonne !
""")

