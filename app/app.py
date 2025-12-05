import streamlit as st
import random
from datetime import date
import re

# Configuración de la página
st.set_page_config(
    page_title="Algo Fit - Fitness App",
    page_icon="💪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== SISTEMA DE IDIOMAS ==========
def setup_languages():
    """Configura el sistema de idiomas"""
    if 'language' not in st.session_state:
        st.session_state.language = 'es'
    
    # Diccionarios de traducción
    translations = {
        'es': {
            'app_title': 'Algo Fit - Fitness App',
            'form_title': '¡Regístrate y únete a nuestra comunidad!',
            'form_subtitle': 'Completa tus datos personales para unirte a nuestra comunidad.',
            'personal_data': 'Datos Personales',
            'physical_info': 'Información física y objetivos',
            'full_name': 'Nombre completo *',
            'gender': 'Género *',
            'select_gender': 'Selecciona tu género',
            'male': 'Masculino',
            'female': 'Femenino',
            'birth_date': 'Fecha de nacimiento *',
            'age': 'Edad *',
            'height': 'Altura (cm) *',
            'weight': 'Peso (kg) *',
            'objective': 'Objetivo *',
            'select_objective': 'Selecciona un objetivo',
            'gain_muscle': 'Ganar músculo/peso',
            'lose_weight': 'Perder peso',
            'experience': 'Experiencia en gimnasio *',
            'select_experience': 'Selecciona tu experiencia en gimnasio',
            'beginner': 'Principiante (0-6 meses)',
            'intermediate': 'Intermedio (6-12 meses)',
            'expert': 'Experto (>12 meses)',
            'send': 'Enviar',
            'required_note': 'Todos los campos marcados con * son obligatorios.',
            'select_exercises': 'Selecciona la cantidad de ejercicios',
            'recommend': 'Recomendar',
            'personal_info': 'Información Personal',
            'recommended_exercises': 'Ejercicios Recomendados',
            'loading': 'Generando tu rutina personalizada...',
            'no_data_error': 'Primero debes completar tu información personal.',
            'invalid_number': 'Por favor, selecciona un número entre 1 y 10.',
            'body_zone': 'Zona Corporal',
            'muscle_group': 'Grupo Muscular',
            'series': 'Series',
            'repetitions': 'Repeticiones',
            'rest': 'Descanso',
            'equipment': 'Equipo',
            'difficulty': 'Dificultad',
            'back': 'Espalda',
            'chest': 'Pecho',
            'legs': 'Piernas',
            'back_to_adjust': '← Volver a ajustar cantidad',
            'no_exercises': 'No se encontraron ejercicios.',
            'showing': 'Mostrando {count} ejercicios recomendados',
            'all_exercises': 'Solo disponemos de {count} ejercicios. Mostrando todos.'
        },
        'ca': {
            'app_title': 'Algo Fit - Aplicació de Fitness',
            'form_title': 'Registra\'t i uneix-te a la nostra comunitat!',
            'form_subtitle': 'Completa les teves dades personals per unir-te a la nostra comunitat.',
            'personal_data': 'Dades Personals',
            'physical_info': 'Informació física i objectius',
            'full_name': 'Nom complet *',
            'gender': 'Gènere *',
            'select_gender': 'Selecciona el teu gènere',
            'male': 'Masculí',
            'female': 'Femení',
            'birth_date': 'Data de naixement *',
            'age': 'Edat *',
            'height': 'Alçada (cm) *',
            'weight': 'Pes (kg) *',
            'objective': 'Objectiu *',
            'select_objective': 'Selecciona un objectiu',
            'gain_muscle': 'Guanyar múscul/pes',
            'lose_weight': 'Perdre pes',
            'experience': 'Experiència en gimnàs *',
            'select_experience': 'Selecciona la teva experiència en gimnàs',
            'beginner': 'Principiant (0-6 mesos)',
            'intermediate': 'Intermedi (6-12 mesos)',
            'expert': 'Expert (>12 mesos)',
            'send': 'Enviar',
            'required_note': 'Tots els camps marcats amb * són obligatoris.',
            'select_exercises': 'Selecciona la quantitat d\'exercicis',
            'recommend': 'Recomanar',
            'personal_info': 'Informació Personal',
            'recommended_exercises': 'Exercicis Recomanats',
            'loading': 'Generant la teva rutina personalitzada...',
            'no_data_error': 'Primer has de completar la teva informació personal.',
            'invalid_number': 'Si us plau, selecciona un número entre 1 i 10.',
            'body_zone': 'Zona Corporal',
            'muscle_group': 'Grup Muscular',
            'series': 'Sèries',
            'repetitions': 'Repeticions',
            'rest': 'Descans',
            'equipment': 'Equip',
            'difficulty': 'Dificultat',
            'back': 'Esquena',
            'chest': 'Pit',
            'legs': 'Cames',
            'back_to_adjust': '← Tornar a ajustar quantitat',
            'no_exercises': 'No s\'han trobat exercicis.',
            'showing': 'Mostrant {count} exercicis recomanats',
            'all_exercises': 'Només disposem de {count} exercicis. Mostrant tots.'
        },
        'en': {
            'app_title': 'Algo Fit - Fitness App',
            'form_title': 'Sign up and join our community!',
            'form_subtitle': 'Fill in your personal details to join our community.',
            'personal_data': 'Personal Data',
            'physical_info': 'Physical information and objectives',
            'full_name': 'Full name *',
            'gender': 'Gender *',
            'select_gender': 'Select your gender',
            'male': 'Male',
            'female': 'Female',
            'birth_date': 'Birth date *',
            'age': 'Age *',
            'height': 'Height (cm) *',
            'weight': 'Weight (kg) *',
            'objective': 'Objective *',
            'select_objective': 'Select an objective',
            'gain_muscle': 'Gain muscle/weight',
            'lose_weight': 'Lose weight',
            'experience': 'Gym experience *',
            'select_experience': 'Select your gym experience',
            'beginner': 'Beginner (0-6 months)',
            'intermediate': 'Intermediate (6-12 months)',
            'expert': 'Expert (>12 months)',
            'send': 'Send',
            'required_note': 'All fields marked with * are required.',
            'select_exercises': 'Select the number of exercises',
            'recommend': 'Recommend',
            'personal_info': 'Personal Information',
            'recommended_exercises': 'Recommended Exercises',
            'loading': 'Generating your personalized routine...',
            'no_data_error': 'First you must complete your personal information.',
            'invalid_number': 'Please select a number between 1 and 10.',
            'body_zone': 'Body Zone',
            'muscle_group': 'Muscle Group',
            'series': 'Series',
            'repetitions': 'Repetitions',
            'rest': 'Rest',
            'equipment': 'Equipment',
            'difficulty': 'Difficulty',
            'back': 'Back',
            'chest': 'Chest',
            'legs': 'Legs',
            'back_to_adjust': '← Back to adjust quantity',
            'no_exercises': 'No exercises found.',
            'showing': 'Showing {count} recommended exercises',
            'all_exercises': 'We only have {count} exercises available. Showing all.'
        },
        'fr': {
            'app_title': 'Algo Fit - Application de Fitness',
            'form_title': 'Inscrivez-vous et rejoignez notre communauté !',
            'form_subtitle': 'Remplissez vos informations personnelles pour rejoindre notre communauté.',
            'personal_data': 'Données Personnelles',
            'physical_info': 'Informations physiques et objectifs',
            'full_name': 'Nom complet *',
            'gender': 'Genre *',
            'select_gender': 'Sélectionnez votre genre',
            'male': 'Masculin',
            'female': 'Féminin',
            'birth_date': 'Date de naissance *',
            'age': 'Âge *',
            'height': 'Taille (cm) *',
            'weight': 'Poids (kg) *',
            'objective': 'Objectif *',
            'select_objective': 'Sélectionnez un objectif',
            'gain_muscle': 'Gagner du muscle/poids',
            'lose_weight': 'Perdre du poids',
            'experience': 'Expérience en salle de sport *',
            'select_experience': 'Sélectionnez votre expérience en salle de sport',
            'beginner': 'Débutant (0-6 mois)',
            'intermediate': 'Intermédiaire (6-12 mois)',
            'expert': 'Expert (>12 mois)',
            'send': 'Envoyer',
            'required_note': 'Tous les champs marqués d\'un * sont obligatoires.',
            'select_exercises': 'Sélectionnez le nombre d\'exercices',
            'recommend': 'Recommander',
            'personal_info': 'Informations Personnelles',
            'recommended_exercises': 'Exercices Recommandés',
            'loading': 'Génération de votre routine personnalisée...',
            'no_data_error': 'Vous devez d\'abord compléter vos informations personnelles.',
            'invalid_number': 'Veuillez sélectionner un nombre entre 1 et 10.',
            'body_zone': 'Zone Corporelle',
            'muscle_group': 'Groupe Musculaire',
            'series': 'Séries',
            'repetitions': 'Répétitions',
            'rest': 'Repos',
            'equipment': 'Équipement',
            'difficulty': 'Difficulté',
            'back': 'Dos',
            'chest': 'Poitrine',
            'legs': 'Jambes',
            'back_to_adjust': '← Retour pour ajuster la quantité',
            'no_exercises': 'Aucun exercice trouvé.',
            'showing': 'Affichage de {count} exercices recommandés',
            'all_exercises': 'Nous n\'avons que {count} exercices disponibles. Affichage de tous.'
        },
        'de': {
            'app_title': 'Algo Fit - Fitness App',
            'form_title': 'Melden Sie sich an und werden Sie Teil unserer Community!',
            'form_subtitle': 'Füllen Sie Ihre persönlichen Daten aus, um unserer Community beizutreten.',
            'personal_data': 'Persönliche Daten',
            'physical_info': 'Körperliche Informationen und Ziele',
            'full_name': 'Vollständiger Name *',
            'gender': 'Geschlecht *',
            'select_gender': 'Wählen Sie Ihr Geschlecht',
            'male': 'Männlich',
            'female': 'Weiblich',
            'birth_date': 'Geburtsdatum *',
            'age': 'Alter *',
            'height': 'Größe (cm) *',
            'weight': 'Gewicht (kg) *',
            'objective': 'Ziel *',
            'select_objective': 'Wählen Sie ein Ziel',
            'gain_muscle': 'Muskeln/Gewicht zunehmen',
            'lose_weight': 'Gewicht verlieren',
            'experience': 'Fitnessstudio-Erfahrung *',
            'select_experience': 'Wählen Sie Ihre Fitnessstudio-Erfahrung',
            'beginner': 'Anfänger (0-6 Monate)',
            'intermediate': 'Fortgeschritten (6-12 Monate)',
            'expert': 'Experte (>12 Monate)',
            'send': 'Senden',
            'required_note': 'Alle mit * markierten Felder sind Pflichtfelder.',
            'select_exercises': 'Wählen Sie die Anzahl der Übungen',
            'recommend': 'Empfehlen',
            'personal_info': 'Persönliche Informationen',
            'recommended_exercises': 'Empfohlene Übungen',
            'loading': 'Erstelle Ihre personalisierte Routine...',
            'no_data_error': 'Zuerst müssen Sie Ihre persönlichen Daten vervollständigen.',
            'invalid_number': 'Bitte wählen Sie eine Zahl zwischen 1 und 10.',
            'body_zone': 'Körperzone',
            'muscle_group': 'Muskelgruppe',
            'series': 'Serien',
            'repetitions': 'Wiederholungen',
            'rest': 'Pause',
            'equipment': 'Ausrüstung',
            'difficulty': 'Schwierigkeit',
            'back': 'Rücken',
            'chest': 'Brust',
            'legs': 'Beine',
            'back_to_adjust': '← Zurück zur Mengenanpassung',
            'no_exercises': 'Keine Übungen gefunden.',
            'showing': 'Zeige {count} empfohlene Übungen',
            'all_exercises': 'Wir haben nur {count} Übungen verfügbar. Zeige alle.'
        }
    }
    
    return translations[st.session_state.language]

# ========== CLASES PARA MANEJAR DATOS ==========
class UsuarioDatos:
    def __init__(self, nombre, apellido, edad, genero, altura, peso, objetivo, nivel):
        self.Nombre = nombre
        self.Apellido = apellido
        self.Edad = edad
        self.Genero = genero
        self.Altura = altura
        self.Peso = peso
        self.Objetivo = objetivo
        self.Nivel = nivel

class GestorUsuario:
    def get_usuario(self, nombre_completo, edad, genero, altura, peso, objetivo, nivel):
        nombre, apellido = self.verif_nombre(nombre_completo)
        edad = self.verif_edad(edad)
        genero = self.verif_genero(genero)
        altura = self.verif_altura(altura)
        peso = self.verif_peso(peso)
        objetivo = self.verif_objetivo(objetivo)
        nivel = self.verif_nivel(nivel)

        return UsuarioDatos(
            nombre=nombre,
            apellido=apellido,
            edad=edad,
            genero=genero,
            altura=altura,
            peso=peso,
            objetivo=objetivo,
            nivel=nivel
        )

    def verif_nombre(self, nombre_completo):
        partes = nombre_completo.strip().split()
        if len(partes) == 0:
            return ("", "")
        nombre = partes[0]
        apellido = " ".join(partes[1:]) if len(partes) > 1 else ""
        return (nombre, apellido)

    def verif_edad(self, edad):
        return max(12, min(edad, 80))

    def verif_genero(self, genero):
        if genero in ["Male", "Masculino", "Masculí", "Masculin", "Männlich"]:
            return "Male"
        if genero in ["Female", "Femenino", "Femení", "Féminin", "Weiblich"]:
            return "Female"
        return "Other"

    def verif_altura(self, altura):
        return max(100, min(altura, 270))

    def verif_peso(self, peso):
        return max(30, min(peso, 300))

    def verif_objetivo(self, objetivo):
        objetivo = objetivo.lower()
        if any(word in objetivo for word in ['gain', 'ganar', 'guanyar', 'gagner', 'zunehmen']):
            return "Gain muscle"
        if any(word in objetivo for word in ['lose', 'perder', 'perdre', 'verlieren']):
            return "Lose weight"
        return "Unknown"

    def verif_nivel(self, nivel):
        # Extraer solo la parte principal del nivel
        nivel = nivel.split("(")[0].strip()
        if any(word in nivel.lower() for word in ['beginner', 'principiante', 'principiant', 'débutant', 'anfänger']):
            return "Beginner"
        if any(word in nivel.lower() for word in ['intermediate', 'intermedio', 'intermedi', 'intermédiaire', 'fortgeschritten']):
            return "Intermediate"
        if any(word in nivel.lower() for word in ['expert', 'experto', 'expert', 'expert', 'experte']):
            return "Expert"
        return nivel

# ========== BASE DE DATOS DE EJERCICIOS ==========
def get_exercises(lang='es'):
    """Devuelve la lista de ejercicios en el idioma especificado"""
    
    exercises_db = {
        'es': [
            {
                "id": 1,
                "nombre": "Dominadas",
                "grupoMuscular": "Espalda Superior",
                "zonaCorporal": "Espalda",
                "grupoMuscularEspecifico": "Dorsales",
                "series": 4,
                "repeticiones": "8-12",
                "descanso": "90s",
                "equipo": "Barra",
                "dificultad": 3,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204560631664864/espalda.jpg"
            },
            {
                "id": 2,
                "nombre": "Press de Banca",
                "grupoMuscular": "Pecho Superior",
                "zonaCorporal": "Pecho",
                "grupoMuscularEspecifico": "Pectoral Mayor",
                "series": 3,
                "repeticiones": "10-15",
                "descanso": "60s",
                "equipo": "Barra y Banco",
                "dificultad": 2,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561155948676/pecho_2.jpg"
            },
            {
                "id": 3,
                "nombre": "Sentadillas",
                "grupoMuscular": "Pierna Completa",
                "zonaCorporal": "Piernas",
                "grupoMuscularEspecifico": "Cuádriceps",
                "series": 4,
                "repeticiones": "12-15",
                "descanso": "120s",
                "equipo": "Barra",
                "dificultad": 4,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561508536320/pierna.jpg"
            },
            {
                "id": 4,
                "nombre": "Remo con Barra",
                "grupoMuscular": "Espalda Media",
                "zonaCorporal": "Espalda",
                "grupoMuscularEspecifico": "Dorsales y Trapecio",
                "series": 3,
                "repeticiones": "8-10",
                "descanso": "75s",
                "equipo": "Barra y Pesas",
                "dificultad": 2,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204560631664864/espalda.jpg"
            },
            {
                "id": 5,
                "nombre": "Aperturas con Mancuernas",
                "grupoMuscular": "Pecho Externo",
                "zonaCorporal": "Pecho",
                "grupoMuscularEspecifico": "Pectoral Mayor",
                "series": 4,
                "repeticiones": "12-15",
                "descanso": "45s",
                "equipo": "Mancuernas y Banco",
                "dificultad": 3,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561155948676/pecho_2.jpg"
            },
            {
                "id": 6,
                "nombre": "Prensa de Piernas",
                "grupoMuscular": "Cuádriceps y Glúteos",
                "zonaCorporal": "Piernas",
                "grupoMuscularEspecifico": "Cuádriceps",
                "series": 3,
                "repeticiones": "15-20",
                "descanso": "60s",
                "equipo": "Máquina de Prensa",
                "dificultad": 1,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561508536320/pierna.jpg"
            }
        ],
        'en': [
            {
                "id": 1,
                "nombre": "Pull-ups",
                "grupoMuscular": "Upper Back",
                "zonaCorporal": "Back",
                "grupoMuscularEspecifico": "Lats",
                "series": 4,
                "repeticiones": "8-12",
                "descanso": "90s",
                "equipo": "Bar",
                "dificultad": 3,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204560631664864/espalda.jpg"
            },
            {
                "id": 2,
                "nombre": "Bench Press",
                "grupoMuscular": "Upper Chest",
                "zonaCorporal": "Chest",
                "grupoMuscularEspecifico": "Pectoralis Major",
                "series": 3,
                "repeticiones": "10-15",
                "descanso": "60s",
                "equipo": "Bar and Bench",
                "dificultad": 2,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561155948676/pecho_2.jpg"
            },
            {
                "id": 3,
                "nombre": "Squats",
                "grupoMuscular": "Full Leg",
                "zonaCorporal": "Legs",
                "grupoMuscularEspecifico": "Quadriceps",
                "series": 4,
                "repeticiones": "12-15",
                "descanso": "120s",
                "equipo": "Bar",
                "dificultad": 4,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561508536320/pierna.jpg"
            },
            {
                "id": 4,
                "nombre": "Barbell Row",
                "grupoMuscular": "Middle Back",
                "zonaCorporal": "Back",
                "grupoMuscularEspecifico": "Lats and Trapezius",
                "series": 3,
                "repeticiones": "8-10",
                "descanso": "75s",
                "equipo": "Bar and Weights",
                "dificultad": 2,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204560631664864/espalda.jpg"
            },
            {
                "id": 5,
                "nombre": "Dumbbell Flyes",
                "grupoMuscular": "Outer Chest",
                "zonaCorporal": "Chest",
                "grupoMuscularEspecifico": "Pectoralis Major",
                "series": 4,
                "repeticiones": "12-15",
                "descanso": "45s",
                "equipo": "Dumbbells and Bench",
                "dificultad": 3,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561155948676/pecho_2.jpg"
            },
            {
                "id": 6,
                "nombre": "Leg Press",
                "grupoMuscular": "Quadriceps and Glutes",
                "zonaCorporal": "Legs",
                "grupoMuscularEspecifico": "Quadriceps",
                "series": 3,
                "repeticiones": "15-20",
                "descanso": "60s",
                "equipo": "Press Machine",
                "dificultad": 1,
                "imagen": "https://cdn.discordapp.com/attachments/1444030633646100512/1446204561508536320/pierna.jpg"
            }
        ]
    }
    
    # Para idiomas no definidos, usar español como fallback
    if lang not in exercises_db:
        lang = 'es'
    
    return exercises_db[lang]

def get_random_exercises(count, lang='es'):
    """Devuelve una lista aleatoria de ejercicios"""
    exercises = get_exercises(lang)
    if count > len(exercises):
        return exercises
    return random.sample(exercises, count)

# ========== ESTILOS CSS ==========
def apply_styles():
    """Aplica estilos CSS personalizados a la aplicación"""
    st.markdown("""
    <style>
    /* Estilos generales */
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #000000;
    }
    
    /* Logo */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .logo {
        max-width: 200px;
        border-radius: 8px;
    }
    
    /* Tarjetas de ejercicio */
    .exercise-card {
        background-color: #111111;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #222222;
    }
    
    .exercise-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .exercise-image {
        width: 120px;
        height: 120px;
        object-fit: cover;
        border-radius: 8px;
        margin-right: 20px;
        border: 2px solid #333333;
    }
    
    .exercise-title {
        flex: 1;
    }
    
    .muscle-group {
        display: inline-block;
        background-color: #222222;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .difficulty-dots {
        display: flex;
        gap: 5px;
        margin-top: 8px;
    }
    
    .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #333333;
    }
    
    .dot.filled {
        background-color: #4CAF50;
    }
    
    /* Grid de detalles */
    .exercise-details {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 15px;
    }
    
    .detail-item {
        background-color: #222222;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
    }
    
    .detail-label {
        font-size: 12px;
        color: #888888;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    
    .detail-value {
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
    }
    
    /* Botones */
    .stButton > button {
        width: 100%;
        background-color: #222222;
        color: white;
        border: 2px solid #333333;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #333333;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: #222222;
    }
    
    .stSlider > div > div > div > div {
        background-color: #4CAF50;
    }
    
    /* Selector de idiomas */
    .language-selector {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 100;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .exercise-header {
            flex-direction: column;
            text-align: center;
        }
        
        .exercise-image {
            margin-right: 0;
            margin-bottom: 15px;
            width: 100%;
            max-width: 250px;
        }
        
        .exercise-details {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    @media (max-width: 480px) {
        .exercise-details {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ========== PÁGINAS ==========
def show_language_selector():
    """Muestra el selector de idiomas"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🇪🇸 ES", use_container_width=True):
            st.session_state.language = 'es'
            st.rerun()
    
    with col2:
        if st.button("🇨🇦 CA", use_container_width=True):
            st.session_state.language = 'ca'
            st.rerun()
    
    with col3:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    
    with col4:
        if st.button("🇫🇷 FR", use_container_width=True):
            st.session_state.language = 'fr'
            st.rerun()
    
    with col5:
        if st.button("🇩🇪 DE", use_container_width=True):
            st.session_state.language = 'de'
            st.rerun()

def page_form():
    """Página 1: Formulario de datos personales"""
    t = setup_languages()
    
    # Logo
    st.markdown("""
    <div class="logo-container">
        <img src="https://cdn.discordapp.com/attachments/1445471570125520956/1445471701906231416/Algo_Fit.png?ex=6933c3ad&is=6932722d&hm=e7f5258a6b46763716a32dc6ca408fba4409583fce6fae085f300e1f40060b35&" 
             alt="Algo Fit" 
             class="logo">
    </div>
    """, unsafe_allow_html=True)
    
    st.title(t['form_title'])
    st.write(t['form_subtitle'])
    
    # Selector de idiomas
    show_language_selector()
    
    # Formulario
    with st.form("personal_form"):
        st.subheader(t['personal_data'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_completo = st.text_input(t['full_name'], key="nombre")
            genero = st.selectbox(t['gender'], 
                                 [t['select_gender'], t['male'], t['female']], 
                                 key="genero")
            
            # Fecha de nacimiento
            hoy = date.today()
            fecha_min = date(hoy.year - 80, hoy.month, hoy.day)
            fecha_nac = st.date_input(t['birth_date'], 
                                     min_value=fecha_min, 
                                     max_value=hoy, 
                                     value=hoy,
                                     key="fecha_nac")
        
        with col2:
            edad = st.number_input(t['age'], min_value=12, max_value=80, value=25, key="edad")
            altura_cm = st.number_input(t['height'], min_value=100, max_value=270, value=170, key="altura")
            peso_kg = st.number_input(t['weight'], min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="peso")
        
        st.subheader(t['physical_info'])
        
        objetivo = st.selectbox(t['objective'], 
                               [t['select_objective'], t['gain_muscle'], t['lose_weight']], 
                               key="objetivo")
        
        experiencia = st.selectbox(t['experience'], 
                                  [t['select_experience'], t['beginner'], t['intermediate'], t['expert']], 
                                  key="experiencia")
        
        st.info(t['required_note'])
        
        enviar = st.form_submit_button(t['send'])
    
    if enviar:
        errores = []
        
        # Validaciones
        if not nombre_completo.strip():
            errores.append(t['full_name'] + " " + t['required_note'].lower())
        elif not re.match(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$", nombre_completo):
            errores.append("El nombre solo puede contener letras y espacios")
        
        if genero == t['select_gender']:
            errores.append(t['gender'] + " " + t['required_note'].lower())
        
        if objetivo == t['select_objective']:
            errores.append(t['objective'] + " " + t['required_note'].lower())
        
        if experiencia == t['select_experience']:
            errores.append(t['experience'] + " " + t['required_note'].lower())
        
        # Validar edad vs fecha de nacimiento
        if fecha_nac:
            edad_calc = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            if not (edad == edad_calc or edad == edad_calc + 1):
                errores.append(f"La edad ({edad}) no coincide con la fecha de nacimiento (edad calculada: {edad_calc})")
        
        if errores:
            for error in errores:
                st.error(error)
        else:
            # Procesar datos
            gestor = GestorUsuario()
            usuario = gestor.get_usuario(
                nombre_completo,
                edad,
                genero,
                altura_cm,
                peso_kg,
                objetivo,
                experiencia
            )
            
            # Guardar en session_state
            st.session_state.usuario = {
                "Nombre": usuario.Nombre,
                "Apellido": usuario.Apellido,
                "Edad": usuario.Edad,
                "Genero": usuario.Genero,
                "Altura": usuario.Altura,
                "Peso": usuario.Peso,
                "Objetivo": usuario.Objetivo,
                "Nivel": usuario.Nivel
            }
            
            st.success("¡Datos guardados correctamente!")
            st.session_state.page = "main"
            st.rerun()

def page_main():
    """Página 2: Página principal con slider"""
    t = setup_languages()
    
    # Logo
    st.markdown("""
    <div class="logo-container">
        <img src="https://cdn.discordapp.com/attachments/1445471570125520956/1445471701906231416/Algo_Fit.png?ex=6933c3ad&is=6932722d&hm=e7f5258a6b46763716a32dc6ca408fba4409583fce6fae085f300e1f40060b35&" 
             alt="Algo Fit" 
             class="logo">
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de idiomas
    show_language_selector()
    
    # Verificar si hay datos de usuario
    if 'usuario' not in st.session_state:
        st.warning(t['no_data_error'])
        if st.button(t['personal_info']):
            st.session_state.page = "form"
            st.rerun()
        return
    
    # Slider para seleccionar cantidad de ejercicios
    st.subheader(t['select_exercises'])
    
    cantidad = st.slider("", 1, 10, 5, 1, label_visibility="collapsed")
    
    # Botones
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(t['recommend'], use_container_width=True):
            if 1 <= cantidad <= 10:
                st.session_state.exercise_count = cantidad
                st.session_state.page = "exercises"
                st.rerun()
            else:
                st.error(t['invalid_number'])
    
    with col2:
        if st.button(t['personal_info'], use_container_width=True):
            st.session_state.page = "form"
            st.rerun()

def page_exercises():
    """Página 3: Lista de ejercicios recomendados"""
    t = setup_languages()
    
    # Logo
    st.markdown("""
    <div class="logo-container">
        <img src="https://cdn.discordapp.com/attachments/1445471570125520956/1445471701906231416/Algo_Fit.png?ex=6933c3ad&is=6932722d&hm=e7f5258a6b46763716a32dc6ca408fba4409583fce6fae085f300e1f40060b35&" 
             alt="Algo Fit" 
             class="logo">
    </div>
    """, unsafe_allow_html=True)
    
    st.title(t['recommended_exercises'])
    
    # Selector de idiomas
    show_language_selector()
    
    # Verificar si hay datos necesarios
    if 'exercise_count' not in st.session_state:
        st.warning(t['no_data_error'])
        if st.button(t['back_to_adjust']):
            st.session_state.page = "main"
            st.rerun()
        return
    
    cantidad = st.session_state.exercise_count
    
    # Mostrar mensaje
    if cantidad > 6:  # Solo tenemos 6 ejercicios
        st.info(t['all_exercises'].format(count=6))
        cantidad = 6
    else:
        st.success(t['showing'].format(count=cantidad))
    
    # Obtener ejercicios aleatorios
    exercises = get_random_exercises(cantidad, st.session_state.language)
    
    # Mostrar cada ejercicio
    for exercise in exercises:
        with st.container():
            st.markdown(f"""
            <div class="exercise-card">
                <div class="exercise-header">
                    <img src="{exercise['imagen']}" class="exercise-image">
                    <div class="exercise-title">
                        <h3>{exercise['nombre']}</h3>
                        <div class="muscle-group">{exercise['grupoMuscular']}</div>
                        <div class="difficulty-dots">
                            {"".join(['<div class="dot filled"></div>' if i < exercise['dificultad'] else '<div class="dot"></div>' for i in range(5)])}
                        </div>
                    </div>
                </div>
                <div class="exercise-details">
                    <div class="detail-item">
                        <div class="detail-label">{t['body_zone']}</div>
                        <div class="detail-value">{exercise['zonaCorporal']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['muscle_group']}</div>
                        <div class="detail-value">{exercise['grupoMuscularEspecifico']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['series']}</div>
                        <div class="detail-value">{exercise['series']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['repetitions']}</div>
                        <div class="detail-value">{exercise['repeticiones']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['rest']}</div>
                        <div class="detail-value">{exercise['descanso']}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">{t['equipment']}</div>
                        <div class="detail-value">{exercise['equipo']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Botón para volver
    if st.button(t['back_to_adjust']):
        st.session_state.page = "main"
        st.rerun()

# ========== APLICACIÓN PRINCIPAL ==========
def main():
    """Función principal de la aplicación"""
    
    # Inicializar session_state
    if 'page' not in st.session_state:
        st.session_state.page = "form"
    
    if 'language' not in st.session_state:
        st.session_state.language = 'es'
    
    # Aplicar estilos
    apply_styles()
    
    # Mostrar página según estado
    if st.session_state.page == "form":
        page_form()
    elif st.session_state.page == "main":
        page_main()
    elif st.session_state.page == "exercises":
        page_exercises()

if __name__ == "__main__":
    main()
