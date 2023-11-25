import streamlit as st
import mysql.connector
import pickle
from passlib.hash import pbkdf2_sha256
from streamlit_option_menu import option_menu
# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shared"
)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL
    )
""")
conn.commit()

# Streamlit App
def main():
    st.title("Authentication App")

    menu = ["Login", "Register", "Update Password", "Forgot Password"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login()
    elif choice == "Register":
        register()
    elif choice == "Update Password":
        update_password()
    elif choice == "Forgot Password":
        forgot_password()

# Function to hash the password
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to verify the hashed password
def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

# Function to register a new user
def register():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    repeat_password = st.text_input("Repeat Password", type="password")

    if st.button("Register"):
        if password == repeat_password:
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            st.success("Registration successful. Please login.")
        else:
            st.error("Passwords do not match. Please try again.")

# Function to authenticate user
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and verify_password(password, user[2]):
            st.success(f"Logged in as {username}")

            # Set session state variable for successful login
            st.session_state.is_logged_in = True

        else:
            st.error("Invalid username or password")

# Function to update password
def update_password():
    st.subheader("Update Password")
    username = st.text_input("Username")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")

    if st.button("Update Password"):
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and verify_password(current_password, user[2]):
            hashed_new_password = hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash=%s WHERE username=%s", (hashed_new_password, username))
            conn.commit()
            st.success("Password updated successfully")
        else:
            st.error("Invalid username or password")

# Function for password recovery (simplified, for demonstration purposes)
def forgot_password():
    st.subheader("Forgot Password")
    username = st.text_input("Username")

    if st.button("Recover Password"):
        # In a real-world scenario, you might want to implement a more secure password recovery mechanism
        st.warning("Password recovery email sent (not implemented in this example).")

# Home page
# Home page
# Home page
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

def home():
    diabetes_model = pickle.load(open("model/diabetes_model.sav", "rb"))
    heart_disease_model = pickle.load(open("model/heart_disease_model.sav", "rb"))
    parkinsons_model = pickle.load(open("model/parkinsons_model.sav", "rb"))

    with st.sidebar:
        selected = option_menu("Multiple Disease Prediction System", ["Diabetes Prediction", "Heart Disease Prediction", "Parkinsons Prediction"],
                               icons=["activity", "heart", "person"], default_index=0)

    if selected == "Diabetes Prediction":
        st.title("Diabetes Prediction using ML")
        col1, col2 = st.columns(2)
        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')
        with col2:
            Glucose = st.text_input('Glucose Level')
        with col1:
            BloodPressure = st.text_input('Blood Pressure value')
        with col2:
            SkinThickness = st.text_input('Skin Thickness value')
        with col1:
            Insulin = st.text_input('Insulin Level')
        with col2:
            BMI = st.text_input('BMI value')
        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
        with col2:
            Age = st.text_input('Age of the Person')
        diab_diagnosis = ''
        if st.button('Diabetes Test Result'):
            diab_prediction = diabetes_model.predict(
                [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            if diab_prediction[0] == 1:
                diab_diagnosis = 'The person is diabetic'
            else:
                diab_diagnosis = 'The person is not diabetic'
        st.success(diab_diagnosis)

    if selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.text_input('Age')
        with col2:
            sex = st.text_input('Sex')
        with col3:
            cp = st.text_input('Chest Pain types')
        with col1:
            trestbps = st.text_input('Resting Blood Pressure')
        with col2:
            chol = st.text_input('Serum Cholesterol in mg/dl')
        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')
        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')
        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')
        with col3:
            exang = st.text_input('Exercise Induced Angina')
        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')
        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')
        with col3:
            ca = st.text_input('Major vessels colored by fluoroscopy')
        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')
        heart_diagnosis = ''
        if st.button('Heart Disease Test Result'):
            heart_prediction = heart_disease_model.predict(
                [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
            if heart_prediction[0] == 1:
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'
        st.success(heart_diagnosis)

    if selected == "Parkinsons Prediction":
        st.title("Parkinson's Disease Prediction using ML")
        col1, col2, col3 = st.columns(3)
        with col1:
            fo = st.text_input('MDVP:Fo(Hz)')
        with col2:
            fhi = st.text_input('MDVP:Fhi(Hz)')
        with col3:
            flo = st.text_input('MDVP:Flo(Hz)')
        with col1:
            Jitter_percent = st.text_input('MDVP:Jitter(%)')
        with col2:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
        with col3:
            RAP = st.text_input('MDVP:RAP')
        with col1:
            PPQ = st.text_input('MDVP:PPQ')
        with col2:
            DDP = st.text_input('Jitter:DDP')
        with col3:
            Shimmer = st.text_input('MDVP:Shimmer')
        with col1:
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
        with col2:
            APQ3 = st.text_input('Shimmer:APQ3')
        with col3:
            APQ5 = st.text_input('Shimmer:APQ5')
        with col1:
            APQ = st.text_input('MDVP:APQ')
        with col2:
            DDA = st.text_input('Shimmer:DDA')
        with col3:
            NHR = st.text_input('NHR')
        with col1:
            HNR = st.text_input('HNR')
        with col2:
            RPDE = st.text_input('RPDE')
        with col3:
            DFA = st.text_input('DFA')
        with col1:
            spread1 = st.text_input('spread1')
        with col2:
            spread2 = st.text_input('spread2')
        with col3:
            D2 = st.text_input('D2')
        with col1:
            PPE = st.text_input('PPE')
        parkinsons_diagnosis = ''
        if st.button("Parkinson's Test Result"):
            parkinsons_prediction = parkinsons_model.predict(
                [[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR,
                  RPDE, DFA, spread1, spread2, D2, PPE]])
            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
        st.success(parkinsons_diagnosis)

# Run the application
# Check if the user is logged in before rendering the home page
if st.session_state.get("is_logged_in", False):
    home()
else:
    main()
