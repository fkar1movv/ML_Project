import numpy as np
from flask import Flask, request, jsonify
import pandas as pd

# Import the Isolation Forest model and feature names
from sklearn.ensemble import IsolationForest

# Replace 'data.csv' with the path to your dataset
data = pd.read_csv('dataset.csv')
data.drop(columns=['Unnamed: 0', 'timestamp'], inplace=True)

# Create and fit the Isolation Forest model
model = IsolationForest(contamination='auto', random_state=42)
model.fit(data)

# Create a Flask app
app = Flask(__name__)

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request
        data_json = request.get_json()
        input_data = np.array(data_json['data'])

        # Ensure the input data has the same number of features as the model expects
        assert input_data.shape[1] == len(data.columns)

        # Perform prediction using the model
        predictions = model.predict(input_data)

        # Convert predictions to a list and send the response
        results = []
        for idx, pred in enumerate(predictions):
            if pred == -1:
                result = 'Anomaly'
            else:
                result = 'Normal'
            results.append({'data_point': input_data[idx].tolist(), 'prediction': result})

        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Start the server
    app.run(host='localhost', port=8000)