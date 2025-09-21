# Obesity Level Prediction System

This repository contains an end-to-end machine learning project designed to classify an individual's obesity level based on lifestyle and daily habits. The system is deployed as a full-stack application with a FastAPI backend serving the model and a Streamlit frontend for user interaction.

## Project Overview

To facilitate proactive and personalized healthcare, this project was developed for a health clinic focused on obesity prevention. The system predicts an individual's obesity risk category, allowing the clinic to offer early education and intervention to those at high risk. By leveraging data-driven insights, health campaigns can be more effectively targeted.

## Application Architecture

The project follows a modern, decoupled architecture:

1.  **Machine Learning Model**: A classification model was trained using a data pipeline that includes all necessary preprocessing steps. After comparing multiple algorithms, the best-performing model was serialized using `pickle` for deployment.
2.  **Backend API (FastAPI)**: A robust, high-performance API was built using FastAPI to serve the machine learning model. It exposes a single endpoint that accepts user data, processes it, and returns the predicted obesity level.
3.  **Frontend Application (Streamlit)**: An interactive and user-friendly web interface was created with Streamlit. The frontend provides a form for users to input their data, which is then sent to the FastAPI backend. The prediction returned by the API is then clearly displayed to the user.
