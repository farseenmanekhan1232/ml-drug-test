# Compound Prediction Flask Application

This Flask application allows users to upload `.mzML` files and receive predictions for compounds based on molecular mass extracted from the file. The application utilizes a pre-trained model for making predictions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The project is containerized using Docker, simplifying the setup and deployment process.

### Prerequisites

Ensure you have Docker installed on your machine. Docker will handle the installation of Python and all the necessary dependencies for you.

- [Get Docker](https://docs.docker.com/get-docker/)

### Installing

1. **Clone the repository**

   Clone this repository to your local machine to get started.

   ```bash
   git clone https://github.com/farseenmanekhan1232/ml-drug-test.git
   cd ml-drug-test
   ```

````

2. **Build the Docker image**

   Navigate to the root of the project directory where the `Dockerfile` is located and build the Docker image using the following command:

   ```bash
   docker build -t flask_compound_prediction .
   ```

   This command builds a Docker image named `flask_compound_prediction` based on the instructions in your `Dockerfile`.

3. **Run the Docker container**

   After the image is built, you can run the application inside a Docker container using:

   ```bash
   docker run -p 5000:5000 flask_compound_prediction
   ```

   This command runs the `flask_compound_prediction` image as a container and maps port 5000 of the container to port 5000 on your host, allowing you to access the Flask application by visiting `http://localhost:5000` in your web browser.

### Using the Application

To use the application, follow these steps:

1. Open your web browser and navigate to `http://localhost:5000`.
2. Use the web interface to upload a `.mzML` file from your local system.
3. Submit the file, and the application will display the predicted compound based on the molecular mass extracted from the `.mzML` file.

## Built With

- [Flask](http://flask.pocoo.org/) - The web framework used
- [Docker](https://www.docker.com/) - Containerization
- [Scikit-Learn](https://scikit-learn.org/stable/) - Machine Learning library for Python
- [Joblib](https://joblib.readthedocs.io/en/latest/) - Efficiently loading the pre-trained model
````
