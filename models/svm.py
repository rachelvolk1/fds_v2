from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

def train_svm_model(filename):
    # Load the dataset from the provided filename
    df = pd.read_csv(filename)
    
    # Assuming 'target' is the column to predict
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the SVM model
    model = svm.SVC(kernel='linear')
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"SVM Model Accuracy: {accuracy:.2f}")
    return accuracy
