# Network Intrusion and Attack Detection

**Group Members:** Jalen Pope, Kelly Rudnick, Paul Scalice, Dathan Knott, Nicholas DiTommaso

This repository contains the codebase and documentation for our CYSE 635 AI Security and Privacy final project. It was developed by developed by Group 4 also known as The Vigilant Core. The focus of this project is on AI-powered network intrusion detection for IoT environments using machine learning techniques.


**Project Overview**

The rapid expansion of IoT devices introduces significant security risks. Our project aims to address these risks by developing a machine learning-based system to classify IoT network traffic as malicious or benign.

Our solution leverages Random Forest and Support Vector Machine (SVM) algorithms to analyze network traffic logs by enhancing detection rates and providing actionable insights into potential threats.


**Technologies and Tools**

Programming Language: Python

Machine Learning Libraries: Scikit-learn, Pandas, NumPy

Visualization Tools: Matplotlib, Seaborn

Environment: Google Colab


**Models Used:**

Random Forest
Support Vector Machines (SVM)
K-Nearest Neighbors (KNN)


**Datasets**

Dataset 1: Initial dataset of 40,000 records with 25 features.

Dataset 2: Cisco Netflow data utilized to refine feature selection and enhance performance.


**Data Preprocessing Steps** 

Data Cleaning: Removed irrelevant fields and filled missing values.

Feature Transformation: Converted categorical data to numerical values.

Stratified Sampling: Balanced training and testing datasets.

Dimensionality Reduction: Utilized correlation matrices for feature selection.


**Project Results**

Initial Dataset: Accuracy is limited to 50% due to feature selection and dataset quality issues.

Refined Dataset: Achieved over 90% accuracy, precision, recall, and F1-scores using improved data and algorithms.


**Challenges**

Dataset limitations and imbalances.

Computational constraints during training and hyperparameter optimization.

Handling high-dimensional network traffic data.


**Installation and Usage**

Prerequisites
Python 3.x


**Required Libraries:** 

pandas, numpy, matplotlib, seaborn, scikit-learn
