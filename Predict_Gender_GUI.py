# Import libraries
import cv2
import numpy as np
from keras.models import load_model
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
from tkinter import ttk


# Load model h5
model = load_model("Predict_Gender_model2.h5")

# Reshape input photo
input_shape = (150, 150)

# List label
labels = ['Male', 'Female']


# process input photo and predict function
def recognize_face(image):
    resized_image = image.resize(input_shape)
    rgb_image = resized_image.convert('RGB')
    face_image = np.array(rgb_image) / 255
    face_image = np.expand_dims(face_image, axis=0)
    prediction = model.predict(face_image)
    predicted_label = np.argmax(prediction)
    return predicted_label

# camera recognition function 
def recognition_from_camera():
    cap = cv2.VideoCapture(0)
    while True:
        # Read frame from cam
        ret, frame = cap.read()
        
        # design face recognition frame 
        frame_height, frame_width = frame.shape[:2]
        top_left = ((frame_width - 270) // 2, (frame_height - 270) // 2)
        bottom_right = (top_left[0] + 270, top_left[1] + 270)

        # set + center in frame 
        text = '+'
        font_scale = 0.8
        font_thickness = 2
        font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_width = text_size[0]
        text_height = text_size[1]
        text_x = top_left[0] + (270 - text_width) // 2
        text_y = top_left[1] + (270 - text_height) // 2

        # convert frame to Image
        image = Image.fromarray(frame)

        # predict with function recognize_face()
        label = recognize_face(image)

        # draw face frame and show label result
        if label is not None:
            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 0), 2)
            cv2.putText(frame, 'Recognition Result: {}'.format(labels[label]), (10, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.9, (255, 0, 0), 2)

       
        # Detect Face
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0,0,255), font_thickness, cv2.LINE_AA)

        
        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty('Face Recognition', cv2.WND_PROP_VISIBLE)<1:
            break

    cap.release()
    cv2.destroyAllWindows()

# Recognize image from library funciton
def recognition_from_image():
    root = tk.Tk()
    root.withdraw()

    # Select image from folder
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        resized_image = image.resize(input_shape)
        rgb_image = resized_image.convert('RGB')
        label = recognize_face(rgb_image)

        # draw face frame and show result label 
        if label is not None:
            image_with_box = np.array(image)
            cv2.rectangle(image_with_box, (0, 0), (image.width, image.height), (255, 255, 255), 2)
            # Resize image window
            display_width = 400
            display_height = 500
            image_with_box = cv2.cvtColor(image_with_box, cv2.COLOR_RGB2BGR)
            resized_display = cv2.resize(image_with_box, (display_width, display_height))
            cv2.putText(resized_display, 'Recognition Result: {}'.format(labels[label]), (25, 30), cv2.FONT_HERSHEY_TRIPLEX,
                        0.7, (255, 0, 0), 1)
            
            cv2.imshow('Face Recognition', resized_display)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
# Show time
def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    time_label.config(text=current_time)
    window.after(1000, update_time)
    
    
### Design interface

# open cam to predict
def open_camera():
    recognition_from_camera()

# load image to predict
def open_image():
    recognition_from_image()

def exit_program():
    response = messagebox.askquestion("Confirmation", "Do you want to close the program?")

    if response == 'yes':
        window.destroy()
    else:
        messagebox.showinfo("Information", "The program will continue.")
    

# Design interface
window = tk.Tk()
window.title("Face Recognition Program")
window.geometry("640x611")
background_image = Image.open("bg12.jpg")  
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# show clock
time_label = tk.Label(window, font=("Courier New", 20), borderwidth=2, relief="solid")
time_label.place(x=486, y=25)

update_time()

style = ttk.Style()

# Define button style
style.configure("Custom.TButton", font=("Arial", 14), foreground="white", background="#443dcc", padding=10)
style.map("Custom.TButton",
          foreground=[("pressed", "green"), ("active", "green")],
          background=[("pressed", "#0c04b3"), ("active", "#0c04b3")])

# Label information
label1 = tk.Label(window, text="Nguyễn Minh Tấn", font=("Verdana", 22, "bold"), bg="#d8e9f2", foreground="#260961")
label1.place(x=20, y=30)

label2 = tk.Label(window, text="ID: 20146417", font=("Verdana", 22, "bold"), bg="#d8e9f2", foreground="#260961")
label2.place(x=20, y=90)

# Label Select
function_label = tk.Label(window, text="Select function:", font=("Georgia", 20, "bold"), bg="#d8e9f2", foreground="black")
function_label.place(x=20, y=180)

# Label Use Camera
camera_label = tk.Label(window, text="Recognition gender by camera:", font=("Times New Roman", 18), bg="#d8e9f2", foreground="black")
camera_label.place(x=20, y=270)

# Label import image
image_label = tk.Label(window, text="Recognition gender by image:", font=("Times New Roman", 18), bg="#d8e9f2", foreground="black")
image_label.place(x=20, y=380)

# Button Camera
button1 = ttk.Button(window, text="Turn camera on", style="Custom.TButton", command=open_camera)
button1.place(x=370, y=262)


# Button import image

button2 = ttk.Button(window, text="Load image", style="Custom.TButton", command=open_image)
button2.place(x=370, y=370)


# Button exit
exit_button = tk.Button(window, text="Exit",font=("Verdana", 22, "bold"), command=exit_program, bg="#FF0000", fg="white", relief="solid", bd=3, width=5, activebackground="green")
exit_button.place(x=260, y=500)



window.mainloop()