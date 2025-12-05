import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split


# -----------------------------------------------------------
# 1. Cargar datasets
# -----------------------------------------------------------
base_path = os.getcwd()
mega_file = os.path.join(base_path, "Data", "megaGymDataset.csv")
exercise_file = os.path.join(base_path, "Data", "GymExercisesDataset.xlsx")

gym1 = pd.read_excel(exercise_file)
gym2 = pd.read_csv(mega_file)


# -----------------------------------------------------------
# 2. Mapa de normalización de músculos
# -----------------------------------------------------------
MUSCLE_MAP = {
    "abs": "abs",
    "abdominals": "abs",
    "core": "abs",

    "quadriceps": "legs",
    "quads": "legs",
    "hamstrings": "legs",
    "calves": "legs",
    "legs": "legs",
    "leg": "legs",

    "chest": "chest",
    "pectorals": "chest",
    "pecs": "chest",

    "back": "back",
    "lats": "back",
    "latissimus": "back",
    "lower back": "back",
    "upper back": "back",

    "shoulders": "shoulders",
    "deltoids": "shoulders",
    "delts": "shoulders",

    "biceps": "biceps",
    "triceps": "triceps",

    "glutes": "glutes",
    "buttocks": "glutes",
    "gluteus": "glutes",
}


def normalize_muscle(muscle: str):
    muscle = str(muscle).lower()
    for key in MUSCLE_MAP:
        if key in muscle:
            return MUSCLE_MAP[key]
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


# -----------------------------------------------------------
# 3. Unificar datasets + limpiar
# -----------------------------------------------------------
clean1 = pd.DataFrame({
    "Exercise_Name": gym1["Exercise_Name"],
    "muscles": gym1["muscle_gp"].apply(clean_muscles),
    "equipment": gym1["Equipment"],
    "description": gym1["Description"]
})

clean2 = pd.DataFrame({
    "Exercise_Name": gym2["Title"],
    "muscles": gym2["BodyPart"].apply(clean_muscles),
    "equipment": gym2["Equipment"],
    "description": gym2["Desc"]
})

df = pd.concat([clean1, clean2], ignore_index=True)

df = df[df["muscles"].map(len) > 0]
df = df.dropna(subset=["Exercise_Name"])

df.reset_index(drop=True, inplace=True)


# -----------------------------------------------------------
# 4. One-hot encoding (MLB)
# -----------------------------------------------------------
mlb = MultiLabelBinarizer()
muscle_matrix = mlb.fit_transform(df["muscles"])
feature_matrix = muscle_matrix


# -----------------------------------------------------------
# 5. Vector usuario normalizado
# -----------------------------------------------------------
def build_user_vector(priorities_dict):
    base = 0.1
    user_vector = np.full(len(mlb.classes_), base)

    for muscle, prio in priorities_dict.items():
        muscle = muscle.lower()
        if muscle in mlb.classes_:
            idx = list(mlb.classes_).index(muscle)
            user_vector[idx] = 0.1 + (prio / 10.0) * 0.9

    return user_vector.reshape(1, -1)


# -----------------------------------------------------------
# 6. Recomendador por músculo
# -----------------------------------------------------------
def recommend_by_muscle(priorities_dict, exercises_per_muscle=5):
    user_vec = build_user_vector(priorities_dict)

    sim = cosine_similarity(user_vec, feature_matrix)[0]
    df["similarity"] = sim

    results_by_muscle = {}

    for muscle in priorities_dict.keys():
        muscle = muscle.lower()
        if muscle not in mlb.classes_:
            continue

        muscle_exercises = df[df["muscles"].apply(lambda x: muscle in x)]
        muscle_exercises = muscle_exercises.sort_values("similarity", ascending=False)

        top_n = muscle_exercises.head(exercises_per_muscle)

        results_by_muscle[muscle] = top_n[["Exercise_Name", "muscles", "equipment", "similarity"]]

    return results_by_muscle


# -----------------------------------------------------------
# 7. Métricas
# -----------------------------------------------------------
def precision_recall_k(k=5, test_size=0.25):
    train, test = train_test_split(df, test_size=test_size, random_state=42)

    precision_list = []
    recall_list = []

    for _, row in test.iterrows():
        target = row["muscles"]

        if len(target) == 0:
            continue

        priorities = {m: 10 for m in target}

        recs = recommend_by_muscle(priorities, exercises_per_muscle=k)

        if not recs:
            continue

        hits = 0
        total_recs = 0

        for muscle_df in recs.values():
            for rec_muscles in muscle_df["muscles"]:
                if len(set(rec_muscles).intersection(target)) > 0:
                    hits += 1
                total_recs += 1

        if total_recs == 0:
            continue

        precision_list.append(hits / total_recs)
        recall_list.append(hits / len(target))

    if len(precision_list) == 0 or len(recall_list) == 0:
        return 0, 0

    return float(np.mean(precision_list)), float(np.mean(recall_list))


# -----------------------------------------------------------
# 8. Ejecutar métricas
# -----------------------------------------------------------
precision, recall = precision_recall_k(k=5)

print("\n===== MÉTRICAS =====")
print("Precision@5:", round(precision, 3))
print("Recall@5:", round(recall, 3))


# -----------------------------------------------------------
# 9. Ejemplo de uso
# -----------------------------------------------------------
user_priorities = {
    "biceps": 5,
    "chest": 6,
    "abs": 7,
}

recommendations = recommend_by_muscle(user_priorities, exercises_per_muscle=5)

print("\n====================================")
print("        RECOMENDACIONES")
print("====================================")

for muscle, recs in recommendations.items():
    print(f"\n===== {muscle.upper()} =====")
    print(recs)


# -----------------------------------------------------------
# 10. (Opcional) Exportar a Excel
# -----------------------------------------------------------
export = False  # Cambia a True si quieres exportar

if export:
    with pd.ExcelWriter("recomendaciones.xlsx") as writer:
        for muscle, recs in recommendations.items():
            recs.to_excel(writer, sheet_name=muscle[:30], index=False)

    print("\n✅ Archivo 'recomendaciones.xlsx' creado")
