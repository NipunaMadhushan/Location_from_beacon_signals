from New.GetData import Dataset
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd

# Import dataset
X, y = Dataset()

# Divide data into training and testing datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

def svm_train_model():
    svclassifier = SVC(kernel='poly')
    svclassifier.fit(X_train, y_train)

    return svclassifier


def rf_train_model():
    rfclassifier = RandomForestClassifier(n_estimators=100, max_depth=15)
    rfclassifier.fit(X_train, y_train)

    return rfclassifier


def dt_train_model():
    dtclassifier = DecisionTreeClassifier(max_depth=15)
    dtclassifier.fit(X_train, y_train)

    return dtclassifier


def logistic_train_model():
    logisticclf = LogisticRegression()
    logisticclf.fit(X_train, y_train)

    return logisticclf


def test_model(classifier):
    # Test the model with test data
    print("Test Accuracy: ", classifier.score(X_test, y_test))

    # Make predictions for test data
    y_pred = classifier.predict(X_test)

    # Evaluating the model
    #Confusion matrix, precision, recall, and F1 measures are the most commonly used metrics for classification tasks.
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


def predict_location(svclassifier, data):
    pred = svclassifier.predict([data])

    return pred[0]


#print("Test Results of SVM Model: ")
#clf1 = svm_train_model()
#test_model(clf1)



# To compare the predicted values with each model
clf1 = logistic_train_model()
clf2 = dt_train_model()
clf3 = rf_train_model()
clf4 = svm_train_model()

y_pred1 = clf1.predict(X_test)
y_pred2 = clf2.predict(X_test)
y_pred3 = clf3.predict(X_test)
y_pred4 = clf4.predict(X_test)

test_acc1 = clf1.score(X_test, y_test)
test_acc2 = clf2.score(X_test, y_test)
test_acc3 = clf3.score(X_test, y_test)
test_acc4 = clf4.score(X_test, y_test)

train_acc1 = clf1.score(X_train, y_train)
train_acc2 = clf2.score(X_train, y_train)
train_acc3 = clf3.score(X_train, y_train)
train_acc4 = clf4.score(X_train, y_train)


print("Results:")
data1 = {"Acutual": y_test, "Logistic Regression": y_pred1, "Decision Tree": y_pred2, "Random Forest": y_pred3,
        "SVM": y_pred4}

df1 = pd.DataFrame(data1)
print(df1.head(25))

print("Test Accuracies:")
data2 = {"Dataset": ["Train", "Test"], "Logistic Regression": [train_acc1, test_acc1], "Decision Tree": [train_acc2, test_acc2],
        "Random Forest": [train_acc3, test_acc3], "SVM": [train_acc4, test_acc4]}

df2 = pd.DataFrame(data2)
print(df2)



