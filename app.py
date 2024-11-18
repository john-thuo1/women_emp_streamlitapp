import streamlit as st
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from typing import Dict, List
from logger import setup_logger

Logger = setup_logger(logger_file="app_logs")

MODEL_PATH = st.secrets["general"].get("MODEL_PATH")

# Load the trained model
@st.cache_data
def load_model(model_path: str) -> pickle:
    """
    Load a machine learning model from a pickle file.
    
    Args:
        model_path (str): The path to the model pickle file.
        
    Returns:
        model: The loaded machine learning model.
    """
    try:
        Logger.info(f"Attempting to load the model from: {model_path}")
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        Logger.info("Model loaded successfully.")
        return model
    except FileNotFoundError as e:
        Logger.error(f"File not found: {model_path}")
        raise e

# Categories for Categorical Features
categories = {
    "Trade Flows": ["Increasing", "Stable", "Decreasing"],
    "Access to Finances": ["High", "Moderate", "Low"],
    "Farming Type": ["Communal", "Single-household", "Mixed"],
    "Education and Skills": ["Advanced", "Basic", "Intermediate"],
    "Changes in Women's Income": ["Rising", "Falling", "Stable"],
    "Clear Decision Points": ["Yes", "No", "Partial"],
    "Policy Changes": ["Significant", "Minor", "None"],
    "Complex Interactions": ["High", "Medium", "Low"],
    "Feedback Loops": ["Present", "Absent", "Weak"],
    "Intra-African Mobility": ["Increasing", "Decreasing", "Stable"],
    "Legal Frameworks": ["Supportive", "Neutral", "Restrictive"],
    "Social Norms and Gender Roles": ["Progressive", "Traditional", "Mixed"],
    "Access to Childcare": ["Good", "Limited", "None"],
    "Impact on Women": ["Positive", "Negative", "Neutral"],
    "Value Chain Participation": ["High", "Moderate", "Low"],
    "Health and Well-being": ["Improved", "Declining", "Stable"]
}

label_encoders = {key: LabelEncoder().fit(value) for key, value in categories.items()}


def encode_categorical_features(features: Dict[str, str]) -> List[int]:
    """
    Encodes categorical features using LabelEncoder.
    
    Args:
        features (Dict[str, str]): A dictionary containing feature names and their categorical values.
        
    Returns:
        List[int]: A list of encoded values for the categorical features.
    """
    encoded_features = []
    for feature_name, feature_value in features.items():
        if feature_name in label_encoders:
            encoded_value = label_encoders[feature_name].transform([feature_value])[0]
            encoded_features.append(encoded_value)
        else:
            encoded_features.append(feature_value)
    return encoded_features


def scale_numerical_features(numerical_features: Dict[str, float]) -> List[float]:
    """
    Scales numerical features using StandardScaler.
    
    Args:
        numerical_features (Dict[str, float]): A dictionary containing feature names and their numerical values.
        
    Returns:
        List[float]: A list of scaled numerical features.
    """
    scaler = StandardScaler()
    
    numerical_data = list(numerical_features.values())
    numerical_data_2d = [numerical_data]  
    scaled_data = scaler.fit_transform(numerical_data_2d)  
    
    return scaled_data[0].tolist()  


def main():
    st.title("Women Empowerment Predictor")
    st.write("Enter the details to predict women empowerment status.")
    
    with st.form("input_form"):
        business_ownership = st.number_input(label="Business Ownership", min_value=0, value=None,
                                            placeholder="Enter the total number of businesses owned in the target group.")
        employment_rates = st.number_input(label="Employment Rates (%)", min_value=0, max_value=100, value=None,
                                           placeholder="Specify the employment rate as a percentage (0-100%).")
        women_in_leadership = st.number_input(label="Women in Leadership", min_value=0, max_value=100, value=None,
                                             placeholder="Provide the count of women in leadership positions.")
        tariff_rates = st.number_input(label="Tariff Rates", min_value=0, max_value=100, value=None,
                                       placeholder="Input the tariff rates as a percentage (0-100%).")

        form_inputs = {}
        for category, options in categories.items():
            form_inputs[category] = st.selectbox(label=category, options=options, index=None,
                                                 placeholder=f"Select {category.replace('_', ' ')}")

        # Submit button for form
        submit_button = st.form_submit_button("Run Prediction")

    if submit_button:
        features = {
            "Business Ownership": business_ownership,
            "Employment Rates": employment_rates,
            "Women in Leadership": women_in_leadership,
            "Tariff Rates": tariff_rates,
        }
        features.update(form_inputs)

        numerical_features = {key: value for key, value in features.items() if isinstance(value, (int, float))}
        categorical_features = {key: value for key, value in features.items() if isinstance(value, str)}

        # Encode categorical features
        encoded_categorical_features = encode_categorical_features(categorical_features)

        # Scale numerical features
        scaled_numerical_features = scale_numerical_features(numerical_features)

        final_features = scaled_numerical_features + encoded_categorical_features

        model = load_model(MODEL_PATH)
        prediction = model.predict([final_features])[0]
        result = "Empowered" if prediction == 1 else "Not Empowered"
        st.write(f"Prediction: Women are {result}.")

if __name__ == "__main__":
    main()
