import streamlit as st
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from typing import Dict, List
from utilities.utils import (setup_logger, load_categories)
from omegaconf import OmegaConf

config = OmegaConf.load('./utilities/config.yml')
Logger = setup_logger(logger_file="app_logs")

MODEL_PATH = config.general.MODEL_PATH
FILE_PATH = config.general.FILE_PATH

categories = load_categories(FILE_PATH)


# Load the trained model
@st.cache_data
def load_model(model_path: str) -> pickle:
    """
    Loads a trained model from a specified file path.

    Args:
        model_path (str): The file path to the saved model.

    Returns:
        pickle: The loaded model object.
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

label_encoders = {key: LabelEncoder().fit(value) for key, value in categories.items()}


def encode_categorical_features(features: Dict[str, str]) -> List[int]:
    """
    Encodes categorical features into numerical values using LabelEncoder.

    Args:
        features (Dict[str, str]): A dictionary where the keys are feature names and values are categorical feature values.

    Returns:
        List[int]: A list of encoded numerical values for the categorical features.
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
        numerical_features (Dict[str, float]): A dictionary where the keys are feature names and values are numerical feature values.

    Returns:
        List[float]: A list of scaled numerical values for the numerical features.
    """

    scaler = StandardScaler()
    
    numerical_data = list(numerical_features.values())
    numerical_data_2d = [numerical_data]  
    scaled_data = scaler.fit_transform(numerical_data_2d)  
    
    return scaled_data[0].tolist()  


def predict_result(model, features) -> str:
    """
    Predicts the result based on the provided features using the trained model.

    Args:
        model: The trained model object.
        features: The list of features to be passed to the model for prediction.

    Returns:
        str: The predicted result, either "Empowered" if >= 0.75 or "Not Empowered".
    """

    prediction = model.predict([features])[0]
    return "Empowered" if prediction >= 0.75 else "Not Empowered"


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

        submit_button = st.form_submit_button("Run Prediction")

    if submit_button:
        try:
            if any(
                value is None for value in (business_ownership, employment_rates, women_in_leadership, tariff_rates)
            ) or any(value == "" for value in form_inputs.values()):
                raise ValueError("Please ensure all fields are filled.")
            else: 

                features = {
                    "Business Ownership": business_ownership,
                    "Employment Rates": employment_rates,
                    "Women in Leadership": women_in_leadership,
                    "Tariff Rates": tariff_rates,
                }
                features.update(form_inputs)

                numerical_features = {key: value for key, value in features.items() if isinstance(value, (int, float))}
                categorical_features = {key: value for key, value in features.items() if isinstance(value, str)}
                encoded_categorical_features = encode_categorical_features(categorical_features)
                scaled_numerical_features = scale_numerical_features(numerical_features)

                final_features = scaled_numerical_features + encoded_categorical_features

                model = load_model(MODEL_PATH)
                result = predict_result(model, final_features)

                st.success(f"Prediction: Women are {result} in this Organization.")
        except ValueError as e:
            st.error(f"Input Error: {e}")


if __name__ == "__main__":
    main()
