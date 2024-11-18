# Women Empowerment Predictor

This application uses a Logistic Regression Model to predict women's empowerment status based on various socio-economic factors. The model predicts whether a target group of women is "Empowered" or "Not Empowered" based on inputs like business ownership, employment rates, women in leadership positions, tariff rates, and other socio-economic categories.

## Features
- Input form to collect information on socio-economic factors.
- Automatic encoding of categorical features (e.g., "Trade Flows", "Access to Finances").
- Scaling of numerical features (e.g., business ownership, employment rates).
- Machine learning model prediction using a pre-trained model loaded from a pickle file.


## Local Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/women-empowerment-predictor.git
   cd women-empowerment-predictor
2. Install Application Dependencies in your Virtual Env
    ```bash
    pip install -r requirements.txt
    
3. Run Application
   ```bash
   streamlit run app.py
   
   
