from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def get_database():
    data_x = [[0, 0, 0, 0],[0, 0, 0, 1],[0, 0, 1, 0],[0, 0, 1, 1], 
              [0, 1, 0, 0],[0, 1, 0, 1],[0, 1, 1, 0],[0, 1, 1, 1],
              [1, 0, 0, 0],[1, 0, 0, 1],[1, 0, 1, 0],[1, 0, 1, 1],
              [1, 1, 0, 0],[1, 1, 0, 1],[1, 1, 1, 0],[1, 1, 1, 1]] 
    data_y = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    print("DATABASE")
    print("      Data base (100 %): ", data_x)
    print(" Classification (100 %): ", data_y)
    print("\n")

    return data_x, data_y

def run_ml_model(data_x, data_y):
    ml_model = LinearSVC()
    training_x, test_x, training_y, test_y = train_test_split(data_x, data_y)
    ml_model.fit(training_x, training_y)
    print("\n")
    print("TRAINING AND TEST ACCURACY:")
    print("\n")
    print("       Data test (25 %): ", test_x)
    print(" Expected result (25 %): ", test_y)
    print("\n")

    ml_predict = ml_model.predict(test_x)
    ml_accuracy = accuracy_score(test_y, ml_predict) * 100
    print("             ML predict: ", ml_predict)
    print("            ML accuracy: " + str(round(ml_accuracy, 2)) + " % \n")


if __name__ == "__main__":
    print("\n----------------- Machine Learning -----------------\n")

    data_x, data_y = get_database()

    while(1):
        inputMessage = input("Run ML test? (y/n): ") 
        if (inputMessage == "y"): run_ml_model(data_x, data_y)
        else              : break 

    print("\n----------------------------------------------------\n")