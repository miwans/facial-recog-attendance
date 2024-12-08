import cv2
import os

# Path to Haar Cascade 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Preprocess the image 
def preprocess_image(image, target_size=(100, 100)):
    resized_image = cv2.resize(image, target_size)  
    return resized_image

# Capture images from the webcam and save to dataset
def capture_images(person_name, num_images=50):
    # Open the webcam
    cam = cv2.VideoCapture(0) 
    if not cam.isOpened():
        print("Error: Could not access the webcam.")
        return

    # if it doesn't exist
    os.makedirs(f'dataset/{person_name}', exist_ok=True)
    count = 0

    # Loop to capture number of images
    while count < num_images:
        ret, frame = cam.read()  
        if not ret:
            print("Error: Failed to capture an image from the webcam.")
            break

        # Detect facenframe
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)

        # Display the frame
        cv2.imshow('Capturing Faces', frame)

        # if no face is detected
        if len(faces) == 0:
            print("No face detected. Make sure your face is visible in the camera.")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # loop through all faces
        for (x, y, w, h) in faces:
            count += 1
            face = frame[y:y + h, x:x + w]  # face region
            face_resized = preprocess_image(face)  

            # Save to folder
            save_path = f'dataset/{person_name}/{count}.jpg'
            cv2.imwrite(save_path, face_resized)
            print(f"Captured {count}/{num_images} images for {person_name} (saved at {save_path})")

            #  a rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"Capturing {count}/{num_images}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # the current frame with face
        cv2.imshow('Capturing Faces', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()  
    cv2.destroyAllWindows()  

    if count == num_images:
        print(f"Successfully captured {num_images} images for {person_name}.")
    else:
        print(f"Stopped after capturing {count} images for {person_name}.")

if __name__ == "__main__":
    # Take person name as input and start capturing
    person_name = input("Enter the person's name: ")
    recognized_student_id=input("Enter ID:")
    capture_images(person_name, num_images=5)

