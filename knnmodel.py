import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle

# preprocess images
def preprocess_image(image, target_size=(100, 100)):
    return cv2.resize(image, target_size).flatten()

# Train KNN save 
def train_knn_model():
    X, y = [], []
    people = os.listdir('dataset')

    for person in people:
        person_folder = f'dataset/{person}'
        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name) #dataset/miwan/1
            image = cv2.imread(image_path)  #readimage of imagepath
            if image is not None:
                processed_image = preprocess_image(image)
                X.append(processed_image)
                y.append(person)
    
    X, y = np.array(X), np.array(y)
    knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
    knn.fit(X, y)

    # save model in file
    with open('knn_model.pkl', 'wb') as f:
        pickle.dump(knn, f)  
    print("KNN model trained and saved as 'knn_model.pkl'.")

if __name__ == "__main__":
    train_knn_model()


