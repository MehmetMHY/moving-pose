import pandas as pd
import os

# returns the accuracy of the predictions
def theAccuracy(real, predict):
    total = 0
    for i in range(len(real)):
        if(real[i] == predict[i]): total = total + 1
    return (round((total / len(real))*100, 2))

# creates confusion matrix
def confusionMatrix(actual, prediction):
    action = pd.Series(actual, name="Actual")
    predict = pd.Series(prediction, name="Predicted")
    confusion = pd.crosstab(action, predict)
    print(confusion)
    print("Accuracy:", theAccuracy(actual, prediction))


# testing
actions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
predicted = [1, 2, 4, 5, 5, 6, 7, 8, 9, 10]
confusionMatrix(actions, predicted)


