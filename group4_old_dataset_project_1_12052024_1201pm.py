# -*- coding: utf-8 -*-
"""Group4 Old Dataset Project 1 12052024_1201PM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-DA5qdISiSfM3q6k9KOGnpzjgs3D7aKG

1.1. Importing the basic libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# Load data processing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
# %matplotlib inline

"""1.2. Importing machine learning libraries"""

# Load machine learning libraries
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Import the necessary module for 3D plotting

"""Dataset = https://www.kaggle.com/datasets/teamincribo/cyber-security-attacks?resource=download"""

import os

curr_dir = os.getcwd()
print(curr_dir)

"""###1.3 Upload Dataset"""

from google.colab import files
uploaded = files.upload()

"""###1.4 Verify File(s)"""

ls -al /content/

"""###1.5 Verify Loaded Dataset Information"""

df=pd.read_csv("/content/cybersecurity_attacks.csv") # 2-dimensional data structure (rows X columns) created from reading .csv and assigned name df
df.head(5) #print first 5 rows with header

#Verify Fields and Types
df.info() #This is a method that you apply to a DataFrame to get a concise summary of its structure and content.

#Verify Empty (null) Fields
df.isnull().sum() #This method is applied to the DataFrame. It checks each cell in the DataFrame and returns a new DataFrame of the same shape, but with Boolean values (True or False). Missing values

"""##1.6 Data Preprocessing

###1.61 Data Cleaning
"""

# Fill the missing null values with relevant data
df['Alerts/Warnings'].fillna('No Alert', inplace=True)
df['Firewall Logs'].fillna('No Log', inplace=True)
df['Proxy Information'].fillna('No Proxy Inforation', inplace=True)
df['Geo-location Data'].fillna('No Geolocation Data', inplace=True)
df['User Information'].fillna('No User Information', inplace=True)
df['Malware Indicators'].fillna('No Malware Indicator', inplace=True)
df['IDS/IPS Alerts'].fillna('No IDS/IPS Alert', inplace=True)

#Verify Empty (null) Fields
df.isnull().sum() #This method is applied to the DataFrame. It checks each cell in the DataFrame and returns a new DataFrame of the same shape, but with Boolean values (True or False). Missing values

# prompt: count the number of unique values in each column

for col in df.columns:
  print(f"Column '{col}': {df[col].nunique()} unique values")

Protocol_unique_values = df['Protocol'].unique()
count_Protocol_unique_values = len(Protocol_unique_values)
print("Number of unique Protocol values:", count_Protocol_unique_values)

Packet_Length_unique_values = df['Packet Length'].unique()
count_Packet_Length_unique_values = len(Packet_Length_unique_values)
print("Number of unique Packet Length values:", count_Packet_Length_unique_values)

Traffic_Type_unique_values = df['Traffic Type'].unique()
count_Traffic_Type_unique_values = len(Traffic_Type_unique_values)
print("Number of unique Traffic Type values:", count_Traffic_Type_unique_values)

Alerts_Warnings_unique_values = df['Alerts/Warnings'].unique()
count_Alerts_Warnings_unique_values = len(Alerts_Warnings_unique_values)
print("Number of unique Alerts/Warnings values:", count_Alerts_Warnings_unique_values)

Packet_Type_unique_values = df['Packet Type'].unique()
count_Packet_Type_unique_values = len(Packet_Type_unique_values)
print("Number of unique Packet Type values:", count_Packet_Type_unique_values)

Attack_Type_unique_values = df['Attack Type'].unique()
count_Attack_Type_unique_values = len(Attack_Type_unique_values)
print("Number of unique Attack Type values:", count_Attack_Type_unique_values)

Attack_Signature_unique_values = df['Attack Signature'].unique()
count_Attack_Signature_unique_values = len(Attack_Signature_unique_values)
print("Number of unique Attack_Signature values:", count_Attack_Signature_unique_values)

Severity_Level_unique_values = df['Severity Level'].unique()
count_Severity_Level_unique_values = len(Severity_Level_unique_values)
print("Number of unique Severity Level values:", count_Severity_Level_unique_values)

Severity_Level_unique_values = df['Severity Level'].unique()
count_Severity_Level_unique_values = len(Severity_Level_unique_values)
print("Number of unique Severity Level values:", count_Severity_Level_unique_values)

#remove unneeded labels #new dataset named feature_df
#df.drop(['Timestamp', 'Payload Data', 'Source Port', 'Destination Port', 'IDS/IPS Alerts', 'Source IP Address','Destination IP Address','User Information', 'Device Information','Geo-location Data', 'Firewall Logs', 'Proxy Information','Log Source'], axis=1, inplace=True)
#df.drop(['Timestamp','Source IP Address', 'Destination IP Address', 'Destination IP Address', 'Source Port','Destination Port', 'Packet Length', 'Payload Data', 'Attack Signature','User Information','Device Information','Network Segment','Geo-location Data','Proxy Information','Firewall Logs','IDS/IPS Alerts','Log Source','Malware Indicators','Anomaly Scores', 'Action Taken'], axis=1, inplace=True)
#feature_df=df.drop(['Timestamp','Source IP Address', 'Destination IP Address', 'Destination IP Address', 'Source Port','Destination Port', 'Packet Length', 'Payload Data', 'Attack Signature','User Information','Device Information','Network Segment','Geo-location Data','Proxy Information','Firewall Logs','IDS/IPS Alerts','Log Source','Malware Indicators','Anomaly Scores', 'Action Taken'], axis=1, inplace=False) #inplace=True changed to False so the dataframe is returned
#df.drop(['Timestamp','Source IP Address', 'Destination IP Address', 'Destination IP Address', 'Packet Length', 'Payload Data', 'Attack Signature','User Information','Device Information','Network Segment','Geo-location Data','Proxy Information','Firewall Logs','IDS/IPS Alerts','Log Source','Malware Indicators','Anomaly Scores', 'Action Taken'], axis=1, inplace=True)
feature_df=df.drop(['Timestamp','Source IP Address', 'Destination IP Address', 'Destination IP Address', 'Source Port','Destination Port', 'Payload Data','User Information','Device Information','Network Segment','Geo-location Data','Proxy Information','Firewall Logs','IDS/IPS Alerts','Log Source','Malware Indicators','Anomaly Scores', 'Action Taken'], axis=1, inplace=False) #inplace=True changed to False so the dataframe is returned

feature_df.head(10) #print first 5 rows with header

# prompt: one hot coding Severity Level to numbers

# Create a mapping for Protocol to numerical values
protocol_mapping = {'ICMP': 0, 'UDP': 1, 'TCP': 2}

# Create a mapping for Packet Type to numerical values
packet_type_mapping = {'Data': 0, 'Control': 1}

# Create a mapping for Traffic Type to numerical values
traffic_type_mapping = {'HTTP': 0, 'DNS': 1, 'FTP': 2}

# Create a mapping for Alerts/Warnings to numerical values
alerts_warnings_mapping = {'No Alert': 0, 'Alert Triggered': 1}

# Create a mapping for Attack Type to numerical values
attack_type_mapping = {'Malware': 0, 'DDoS': 1, 'Intrusion': 2}

# Create a mapping for Attack Signature to numerical values
attack_signature_mapping = {'Known Pattern A': 0, 'Known Pattern B': 1}

# Create a mapping for Severity Levels to numerical values
severity_level_mapping = {'Low': 0, 'Medium': 1, 'High': 2}

# Apply one-hot encoding to the 'Protocol' column
feature_df['protocol_type'] = df['Protocol'].map(protocol_mapping)

# Apply one-hot encoding to the 'Packet Type' column
feature_df['packet_type'] = df['Packet Type'].map(packet_type_mapping)

# Apply one-hot encoding to the 'Traffic Type' column
feature_df['traffic_type'] = df['Traffic Type'].map(traffic_type_mapping)

# Apply one-hot encoding to the 'Alerts/Warnings' column
feature_df['alerts_warnings'] = df['Alerts/Warnings'].map(alerts_warnings_mapping)

# Apply one-hot encoding to the 'Attack Type' column
feature_df['attack_type'] = df['Attack Type'].map(attack_type_mapping)

attack_signature_mapping = {'Known Pattern A': 0, 'Known Pattern B': 1}
# Apply one-hot encoding to the 'Attack Signature' column
feature_df['attack_signature'] = df['Attack Signature'].map(attack_signature_mapping)

# Apply one-hot encoding to the 'Severity Level' column
feature_df['severity_level'] = df['Severity Level'].map(severity_level_mapping)


# Display the first few rows of the DataFrame to verify the changes
print(feature_df.head(10))

#Verify change from object to interger
feature_df.head(5) #print first 5 rows with header

"""##Exploratory Data Analysis (EDA)"""

# Drop non-numerical columns #create new data frame called num_df
num_df = feature_df.select_dtypes(include=np.number)
print(num_df.head())

#compare severity level and traffic type
# Create an Axes object
fig, ax = plt.subplots() #This will create a figure and an axes object which is assigned to ax.

sns.countplot(x='alerts_warnings', hue='traffic_type', data=num_df, ax=ax) #Pass ax to countplot

# Get the current tick locations and labels
x_ticks = ax.get_xticks()
x_labels = [list(alerts_warnings_mapping.keys())[list(alerts_warnings_mapping.values()).index(tick)] for tick in x_ticks]
# Set the x-tick labels to the original categorical values
ax.set_xticklabels(x_labels)

# Get the legend handles and labels
handles, labels = ax.get_legend_handles_labels()
# Replace the legend labels with the original categorical values
new_labels = [list(traffic_type_mapping.keys())[list(traffic_type_mapping.values()).index(int(label))] for label in labels]
ax.legend(handles, new_labels, title='Traffic Type')

plt.show()

#compare severity level and traffic type
# Create an Axes object
fig, ax = plt.subplots() #This will create a figure and an axes object which is assigned to ax.

sns.countplot(x='severity_level', hue='traffic_type', data=num_df, ax=ax) #Pass ax to countplot

# Get the current tick locations and labels
x_ticks = ax.get_xticks()
x_labels = [list(severity_level_mapping.keys())[list(severity_level_mapping.values()).index(tick)] for tick in x_ticks]
# Set the x-tick labels to the original categorical values
ax.set_xticklabels(x_labels)

# Get the legend handles and labels
handles, labels = ax.get_legend_handles_labels()
# Replace the legend labels with the original categorical values
new_labels = [list(traffic_type_mapping.keys())[list(traffic_type_mapping.values()).index(int(label))] for label in labels]
ax.legend(handles, new_labels, title='Traffic Type')

plt.show()

#compare severity level and protocol type
# Create an Axes object
fig, ax = plt.subplots() #This will create a figure and an axes object which is assigned to ax.

sns.countplot(x='severity_level', hue='protocol_type', data=num_df, ax=ax) #Pass ax to countplot

# Get the current tick locations and labels
x_ticks = ax.get_xticks()
x_labels = [list(severity_level_mapping.keys())[list(severity_level_mapping.values()).index(tick)] for tick in x_ticks]
# Set the x-tick labels to the original categorical values
ax.set_xticklabels(x_labels)

# Get the legend handles and labels
handles, labels = ax.get_legend_handles_labels()
# Replace the legend labels with the original categorical values
new_labels = [list(protocol_mapping.keys())[list(protocol_mapping.values()).index(int(label))] for label in labels]
ax.legend(handles, new_labels, title='Protocol Type')

plt.show()

#compare alerts warnings and protocol type
# Create an Axes object
fig, ax = plt.subplots() #This will create a figure and an axes object which is assigned to ax.

sns.countplot(x='alerts_warnings', hue='protocol_type', data=num_df, ax=ax) #Pass ax to countplot

# Get the current tick locations and labels
x_ticks = ax.get_xticks()
x_labels = [list(alerts_warnings_mapping.keys())[list(alerts_warnings_mapping.values()).index(tick)] for tick in x_ticks]
# Set the x-tick labels to the original categorical values
ax.set_xticklabels(x_labels)

# Get the legend handles and labels
handles, labels = ax.get_legend_handles_labels()
# Replace the legend labels with the original categorical values
new_labels = [list(protocol_mapping.keys())[list(protocol_mapping.values()).index(int(label))] for label in labels]
ax.legend(handles, new_labels, title='Protocol Type')

plt.show()

# prompt: Correlation matrix heatmap for one hot

# Assuming 'df' is your DataFrame with one-hot encoded columns

# Select only the numerical columns for the correlation matrix
numerical_cols = num_df.select_dtypes(include=np.number)

# Calculate the correlation matrix
correlation_matrix = numerical_cols.corr()

# Create the heatmap
plt.figure(figsize=(12, 10))  # Adjust figure size as needed
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix Heatmap')
plt.show()

#Histogram
print("Histogram Analysis")
num_df.hist(bins=50, figsize=(10,7))
plt.show()
#

# print num_df columns

num_df.columns

# Define features (X) and target (y)
num1_df = num_df.drop('alerts_warnings', axis=1)  # Features #This includes non-numerical columns
#X = df[['protocol_type', 'packet_type', 'traffic_type', 'alerts_warnings', 'attack_type']] # Select only numerical columns
#X = num_df[['protocol_type', 'traffic_type', 'alerts_warnings',]] # Select only numerical columns
X = num1_df[['protocol_type', 'packet_type', 'traffic_type', 'severity_level', 'attack_type', 'Packet Length', 'attack_signature' ]] # Select only numerical columns
y = num_df['alerts_warnings']  # Target variable

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% training and 20% test

# Scale the numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Initialize and train a classifier (e.g., RandomForestClassifier)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_scaled, y_train)


# Make predictions on the test set
y_pred = clf.predict(X_test_scaled)


# Evaluate the model
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# prompt: neural network

# Initialize and train an MLPClassifier (Neural Network)
mlp = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42) # Adjust hidden_layer_sizes as needed
mlp.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred_mlp = mlp.predict(X_test_scaled)

# Evaluate the model
print("MLP Classifier Evaluation:")
print(classification_report(y_test, y_pred_mlp))
print(confusion_matrix(y_test, y_pred_mlp))

#Linear regression

from sklearn.linear_model import LinearRegression

# Assuming X and y are defined as in the provided code
# ... (your existing code for data loading and preprocessing) ...

# Initialize and train a Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred_lr = lr_model.predict(X_test_scaled)

# Evaluate the model (you'll need appropriate metrics for regression)
# Example using Mean Squared Error (MSE)
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred_lr)
print(f"Mean Squared Error: {mse}")

# Example using R-squared
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred_lr)
print(f"R-squared: {r2}")

# plot linear regression

# Plot the linear regression line
plt.scatter(y_test, y_pred_lr, color='blue')  # Plot actual vs predicted values
plt.plot([min(y_test), max(y_test)], [min(y_pred_lr), max(y_pred_lr)], color='red')  # Plot the regression line
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Linear Regression Plot')
plt.show()

# logistic regression

from sklearn.linear_model import LogisticRegression

# ... (your existing code) ...

# Initialize and train a Logistic Regression model
logreg_model = LogisticRegression(random_state=42)  # You can adjust parameters like solver, C, etc.
logreg_model.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred_logreg = logreg_model.predict(X_test_scaled)

# Evaluate the model
print("Logistic Regression Evaluation:")
print(classification_report(y_test, y_pred_logreg))
print(confusion_matrix(y_test, y_pred_logreg))

# prompt: naive bays

from sklearn.naive_bayes import GaussianNB

# Initialize and train a Gaussian Naive Bayes classifier
nb_classifier = GaussianNB()
nb_classifier.fit(X_train_scaled, y_train)

# Make predictions on the test set
y_pred_nb = nb_classifier.predict(X_test_scaled)

# Evaluate the model
print("Naive Bayes Classifier Evaluation:")
print(classification_report(y_test, y_pred_nb))
print(confusion_matrix(y_test, y_pred_nb))

# prompt: KNN classifier

# Initialize and train a KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=5)  # You can adjust the number of neighbors
knn_classifier.fit(X_train_scaled, y_train)

# Make predictions on the test set
knn_predictions = knn_classifier.predict(X_test_scaled)

# Evaluate the KNN model
print("KNN Classifier Evaluation:")
print(classification_report(y_test, knn_predictions))
print(confusion_matrix(y_test, knn_predictions))

# prompt: ensemble model

# Initialize and train an ExtraTreesClassifier
extra_trees_classifier = ExtraTreesClassifier(random_state=42)
extra_trees_classifier.fit(X_train_scaled, y_train)

# Make predictions on the test set
extra_trees_predictions = extra_trees_classifier.predict(X_test_scaled)

# Evaluate the ExtraTreesClassifier model
print("ExtraTreesClassifier Evaluation:")
print(classification_report(y_test, extra_trees_predictions))
print(confusion_matrix(y_test, extra_trees_predictions))


# Initialize and train a BaggingClassifier with a decision tree base estimator
bagging_classifier = BaggingClassifier(random_state=42)
bagging_classifier.fit(X_train_scaled, y_train)

# Make predictions
bagging_predictions = bagging_classifier.predict(X_test_scaled)

# Evaluate the BaggingClassifier
print("BaggingClassifier Evaluation:")
print(classification_report(y_test, bagging_predictions))
print(confusion_matrix(y_test, bagging_predictions))


# Create a voting classifier
from sklearn.ensemble import VotingClassifier

voting_clf = VotingClassifier(estimators=[('rf', clf), ('et', extra_trees_classifier), ('bag', bagging_classifier), ('knn', knn_classifier)], voting='hard') #voting='soft' for probability-based voting

voting_clf.fit(X_train_scaled, y_train)
voting_pred = voting_clf.predict(X_test_scaled)

print("VotingClassifier Evaluation:")
print(classification_report(y_test, voting_pred))
print(confusion_matrix(y_test, voting_pred))

# Define features (X) and target (y) 'protocol_type', 'packet_type', 'traffic_type', 'alerts_warnings', 'attack_type', 'severity_level'],
#X = num_df.drop('alerts_warnings', axis=1)  # Features #This includes non-numerical columns
#X = df[['protocol_type', 'packet_type', 'traffic_type', 'alerts_warnings', 'attack_type']] # Select only numerical columns
#X = num_df[['protocol_type', 'traffic_type', 'alerts_warnings',]] # Select only numerical columns
num_df['combined_protocol_traffic'] = num_df['protocol_type'] * 10 + num_df['traffic_type']  # Changed num2_df to num_df
X = num_df[['combined_protocol_traffic']] # Assign the new combined feature to X, but keep it as a DataFrame using double brackets
y = num_df['alerts_warnings']  # Target variable

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% training and 20% test

# Scale the numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Initialize and train a classifier (e.g., RandomForestClassifier)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_scaled, y_train)


# Make predictions on the test set
y_pred = clf.predict(X_test_scaled)


# Evaluate the model
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# prompt: confusion matrix

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Assuming y_test and y_pred are already defined from your model predictions

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=['No Alert', 'Alert Triggered'],
            yticklabels=['No Alert', 'Alert Triggered'])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

num_df.head()

# prompt: feature importance

# Get feature importances from the trained RandomForestClassifier
feature_importances = clf.feature_importances_

# Create a DataFrame to display feature importances
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})

# Sort the DataFrame by importance in descending order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Print or display the feature importances
feature_importance_df

# prompt: suggestions

# Assuming 'df' is your DataFrame and you've already performed the preprocessing steps.

# Example: Feature Engineering - Interaction between Protocol and Traffic Type
num_df['protocol_traffic_interaction'] = num_df['protocol_type'] * num_df['traffic_type']

# Example: Feature Engineering - Ratio of Protocol to Packet Type
num_df['protocol_packet_ratio'] = num_df['protocol_type'] / (num_df['packet_type'] + 1e-6)  # Adding a small value to avoid division by zero


#Re-run the model with the new features
# Define features (X) and target (y) - Include the new engineered features
X = num_df[['protocol_traffic_interaction', 'protocol_packet_ratio']]
y = num_df['alerts_warnings']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model (example: RandomForest)
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_scaled, y_train)

# Make predictions
y_pred = clf.predict(X_test_scaled)

# Evaluate the model
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))


#Further suggestions:

#1. More Advanced Feature Engineering: Explore polynomial features, or other transformations based on domain expertise.
#2. Hyperparameter Tuning:  Use GridSearchCV or RandomizedSearchCV to find the best hyperparameters for your chosen classifier.
#3. Model Selection: Experiment with other classifiers (e.g., Gradient Boosting, Support Vector Machines, Neural Networks) and compare their performance.
#4. Feature Importance: Analyze feature importance from tree-based models (RandomForest, ExtraTrees) to understand which features are most influential.
#5. Dimensionality Reduction: If you have many features, consider using PCA or other dimensionality reduction techniques.
#6. Cross-Validation: Use more robust cross-validation techniques like k-fold or stratified k-fold to get a better estimate of the model's performance.
#7. Handling Class Imbalance: If your target variable has imbalanced classes, consider using techniques like SMOTE or adjusting class weights in your classifier.
#8. Visualizations: Create more visualizations to explore the data further and gain more insights. Consider pairplots or scatter plots of important features.
#9. Robustness testing: Evaluate the model's performance on different subsets of your data to assess its robustness.

# Support Vector Machine

# Initialize and train an SVM classifier
svm_clf = SVC(random_state=42)  # You can adjust hyperparameters like C, kernel, etc.
svm_clf.fit(X_train_scaled, y_train)

# Make predictions
y_pred_svm = svm_clf.predict(X_test_scaled)

# Evaluate the SVM model
print("SVM Classification Report:")
print(classification_report(y_test, y_pred_svm))
print("SVM Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_svm))