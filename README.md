# FaceRecognizer
Face Recognition using OpenCV

There are two python files.
1. DataGeneration.py
2. FaceRecognition.py
Step 1:
• First run the DataGeneration.py. It will give you user input for
user’s name, and it will store the frames which are collected from
the cap in a Frames folder..
• And user’s data will be stored into images.db which contains
PersonINFO table.
Step 2:
• In step 2 I have used LBPHFaceRecognizer model which is
provided by opencv. It is built in model for the face recognition.
• So, I have trained it and predict it with the help of YAML file
which is I have created and save the user’s data in it.
• After the prediction I have compare the name with the predicted
name.
• If predicted name is true than it will show you the result which you
ask for. For ex. Hello Vaibhav at above of the rectangular box in
the video cap.
• If it isn’t than it will shows the result as a new member and it will
ask for two choice (yes, no) for saving the new member’s data. If it
is yes than it will call the DataGeneration.py. If it is no than
program will be shut down.
