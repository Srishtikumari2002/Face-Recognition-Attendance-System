import csv
import datetime
import os
from tkinter import *
from tkinter import font
from tkinter import ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

#____________________________________________________________________________________________________________________________________________________________________
# main app class
class rootApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.font = font.Font(family="Helvetica", size=28, weight="bold")

        self.geometry("1200x700")
        self.resizable(width=False, height=False)
        self.title("Attendance System")
        self.iconbitmap(default="Files/icon.ico")
        #we will place mltiple frames in a container
        #and show the one we want

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in (HomePage, StudentsPage, AttendancePage, RecordATTPage, CreateDataPage):
            page_name = i.__name__
            frame = i(parent=container, controller=self)
            self.frames[page_name] = frame

            #put all of the pages in the same location
            #the one on the top of the stacking order
            #will be the one that is visible
      
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("HomePage") 

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()  

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________
# variables to be used
n=0
haar_file = 'Files/haarcascade_frontalface_default.xml'
datasets = 'Dataset'
#____________________________________________________________________________________________________________________________________________________________________
# homepage class
class HomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="White")

        logo = ImageTk.PhotoImage(Image.open("Files/icon.png"))
        logo_btn = Button(self, text="Attendance System", command=lambda : controller.show_frame("HomePage"), font=("Helvetica", 15, "bold"), bd=0, image=logo, bg="white", compound="left", activebackground="white")
        logo_btn.image = logo
        logo_btn.place(x=0,y=0)

        self.drawer = Frame(self, bg="#f2f0ed", bd=2)
        # let's add options to self.drawer
        stu_img = ImageTk.PhotoImage(Image.open("Files/students.png").resize((70,70)))
        stu_btn = Button(self.drawer, bd=0, text="Students", image=stu_img, compound="top", bg="white", activebackground="white",command=lambda:controller.show_frame("StudentsPage"))
        stu_btn.image = stu_img
        stu_btn.grid(row=0,column=0)

        att_img = ImageTk.PhotoImage(Image.open("Files/attendance.png").resize((70,70)))
        att_btn = Button(self.drawer, bd=0, text="Attendance", image=att_img, compound="top", bg="white", activebackground="white", command=lambda:controller.show_frame("AttendancePage"))
        att_btn.image = att_img
        att_btn.grid(row=0,column=1)

        tr_img = ImageTk.PhotoImage(Image.open("Files/record.png").resize((70,70)))
        tr_btn = Button(self.drawer, bd=0, text="Record", image=tr_img, compound="top", bg="white", activebackground="white", command=lambda:controller.show_frame("RecordATTPage"))
        tr_btn.image = tr_img
        tr_btn.grid(row=1,column=0)

        cr_img = ImageTk.PhotoImage(Image.open("Files/create.png").resize((70,70)))
        cr_btn = Button(self.drawer, bd=0, text="Sample Data", image=cr_img, compound="top", bg="white", activebackground="white", command=lambda:controller.show_frame("CreateDataPage"))
        cr_btn.image = cr_img
        cr_btn.grid(row=1,column=1)

        def control_drawer():
            global n
            if n==0:
                self.drawer.place(x=1030,y=40)
                self.drawer.tkraise()
                n+=1

            elif n==0:
                self.drawer.place(x=1030,y=40)
                self.drawer.tkraise()
                n+=1
            else:
                self.drawer.place_forget()
                n-=1

        features = Button(self, activebackground="white", bg="white", bd=0, text="⫶⫶⫶", compound="top", command=control_drawer, font=("Helvetica", 18, "bold"))
        features.place(x=1120, y=-5)

        def settime():
            dateandtime = datetime.datetime.now()
            date_time.config(text=str(dateandtime.strftime("%I:%M %p.%a,%b %d")))
            date_time.after(1000, settime)


        date_time = Label(self, bd=0, bg="white", fg="black", font=("courier", 15))
        settime()
        date_time.place(x=870, y=5)


        lbl2 = Label(self, text="Easily record attendence during your class.", justify="left", wraplength=580, font=("Helvetica", 26), fg="grey", bg="white")
        lbl2.place(x=80, y=260)
        
        record = Button(self, text="Take Attendance", command=lambda:controller.show_frame("RecordATTPage"), bd=0, font=("Helvetica", 26), fg="Black", bg="white")
        record.place(x=80, y= 350)

        show_img = ImageTk.PhotoImage(Image.open("Files/attendance.png").resize((300,280)))
        showcase = Label(self, bg="white", image = show_img)
        showcase.image = show_img
        showcase.place(x=830, y=210)

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________
# students list page class
class StudentsPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "white")

        logo = ImageTk.PhotoImage(Image.open("Files/icon.png"))
        logo_btn = Button(self, text="Attendance", command=lambda : controller.show_frame("HomePage"), font=("Helvetica", 15, "bold"), bd=0, image=logo, bg="white", compound="left", activebackground="white")
        logo_btn.image = logo
        logo_btn.place(x=0,y=0)

        title = Label(self, text= "Students List", bg  ="White", fg ="red", font=("Helvetica", 25, "italic"))
        title.place(relx=0.5,rely=0.1,anchor=CENTER)

        TableMargin1 = Frame(self, width=500)
        TableMargin1.place(relx=0.1, rely=0.2)
        scrollbary1 = Scrollbar(TableMargin1, orient=VERTICAL)

        table1 = ttk.Treeview(TableMargin1, columns=("Name"), height=400, selectmode="extended", yscrollcommand=scrollbary1.set)
        scrollbary1.config(command=table1.yview)
        scrollbary1.pack(side=RIGHT, fill=Y)

        table1.heading('Name', text="Name", anchor=W)
        table1.column('#0', stretch=NO, minwidth=0, width=0)
        table1.column('#1', stretch=NO, minwidth=0, width=200)
        table1.pack()

        def show_st():
            
            if os.path.isdir('Dataset') == True:
                for item in table1.get_children():
                    table1.delete(item)
                for i in os.listdir('Dataset'):
                    table1.insert("", 0, values=i)
                
            table1.after(100, show_st)
        
        show_st()

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________
# students list page class
class CreateDataPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "white")

        logo = ImageTk.PhotoImage(Image.open("Files/icon.png"))
        logo_btn = Button(self, text="Attendance", command=lambda : controller.show_frame("HomePage"), font=("Helvetica", 15, "bold"), bd=0, image=logo, bg="white", compound="left", activebackground="white")
        logo_btn.image = logo
        logo_btn.place(x=0,y=0)
        
        def record():
            sub_data = name.get()
            datasets = "Dataset"
            path = os.path.join(datasets, sub_data)

            if os.path.isdir(path):
                count = len([name for name in os.listdir(path) if os.path.isfile(name)])+1
            else:
                os.mkdir(path)
                count = 1

            face_cascade = cv2.CascadeClassifier(haar_file)
            webcam = cv2.VideoCapture(0)
            name.set("")
            while True:
                (_, im) = webcam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for(x,y,w,h) in faces:
                    cv2.rectangle(im, (x,y), (x+w,y+h), (255,0,0), 2)
                    face = gray[y:y+h, x:x+w]
                    face_resize = cv2.resize(face, (130, 100))
                    cv2.imwrite('% s/% s.png' % (path, count), face_resize)
                count += 1

                cv2.imshow('Taking Samples', im)
                key = cv2.waitKey(10)
                if key == 27:
                    cv2.destroyAllWindows()
                    break
        
        name = StringVar()
        lbl = Label(self, text="Enter Your Name", bg="White", font=("Helvetica", 16, "bold"))
        e = Entry(self, textvariable=name, font=('calibre',15,'normal'))

        lbl.pack()
        e.pack()

        capture = Button(self, text="Open Camera", bd=0, bg="blue", fg="white", activeforeground="black", command=record)
        capture.pack()
            
#_____________________________________________________________________________________________________________________________________________________________________________________________________________________
# attendance page class
class AttendancePage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "white")

        logo = ImageTk.PhotoImage(Image.open("Files/icon.png"))
        logo_btn = Button(self, text="Attendance", command=lambda : controller.show_frame("HomePage"), font=("Helvetica", 15, "bold"), bd=0, image=logo, bg="white", compound="left", activebackground="white")
        logo_btn.image = logo
        logo_btn.place(x=0,y=0)

        title = Label(self, text= "Attendance", bg  ="White", fg ="red", font=("Helvetica", 25, "italic"))
        title.place(relx=0.5,rely=0.1,anchor=CENTER)

        TableMargin = Frame(self, width=500)
        TableMargin.place(relx=0.1, rely=0.2)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)

        table = ttk.Treeview(TableMargin, columns=("Name", "Attendance", "Date", "Time"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=table.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=table.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)

        table.heading('Name', text="Name", anchor=W)
        table.heading('Attendance', text="Attendance", anchor=W)
        table.heading('Date', text="Date", anchor=W)
        table.heading('Time', text="Time", anchor=W)
        table.column('#0', stretch=NO, minwidth=0, width=0)
        table.column('#1', stretch=NO, minwidth=0, width=200)
        table.column('#2', stretch=NO, minwidth=0, width=200)
        table.column('#3', stretch=NO, minwidth=0, width=300)
        table.column('#4', stretch=NO, minwidth=0, width=300)
        table.pack()

        def show_att():
    
            if os.path.isfile("Files/Attendance.csv") == True:
                for item in table.get_children():
                    table.delete(item)

                with open('Files/Attendance.csv') as f:
                    reader = csv.DictReader(f, delimiter=',')
                    for row in reader:
                        name = row['Name']
                        att = row['Attendance']
                        date = row['Date']
                        time = row['Time']
                        table.insert("", 0, values=(name, att, date, time))
            table.after(100, show_att)
        
        show_att()

#_____________________________________________________________________________________________________________________________________________________________________________________________________________________
# training the dataset class
class RecordATTPage(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg= "white")

        logo = ImageTk.PhotoImage(Image.open("Files/icon.png"))
        logo_btn = Button(self, text="Attendance", command=lambda : controller.show_frame("HomePage"), font=("Helvetica", 15, "bold"), bd=0, image=logo, bg="white", compound="left", activebackground="white")
        logo_btn.image = logo
        logo_btn.place(x=0,y=0)


        (images, labels, names, id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(datasets):
            for subdir in dirs:
                names[id] = subdir
                subjectpath = os.path.join(datasets, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    label = id
                    images.append(cv2.imread(path, 0))
                    labels.append(int(label))
                id += 1
        
        (width, height) = (1200, 700)
        (images, labels) = [np.array(lis) for lis in [images, labels]]

        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(images, labels)

        def main():
            face_cascade = cv2.CascadeClassifier(haar_file)
            webcam = cv2.VideoCapture(0) # modify for raspberry pi

            if os.path.isfile("Files/Attendance.csv") == False:
                with open('Files/Attendance.csv', "w", newline="") as f:
                    wr = csv.writer(f)
                    wr.writerow(["Name", "Attendance", "Date", "Time"])

            while True:
                (_, im) = webcam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for(x,y,w,h) in faces:
                    cv2.rectangle(im, (x,y), (x+w, y+h), (0,51,255), 3)
                    face = gray[y:y+h, x:x+w]
                    face_resize = cv2.resize(face, (width, height))

                    prediction = model.predict(face_resize)
                    cv2.rectangle(im, (x,y), (x+w, y+h), (0,255,0), 3)

                    if prediction[1]<100:
                        with open('Files/Attendance.csv', "r+", newline="") as f:
                            con = csv.reader(f)
                            for i in con:
                                if (i[0] == names[prediction[0]]) and (i[2] == str(datetime.date.today())):
                                    cv2.putText(im, '%s -Marked Present at %s'%(names[prediction[0]], i[-1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,51,255))
                                    break 
                            else:
                                wr = csv.writer(f)
                                wr.writerow([names[prediction[0]], "Present", datetime.date.today(), datetime.datetime.now().strftime("%I:%M %p")])
                                cv2.putText(im, '%s - Marked Present'%(names[prediction[0]]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,51,255))
                                break

                    else:
                        cv2.putText(im, 'Student Not Recognised', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0,51,255))

                cv2.namedWindow("Taking Attendance", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Taking Attendance", 1200, 800)
                cv2.imshow('Taking Attendance', im)

                key = cv2.waitKey(10)
                if key == 27: # press esc key to stop
                    cv2.destroyAllWindows()
                    break

        start = Button(self, text='Record Attendance', command = main, bg="white", bd=0, fg="red", font=("comic sans ms", 32, "bold"))
        start.place(relx=0.5, rely=0.5, anchor=CENTER)

#____________________________________________________________________________________________________________________________________________________________________
# lets run the app
if __name__ == "__main__":
    app = rootApp()
    app.mainloop() 