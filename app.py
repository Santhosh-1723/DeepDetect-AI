from flask import Flask, render_template, request
import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)

# Load trained CNN model
model = tf.keras.models.load_model("model/deepfake_model.h5")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    # Convert uploaded image to OpenCV format
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    image = cv2.resize(image, (128,128))
    image = image / 255.0
    image = np.reshape(image, (1,128,128,3))

    prediction = model.predict(image)[0][0]

    confidence = round(float(prediction) * 100,2)

    if prediction > 0.5:
        result = "⚠️ Deepfake Detected"
    else:
        result = "✅ Authentic Image"

    return render_template(
        "index.html",
        prediction=result,
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(debug=True)