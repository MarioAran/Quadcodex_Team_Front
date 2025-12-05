import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

# ================================
# 1. PATHS
# ================================
base_path = os.getcwd()

mega_file = os.path.join(base_path, "Data", "megaGymDataset.csv")
exercise_file = os.path.join(base_path, "Data", "GymExercisesDataset.xlsx")
ratings_file = os.path.join(base_path, "Data", "usuarios_ejercicios_valoraciones.csv")

# Usuario que se quiere simular
CURRENT_USER = {
    "genero": "male",
    "edad": 25,
    "peso": 72,
    "altura": 175
}


# ================================
# 2. Cargar datasets
# ================================
gym1 = pd.read_excel(exercise_file)
gym2 = pd.read_csv(mega_file)
ratings_df = pd.read_csv(ratings_file)


# ================================
# 3. Mapa de músculos
# ================================
MUSCLE_MAP = {
    "abs": "abs",
    "abdominals": "abs",
    "core": "abs",
    "quadriceps": "legs",
    "quads": "legs",
    "hamstrings": "legs",
    "calves": "legs",
    "legs": "legs",
    "chest": "chest",
    "pectorals": "chest",
    "pecs": "chest",
    "back": "back",
    "lats": "back",
    "latissimus": "back",
    "shoulders": "shoulders",
    "deltoids": "shoulders",
    "biceps": "biceps",
    "triceps": "triceps",
    "glutes": "glutes",
}


def normalize_muscle(m):
    m = str(m).lower()
    for key, val in MUSCLE_MAP.items():
        if key in m:
            return val
    return None


def clean_muscles(x):
    if pd.isna(x):
        return []
    if isinstance(x, list):
        return [normalize_muscle(t) for t in x if normalize_muscle(t)]
    if isinstance(x, str):
        tokens = [t.strip().lower() for t in x.replace(";", ",").split(",")]
        return list(set([normalize_muscle(t) for t in tokens if normalize_muscle(t)]))
    return []


# ================================
# 4. Unificar datasets ejercicios
# ================================
clean1 = pd.DataFrame({
    "Exercise_Name": gym1["Exercise_Name"],
    "muscles": gym1["muscle_gp"].apply(clean_muscles),
    "equipment": gym1["Equipment"]
})

clean2 = pd.DataFrame({
    "Exercise_Name": gym2["Title"],
    "muscles": gym2["BodyPart"].apply(clean_muscles),
    "equipment": gym2["Equipment"]
})

df = pd.concat([clean1, clean2], ignore_index=True)

df = df[df["muscles"].map(len) > 0]
df = df.dropna(subset=["Exercise_Name"])
df.reset_index(drop=True, inplace=True)

# Le damos un id artificial para empatar con ratings
df["id_ejercicio"] = df.index


# ================================
# 5. One hot (MLB)
# ================================
mlb = MultiLabelBinarizer()
feature_matrix = mlb.fit_transform(df["muscles"])


# ================================
# 6. SIMILITUD ENTRE USUARIOS
# ================================
ratings_df["genero"] = ratings_df["genero"].map({"male": 1, "female": 0})

user_vector = np.array([
    1 if CURRENT_USER["genero"] == "male" else 0,
    CURRENT_USER["edad"],
    CURRENT_USER["peso"],
    CURRENT_USER["altura"]
]).reshape(1, -1)

users_features = ratings_df[["genero", "edad", "peso", "altura"]].values

user_sim = cosine_similarity(user_vector, users_features)[0]

ratings_df["user_similarity"] = user_sim


# ================================
# 7. SCORE DE CADA EJERCICIO SEGÚN USUARIOS SIMILARES
# ================================
weighted_ratings = (
    ratings_df["valoracion"] * ratings_df["user_similarity"]
)

exercise_rating = (
    ratings_df.groupby("id_ejercicio")
    .apply(lambda x: np.average(x["valoracion"], weights=x["user_similarity"]))
)

exercise_rating = exercise_rating.fillna(0)

df["rating_score"] = df["id_ejercicio"].map(exercise_rating)
df["rating_score"] = df["rating_score"].fillna(0)


# ================================
# 8. PRIORIDADES (puedes editarlas)
# ================================
user_priorities = {
    "chest": 9,
    "back": 8,
    "legs": 9,
    "shoulders": 7,
    "biceps": 6,
    "triceps": 6,
    "abs": 6,
}


# ================================
# 9. VECTOR USUARIO PARA COSENO
# ================================
def build_user_vector(priorities_dict):
    base = 0.1
    user_vector = np.full(len(mlb.classes_), base)

    for muscle, prio in priorities_dict.items():
        if muscle in mlb.classes_:
            idx = list(mlb.classes_).index(muscle)
            user_vector[idx] = 0.1 + (prio / 10.0) * 0.9

    return user_vector.reshape(1, -1)


# ================================
# 10. RECOMENDADOR HÍBRIDO
# ================================
def hybrid_recommender(priorities_dict, n_per_muscle=5):

    user_vec = build_user_vector(priorities_dict)

    content_sim = cosine_similarity(user_vec, feature_matrix)[0]
    df["content_similarity"] = content_sim

    # normalizar rating 0-1
    scaler = MinMaxScaler()
    df["rating_norm"] = scaler.fit_transform(df[["rating_score"]])

    # SCORE FINAL
    df["final_score"] = (
        0.6 * df["content_similarity"] +
        0.4 * df["rating_norm"]
    )

    results = {}

    for muscle in priorities_dict.keys():
        if muscle not in mlb.classes_:
            continue

        filtered = df[df["muscles"].apply(lambda x: muscle in x)]
        filtered = filtered.sort_values("final_score", ascending=False)

        results[muscle] = filtered.head(n_per_muscle)[
            ["Exercise_Name", "muscles", "equipment",
             "rating_score", "final_score"]
        ]

    return results


# ================================
# 11. EJECUCIÓN
# ================================
recommendations = hybrid_recommender(user_priorities, 5)

print("\n====================================")
print("     RECOMENDACIONES HÍBRIDAS")
print("====================================")

for muscle, recs in recommendations.items():
    print(f"\n===== {muscle.upper()} =====")
    print(recs)
