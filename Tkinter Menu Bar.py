#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk
import pyttsx3
import speech_recognition as sr
from tkinter import messagebox
import subprocess
import boto3
import tkinter.filedialog as filedialog
from cvzone.HandTrackingModule import HandDetector
import requests
from PIL import Image, ImageTk
import os
import re
import cv2
import time
import qrcode
import webbrowser
import tkinter.simpledialog as simpledialog
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

def do_something():
    messagebox.showinfo("Info", "Team 7 - Azfar")

def system_app():
    system_window = tk.Toplevel(root)
    system_window.title("System Apps")
    system_window.geometry("400x275")
    system_window.configure(bg="lightgray")
    
    system_label = tk.Label(system_window, text="System Apps", font=("Arial", 20,))
    system_label.pack(pady=10)

    notepad_button = tk.Button(system_window, text="Open Notepad", width=25, fg='Black', command=open_notepad)
    notepad_button.pack(pady=10)

    calculator_button = tk.Button(system_window, text="Open Calculator", width=25, fg='Black', command=open_calculator)
    calculator_button.pack(pady=10)
    
    system_info_button = tk.Button(system_window, text="System Info", width=25, command=show_system_info)
    system_info_button.pack(pady=10)

    close_button = tk.Button(system_window, text="Close",width=25, command=system_window.destroy)
    close_button.pack(pady=10)
    
def aws_operations_window():
    aws_window = tk.Toplevel(root)
    aws_window.title("AWS Operations")
    aws_window.geometry("400x350")
    aws_window.configure(bg="lightgray")
    
    aws_label = tk.Label(aws_window, text="AWS Operations", font=("Arial", 20, "bold"))
    aws_label.pack(pady=10)

    ec2_button = tk.Button(aws_window, text="Create EC2 Instance",width=25, command=open_ec2_instance)
    ec2_button.pack(pady=15)

    s3_button = tk.Button(aws_window, text="Create S3 Bucket",width=25, command=create_s3_bucket)
    s3_button.pack(pady=15)
    
    s3_button = tk.Button(aws_window, text="Upload to S3",width=25, command=upload_to_s3)
    s3_button.pack(pady=15)
    
    list_ec2_button = tk.Button(aws_window, text="List EC2 Instances", width=25, command=list_ec2_instances)
    list_ec2_button.pack(pady=15)

    close_button = tk.Button(aws_window, text="Close",width=25, command=aws_window.destroy)
    close_button.pack(pady=10)

def on_exit():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def open_notepad():
    subprocess.Popen("notepad.exe")

def open_calculator():
    subprocess.Popen("calc.exe")

import boto3

def list_ec2_instances():
    try:
        ec2 = boto3.client("ec2")
        response = ec2.describe_instances()
        instances = response["Reservations"]

        if not instances:
            messagebox.showinfo("No EC2 Instances", "No EC2 instances found.")
        else:
            instance_info = "\n".join([f"ID: {instance['Instances'][0]['InstanceId']}, "
                                       f"State: {instance['Instances'][0]['State']['Name']}"
                                       for instance in instances])
            messagebox.showinfo("EC2 Instances", f"List of EC2 instances:\n{instance_info}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list EC2 instances: {e}")

def open_ec2_instance():
    response = messagebox.askyesno("AWS EC2 Instance", "Do you want to create an EC2 instance?")
    if response:
        myec2 = boto3.client("ec2")
        response = myec2.run_instances(  
            ImageId='ami-0ded8326293d3201b', 
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1
        )
        print(response)

def create_s3_bucket():
    response = messagebox.askyesno("AWS S3 Bucket", "Do you want to create an S3 bucket?")
    if response:
        s3 = boto3.client('s3')
        s3 = s3.create_bucket(
            Bucket='tareybs3244',
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'us-west-1'
            }
        )
        print("Bucket created successfully with the following response:")
        print(s3)
        print("Bucket 'new' was created in the 'us-west-1' region.")
        
def upload_to_s3():
    bucket_name = simpledialog.askstring("Upload to S3 Bucket", "Enter the bucket name:")
    if bucket_name:
        file_path = filedialog.askopenfilename(title="Select a file to upload")
        if file_path:
            try:
                s3 = boto3.client("s3")
                file_name = os.path.basename(file_path)
                s3.upload_file(file_path, bucket_name, file_name)
                messagebox.showinfo("Upload Successful", f"File '{file_name}' uploaded to '{bucket_name}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload file: {e}")

def open_youtube():
    song_name = simpledialog.askstring("Open YouTube", "Enter the name of your favorite song:")
    if song_name:
        search_query = song_name.replace("", "+")
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

def show_system_info():
    response = messagebox.askyesno("System Info", "Want to see ?")
    system_info = subprocess.check_output("systeminfo", shell=True)
    messagebox.showinfo("System Information", system_info)

def google_search():
    search_query = simpledialog.askstring("Google Search", "Enter your search query:")
    if search_query:
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        

def deaf_people_help():
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  
    engine.setProperty("volume", 1.0)
    cap=cv2.VideoCapture(0)
    model=HandDetector()
    while True:
        status,photo=cap.read()
        cv2.imshow("pic1",photo)
        if cv2.waitKey(10)==13:
            break

        hand=model.findHands(photo,draw=False)
        if hand:
            handPhoto=hand[0]
#    print(handPhoto)
            fingerlist=model.fingersUp(handPhoto)        
            if fingerlist==[0,1,1,1,1]:
                engine.say("namaste")
                engine.runAndWait()
                print("namaste")
                time.sleep(2)
            elif fingerlist==[1,0,0,0,0]:
                engine.say("Good job")
                engine.runAndWait()
                print("Good job")
                time.sleep(2)
            elif fingerlist==[0,1,1,0,0]:
                engine.say("Pleasure meeting with you")
                engine.runAndWait()
                print("Pleasure meeting with you")
                time.sleep(2)
            elif fingerlist==[0,1,1,0,0]:
                engine.say("Perfect")
                engine.runAndWait()
                print("Perfect")
                time.sleep(2)
            elif fingerlist==[1,1,0,0,1]:
                engine.say("I love Vimal Sir")
                engine.runAndWait()
                print("I love Vimal Sir")
                time.sleep(2)
            elif fingerlist==[0,0,0,0,0]:
                engine.say("Sorry")
                engine.runAndWait()
                print("Sorry")
                time.sleep(2)
            elif fingerlist==[0,1,0,0,0]:
                engine.say("Help")
                engine.runAndWait()
                print("Help")
                time.sleep(2)
            else:
                print("dont support")
                time.sleep(2)
        


  
    cv2.destroyAllWindows()
    cap.release()
        

def capture_video():
    if messagebox.askyesno("Exit", "Want to Capture ?"):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter("captured_video.avi", fourcc, 20.0, (640, 480))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(5)==13:
            break

  
    out.release()
    cv2.destroyAllWindows()
    cap.release()

    messagebox.showinfo("Video Captured", "Video captured and saved as 'captured_video.avi'")
    
import requests

def get_weather():
    city = simpledialog.askstring("Weather Update", "Enter city name:")
    if city:
        api_key = "b468e8a2145b49204e0af7d5594d376a"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()
        if weather_data["cod"] == 200:
            weather_info = f"Weather in {city}: {weather_data['weather'][0]['description']}\n" \
                           f"Temperature: {weather_data['main']['temp']}°C\n" \
                           f"Humidity: {weather_data['main']['humidity']}%"
            messagebox.showinfo("Weather Update", weather_info)
        else:
            messagebox.showerror("Error", "Failed to fetch weather data.")

def voice_assistant():
    engine = pyttsx3.init()
    engine.say("How can I assist you?")
    engine.runAndWait()

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        messagebox.showinfo("Voice Assistant", f"You said: {recognized_text}")
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I couldn't understand what you said.")
    except sr.RequestError:
        messagebox.showerror("Error", "Sorry, the speech recognition service is currently unavailable.")

def generate_qr_code():
    data = simpledialog.askstring("QR Code Generator", "Enter the text or URL to encode:")
    if data:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qr_code.png")
        img.show()
        
        
def langchain():
    
    from langchain.llms import OpenAI
    myllm=OpenAI(
        model='text-davinci-003',
        temperature=1,
        openai_api_key="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"
    )

    myserpkey="694ae3d468f57a303cc7edbef0975064e8f3e0f2a4b639f06c1ae4c272f94951"

    import os
    os.environ['SERPAPI_API_KEY']=myserpkey

    from langchain.agents import load_tools
    myserptool=load_tools(tool_names=['serpapi'])

    from langchain.agents import AgentType
    from langchain.agents import initialize_agent
    mygooglechain=initialize_agent(
        llm=myllm,
        tools=myserptool,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    mygooglechain.run("when chandrayan 3 launched")
    
    
    

        

def rekoc():
    client = boto3.client('rekognition',region_name='us-west-1')
    with open("raj1.jpg",'rb') as imgFile:
        imgData=imgFile.read()
        response=client.detect_labels(Image={'Bytes':imgData},MaxLabels=8)
            
    labels= response["Labels"]
    labels
    for label in labels:
        print(f"Label: {label['Name']}, Confidence: {label['Confidence']:.2f}%")
        
        
def handpick():
    cap = cv2.VideoCapture(0) 
 
    mpHands = mp.solutions.hands 
    hands = mpHands.Hands()  
    mpDraw = mp.solutions.drawing_utils
 

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume.iid, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volbar=400
    volper=0
     
    volMin,volMax = volume.GetVolumeRange()[:2]
 
    while True:
        success,img = cap.read() 
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    
    
        results = hands.process(imgRGB) 
 
        lmList = [] 
        if results.multi_hand_landmarks: 
        
            for handlandmark in results.multi_hand_landmarks:
                for id,lm in enumerate(handlandmark.landmark): 
               
                    h,w,_ = img.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    lmList.append([id,cx,cy]) 
                mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    
        if lmList != []:
       
                       
            x1,y1 = lmList[4][1],lmList[4][2]  #thumb
            x2,y2 = lmList[8][1],lmList[8][2]  #index finger
        #creating circle at the tips of thumb and index finger
            cv2.circle(img,(x1,y1),13,(255,0,0),cv2.FILLED) #image #fingers #radius #rgb
            cv2.circle(img,(x2,y2),13,(255,0,0),cv2.FILLED) #image #fingers #radius #rgb
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)  #create a line b/w tips of index finger and thumb
 
            length = hypot(x2-x1,y2-y1) #distance b/w tips using hypotenuse
 # from numpy we find our length,by converting hand range in terms of volume range ie b/w -63.5 to 0
            vol = np.interp(length,[30,350],[volMin,volMax]) 
            volbar=np.interp(length,[30,350],[400,150])
            volper=np.interp(length,[30,350],[0,100])
        
        
            print(vol,int(length))
            volume.SetMasterVolumeLevel(vol, None)
        
        
    
            cv2.rectangle(img,(50,150),(85,400),(0,0,255),4) # vid ,initial position ,ending position ,rgb ,thickness
            cv2.rectangle(img,(50,int(volbar)),(85,400),(0,0,255),cv2.FILLED)
            cv2.putText(img,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(0, 255, 98),3)
      
        cv2.imshow('Image',img) 
        if cv2.waitKey(1) & 0xff==ord(' '): 
            break
        
    cap.release()           
    cv2.destroyAllWindows() 
    

def on_key_press4(email_id):
    pyk.send_mail("azfaralam440@gmail.com", "uidkxlsvorrhlbzr", "GUI Based Mail", "Hii.. Azfar this side", email_id)
    print("Email sent to:", email_id) 
    

def submit2():
    USER_INP = simpledialog.askstring(title="MAIL", prompt="Enter Email Id:")
    
    if USER_INP:
        on_key_press4(USER_INP)
    else:
        print("Email Id not provided.")
            
    
    
def on_key_press2():
    amis = [ 
        "ami-0c38b9e37c107d921" , "ami-0f8e81a3da6e2510a" ,
        "ami-0dc8c969d30e42996"    
    ]
    ami = ""
    
    def on_ec2_click(choice):
        if choice == "ubuntu":
            ami = amis[0]
        elif choice == "amazonlinux":
            ami = amis[1]
        elif choice == "rhel":
            ami = amis[2]
            
        ec2_client = boto3.client("ec2") 
        ec2 = ec2_client.run_instances(
            ImageId=ami,
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1
         )
        
    def submit4():
        choice = USER_INP
        main_choice = choice.lower()
        on_ec2_click(main_choice)
        
    
    USER_INP = simpledialog.askstring(title="EC2",prompt="Enter Name of AMI..")
     
    print(USER_INP)
    submit()    

    

def on_key_press3():
    webbrowser.open_new_tab("http://3.101.152.17/front.html")
    
    
    
        
# Create the main Tkinter window
root = tk.Tk()
root.title("Menu")
root.geometry("580x600")
root.configure(bg="yellow")
title_font = ("Arial", 24, "italic")
root.iconbitmap(r"azfaraa.jpg")

# emoji_img = tk.PhotoImage(file="pngegg.png")  # Replace with the path to your emoji image
# subsample_factor = 6  # Adjust this value to control the size of the image (higher value for smaller size)
# small_image = emoji_img.subsample(subsample_factor, subsample_factor)
# emoji_label = tk.Label(root, image=small_image, bg="black")
# emoji_label.grid(row=2, column=5, columnspan=1, pady=5)

# Welcome Text
title_label = tk.Label(root, text="Python Menu", font=title_font, fg="black")
title_label.grid(row=0,column=0,padx=20, pady=40)


notepad_button = tk.Button(root, text="System Apps", width=25, fg='Black', command=system_app)
notepad_button.grid(row=1,column=0,padx=20, pady=40)

capture_video_button = tk.Button(root, text="Capture Video", width=25, command=capture_video)
capture_video_button.grid(row=1,column=1,padx=20, pady=20)

weather_button = tk.Button(root, text="Weather Update", width=25, command=get_weather)
weather_button.grid(row=1,column=2,padx=30, pady=20)

aws_button = tk.Button(root, text="AWS Operations", width=25, command=aws_operations_window)
aws_button.grid(row=1,column=3,padx=10, pady=20)

browser_button = tk.Button(root, text="Youtube", width=25, command=open_youtube)
browser_button.grid(row=2,column=0,padx=20, pady=20)

google_button = tk.Button(root, text="Google Search", width=25, command=google_search)
google_button.grid(row=2,column=1,padx=30, pady=20)

deaf_people_help = tk.Button(root, text="Communicate With Deaf People", width=25, command=deaf_people_help)
deaf_people_help.grid(row=2,column=2,padx=10, pady=20)

voice_assistant_button = tk.Button(root, text="Voice Assistant", width=25, command=voice_assistant)
voice_assistant_button.grid(row=2,column=3,padx=10, pady=20)

qr_code_button = tk.Button(root, text="Generate QR Code", width=25, command=generate_qr_code)
qr_code_button.grid(row=3,column=0,padx=20, pady=20)

qr_code_button = tk.Button(root, text="GOOGLE+GPT", width=25, command=langchain)
qr_code_button.grid(row=3,column=1,padx=30, pady=20)

qr_code_button = tk.Button(root, text="Image-Recog", width=25, command=rekoc)
qr_code_button.grid(row=3,column=2,padx=20, pady=20)

qr_code_button = tk.Button(root, text="Hand-Vol", width=25, command=handpick)
qr_code_button.grid(row=3,column=3,padx=30, pady=20)

qr_code_button = tk.Button(root, text="SENT-MAIL", width=25, command=submit2)
qr_code_button.grid(row=4,column=0,padx=20, pady=20)

# qr_code_button = tk.Button(root, text="EC_2", width=25, command=submit4)
# qr_code_button.grid(row=4,column=1,padx=30, pady=20)

qr_code_button = tk.Button(root, text="CGI-DOCKER", width=25, command=on_key_press3)
qr_code_button.grid(row=4,column=2,padx=20, pady=20)




button = tk.Button(root, text="Exit",width=25, command=on_exit)
button.grid(row=6,column=2,padx=20, pady=20)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a file menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_exit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Team Info", command=do_something)
menu_bar.add_cascade(label="About", menu=help_menu)

# Start the Tkinter event loop
root.mainloop()


# In[ ]:




