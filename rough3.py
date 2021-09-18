import tkinter as tk
from PIL import ImageTk,Image,ImageOps,ImageDraw,ImageFont
from tkinter import ttk,messagebox,filedialog
import mysql.connector
import os
import pandas as pd
import pyqrcode
from pyzbar.pyzbar import decode
import importlib
import cv2
from pyzbar.pyzbar import decode
from threading import Thread
import time
from datetime import datetime,date,timedelta
from tkcalendar import Calendar,DateEntry
from tkcalendar import *

class Main:
    def __init__(self,root):
        self.root=root
        self.root.geometry('1380x790+0+0')
        self.root.resizable(False,False)
        self.root.title('Advanced Student Managment System')
        self.root.configure(bg='white')

        #l________________________Sql commands
        try:
            dbcon = mysql.connector.connect(host='localhost',user='root',password='',database='database5')
            mycur = dbcon.cursor()
            sql = """
                        CREATE TABLE IF NOT EXISTS fees_table (
                            rno int not null primary key auto_increment,
                            id  int not null ,
                            totalf int not null default 100000,
                            tutionf int not null default 70000,
                            devf int not null default 15000,
                            seqf int not null default 10000,
                            examf int not null default 5000,
                            scholarship int not null default 0,
                            onb varchar(100) not null default 'history',
                            paid int not null default 0,
                            rem int not null default 100000,
                            deposite int not null default 0,
                            status varchar(40) not null default 'unknown',
                            foreign key(id) references table7(id)
                        )
                    """
            mycur.execute(sql)
            dbcon.commit()
            dbcon.close()
        except Exception as el:
            print(el)

        ##k  ____________Making container frame
        self.container_frame = tk.Frame(self.root)
        self.container_frame.place(x=0,y=0,relwidth=1,relheight=1)

            # -------------------------------------------------------- #
            #                         Top Frame                        #
            # -------------------------------------------------------- #
        self.top_frame = tk.Frame(self.container_frame,height=125,bg='#000044')

        self.top_frame.pack(side=tk.TOP,fill=tk.X)
        self.text_label = tk.Label(self.top_frame,text="Advanced Student Managment System",font=("Courier","30"),fg='#ffffff',bg='#000044')
        self.text_label.place(x=340,y=40)
            # -------------------------------------------------------- #
            #   f                    Left Frame                        #
            # -------------------------------------------------------- #
        self.left_frame=tk.Frame(self.container_frame,width=140,bg='#003366')
        self.left_frame.place(y=0,x=0,relheight=1)
        self.display = ImageTk.PhotoImage(file='21.png')
        self.img_label=tk.Label(self.left_frame,image=self.display,bd=0,relief=tk.FLAT,compound=tk.LEFT,width=100,bg='#003366')
        self.img_label.place(x=15,y=25)
            # -------------------------------------------------------- #
            #                        RIGHT FRAME                       #
            # -------------------------------------------------------- #
        self.right_frame = tk.Frame(self.container_frame,bg='white')
        self.right_frame.place(x=140,y=130,width=1230,height=700)
            # -------------------------------------------------------- #
            #                     button Images                        #
            # -------------------------------------------------------- #
        self.fees_img= tk.PhotoImage(file=r'smsicon\91.png')
        self.adm_img=ImageTk.PhotoImage(file=r'smsicon\103.png')
        self.atd_img=ImageTk.PhotoImage(file=r'smsicon\102.jpg')
        self.std_img = ImageTk.PhotoImage(file=r'smsicon\13.png')
        self.result_img = ImageTk.PhotoImage(file=r'smsicon\14.png')


        self.adm_btn = tk.Button(self.right_frame,image=self.adm_img,text='Admission & Registration',compound=tk.TOP,bg='#2e3192',width=310,height=200,font=('Gabriola','18'),activebackground='#2e3192',fg='white',activeforeground='white',cursor='hand2',command=self.admission_frame_fun)
        self.adm_btn.grid(row=0,column=0,padx=46,pady=50)

        self.fees_btn = tk.Button(self.right_frame,image=self.fees_img,text='Fees',compound=tk.TOP,bg='#2e3192',width=310,height=200,font=('Gabriola','18'),activebackground='#2e3192',fg='white',activeforeground='white',cursor ='hand2',command=self.fees_frame_fun)
        self.fees_btn.grid(row=0,column=1,padx=46,pady=50)

        self.atd_btn = tk.Button(self.right_frame,image=self.atd_img,text='Attendence Monitoring',compound=tk.TOP,bg='#2e3192',width=310,height=200,font=('Gabriola','18'),activebackground='#2e3192',fg='white',activeforeground='white',cursor="hand2",command=self.attendence_frame_fun)
        self.atd_btn.grid(row=0,column=2,padx=46,pady=50)

        self.std_btn = tk.Button(self.right_frame,image=self.std_img,text='Student Profile',command=self.student_frame_fun,compound=tk.TOP,bg='#2e3192',width=310,height=200,font=('Gabriola','18'),activebackground='#2e3192',cursor='hand2',fg='white',activeforeground='white')
        self.std_btn.grid(row=1,column=0,padx=46,pady=50,sticky=tk.W)

        self.result_btn = tk.Button(self.right_frame,image=self.result_img,text='Result Monitoring\nUpdate',compound=tk.TOP,bg='#2e3192',width=310,height=200,font=('Gabriola','18'),activebackground='#2e3192',fg='white',activeforeground='white',cursor='hand2',command=self.result_monitor_fun)
        self.result_btn.grid(row=1,column=1,padx=46,pady=50)

        self.status_label = tk.Label(self.right_frame,text='Status',bg='pink')
        self.status_label.place(x=858,y=362,width=330,height=200)


            # -------------------------------------------------------- #
            #                   admission_frame fun                    #
            # -------------------------------------------------------- #

    def admission_frame_fun(self):
        admission_frame = tk.Frame(self.root,bg='white')
        admission_frame.place(x=0,y=0,relheight=1,relwidth=1)
        class Admission_class:
            def __init__(self,admission_frame,container_frame):
                self.container_frame=container_frame
                self.file_name=''
                self.admission_frame = admission_frame
                
                #g______________________Create Three frame 
                self.step_one_frame = tk.Frame(self.admission_frame,bg='white')
                self.step_one_frame.place(x=140,y=120,relheight=1,relwidth=1)
            
                self.step_two_frame = tk.Frame(self.admission_frame,bg='green')
                self.step_two_frame.place(x=140,y=120,relheight=1,relwidth=1)

                self.step_three_frame = tk.Frame(self.admission_frame,bg='white')
                self.step_three_frame.place(x=140,y=120,relheight=1,relwidth=1)
                
                # -------------------------------------------------------- #
                #                         top frame                        #
                # -------------------------------------------------------- #
                self.top_frame = tk.Frame(self.admission_frame,bg='#1A1A1D')
                self.top_frame.place(x=140,y=0,height=120,width=1240)
                self.top_label = tk.Label(self.top_frame,text='Registration & Admission',font=("Courier","40"),bg='#1A1A1D',fg='#C3073F')
                self.top_label.pack(pady=30)

                # -------------------------------------------------------- #
                #      u                 left frame                        #
                # -------------------------------------------------------- #
                self.adm_img=ImageTk.PhotoImage(file=r'smsicon/103.png')

                self.left_frame = tk.Frame(self.admission_frame,bg='#C3073F')
                self.left_frame.place(x=0,y=0,relheight=1,width=140)

                        #g________________________Back button
                self.back_btn = tk.Button(self.left_frame,text='\U0001F530 Home',font=("","16"),bg='#C3073F',fg='black',bd=0,relief='flat',activebackground='#C3073F',command=lambda:self.back_fun(self.container_frame),cursor='hand2')
                self.back_btn.place(x=0,y=730,width=140,height=50)

                Thread(target=self.step_one_fun).start()
                step1_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\step1.png')
                step2_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\step2.png')
                step3_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\step3.png')

                self.step_one_btn = tk.Button(self.left_frame,image=step1_img,font=("","30"),bd=0,relief="flat",command=lambda:Thread(target=self.step_one_fun).start(),bg='#c3073f',activebackground='#c3073f',fg='black',activeforeground='black',cursor='hand2')
                self.step_one_btn.image=step1_img
                self.step_one_btn.place(x=0,y=200,relwidth=1)

                self.step_two_btn = tk.Button(self.left_frame,image=step2_img,font=("","30"),bd=0,relief="flat",command=lambda:Thread(target=self.step_two_fun).start(),bg='#c3073f',activebackground='#c3073f',fg='black',activeforeground='black',cursor='hand2')
                self.step_two_btn.image=step2_img
                self.step_two_btn.place(x=0,y=270,relwidth=1)
                
                self.step_three_btn = tk.Button(self.left_frame,image=step3_img,font=("","30"),bd=0,relief="flat",command=lambda:Thread(target=self.step_three_fun).start(),bg='#c3073f',activebackground='#c3073f',fg='black',activeforeground='black',cursor='hand2')
                self.step_three_btn.image=step3_img
                self.step_three_btn.place(x=0,y=340,relwidth=1)

                    # -------------------------------------------------------- #
                    #                     step three frame                     #
                    # -------------------------------------------------------- #
                #a________init fun of admission class | step three

            def step_three_fun(self): 
                self.step_three_frame.tkraise()

                self.tree_frame4=tk.Frame(self.step_three_frame)
                self.tree_frame4.place(x=838,y=100,width=400,height=560)
                self.my_tree4= ttk.Treeview(self.tree_frame4)

                self.tree_scroll4y = tk.Scrollbar(self.tree_frame4,orient="vertical",command=self.my_tree4.yview)
                self.tree_scroll4x = tk.Scrollbar(self.tree_frame4,orient="horizontal",command=self.my_tree4.xview)

                self.my_tree4.place(x=0,y=0,width=400,height=560)

                self.tree_scroll4y.pack(side="right",fill="y")
                self.tree_scroll4x.pack(side="bottom",fill="x")
                self.my_tree4.configure(yscrollcommand=self.tree_scroll4y.set,xscrollcommand=self.tree_scroll4x)

                self.my_tree4['columns']=('regid','name','father','mobile')

                self.my_tree4.column("#0",width=0,stretch=tk.NO)
                self.my_tree4.column("regid",width=60,anchor="w",minwidth=50)
                self.my_tree4.column("name",width=120,anchor="center",minwidth=100)
                self.my_tree4.column("father",width=120,anchor="center",minwidth=100)
                self.my_tree4.column("mobile",width=100,anchor="center",minwidth=100)

                self.my_tree4.heading('#0',text='',anchor="w")
                self.my_tree4.heading("regid",text='Reg.Id',anchor="w")
                self.my_tree4.heading("name",text='Student Name',anchor="center")
                self.my_tree4.heading("father",text='Father name',anchor="center")
                self.my_tree4.heading("mobile",text='Mobile.No',anchor="center")

                self.my_tree4.bind("<ButtonRelease-1>",self.select2table)
                self.tex = '\U0001F578\U0001F578'
                self.regno = tk.Label(self.step_three_frame,text=f'Reg.No   : {self.tex*2} ',bg='white',font=('','15','bold'))
                self.regno.place(x=20,y=10)
                self.name = tk.Label(self.step_three_frame,text=f'Student Name   : {self.tex*3}',bg='white',font=('','13'))
                self.name.place(x=30,y=40)
                self.father = tk.Label(self.step_three_frame,text=f'Father\'s Name   : {self.tex*3}',bg='white',font=('','13'))
                self.father.place(x=30,y=70)
                self.email = tk.Label(self.step_three_frame,text=f'Email Id  : {self.tex*3}',bg='white',font=('','13'))
                self.email.place(x=30,y=100)
                self.image_label = tk.Label(self.step_three_frame)
                self.image_label.place(x=670,y=20,width=120,height=120)

                self.rollno = tk.Label(self.step_three_frame,text=f'Roll No : {self.tex*3}',font=('','13'),bg='white')
                self.rollno.place(x=400,y=40)
                self.brach = tk.Label(self.step_three_frame,text=f'Branch  : {self.tex*3}',font=('','13'),bg='white')
                self.brach.place(x=400,y=70)
                self.section = tk.Label(self.step_three_frame,text=f'Section : {self.tex*3}',font=('','13'),bg='white')
                self.section.place(x=400,y=100)

                self.tool_frame = tk.Frame(self.step_three_frame,bg ='white')
                self.tool_frame.place(x=60,y=170,width=760,height=40)
                self.gen_rollno_btn = tk.Button(self.tool_frame,text='\U00002699 Generate RollNo',font=("Digital-7 Mono","14","bold"),cursor='hand2',command=lambda:Thread(target=self.gen_rollno).start())
                self.gen_rollno_btn.place(x=260,y=0,width=200,height=40)

                self.branch_var=tk.StringVar()
                self.branch_cb = ttk.Combobox(self.tool_frame,justify="center",textvariable=self.branch_var,font=("","14"),cursor='hand2',state='readonly')
                self.branch_cb['values']=('CSE','ME','IT','CIVIL','EEE')
                self.branch_var.set('BRANCH')
                self.branch_cb.place(x=0,y=0,width=120,height=40)
                


                self.sec_var=tk.StringVar()
                self.sec_cb = ttk.Combobox(self.tool_frame,justify="center",textvariable=self.sec_var,font=("","14"),cursor='hand2',state='readonly')
                self.sec_cb['values']=('CSE-A','CSE-B','ME-C','ME-D','IT-E','CIVIL-F','CIVIL-G','EEE-H','EEE-I')
                self.sec_var.set("SECTION")
                self.sec_cb.place(x=120,y=0,width=120,height=40)

                

                self.gen_id_btn = tk.Button(self.tool_frame,text='\U0001F464 Generate Id',font=("Digital-7 Mono","14","bold"),command=lambda: Thread(target=self.gen_id).start())
                self.gen_id_btn.place(x=500,y=0,width=200,height=40)
                self.branch_frame=tk.Frame(self.step_three_frame)
                self.branch_frame.place(x=20,width=800,y=470,height=80)

                self.brach_cse = tk.Label(self.branch_frame,text='CSE',bg='#262626',fg='white',anchor="center",font=("","16","bold"))
                self.brach_me = tk.Label(self.branch_frame,text='ME',bg='#262626',fg='white',anchor="center",font=("","16","bold"))
                self.brach_it = tk.Label(self.branch_frame,text='IT',bg='#262626',fg='white',anchor="center",font=("","16","bold"))
                self.brach_civil = tk.Label(self.branch_frame,text='CIVIL',bg='#262626',fg='white',anchor="center",font=("","16","bold"))
                self.brach_eee = tk.Label(self.branch_frame,text='EEE',bg='#262626',fg='white',anchor="center",font=("","16","bold"))

                self.brach_cse.place(x=0,y=0,width=150,height=30)
                self.brach_me.place(x=160,y=0,width=150,height=30)
                self.brach_it.place(x=320,y=0,width=150,height=30)
                self.brach_civil.place(x=480,y=0,width=150,height=30)
                self.brach_eee.place(x=640,y=0,width=150,height=30)
                print
                self.csv  = tk.Label(self.branch_frame,text=f'{self.tex*2}',anchor="center",font=("","14"))
                self.csv.place(x=0,y=40,width=150,height=40)

                self.mev  = tk.Label(self.branch_frame,text=f'{self.tex*2}',anchor="center",font=("","14"))
                self.mev.place(x=160,y=40,width=150,height=40)

                self.itv  = tk.Label(self.branch_frame,text=f'{self.tex*2}',anchor="center",font=("","14"))
                self.itv.place(x=320,y=40,width=150,height=40)

                self.civ  = tk.Label(self.branch_frame,text=f'{self.tex*2}',anchor="center",font=("","14"))
                self.civ.place(x=480,y=40,width=150,height=40)

                self.eev  = tk.Label(self.branch_frame,text=f'{self.tex*2}',anchor="center",font=("","14"))
                self.eev.place(x=640,y=40,width=150,height=40)

                self.section_frame = tk.Frame(self.step_three_frame)
                self.section_frame.place(x=30,width=800,height=80,y=580)

                self.sec_a = tk.Label(self.section_frame,text='|SEC-A',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=0,y=0,width=75,height=35)
                self.sec_b = tk.Label(self.section_frame,text='SEC-B|',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=75,y=0,width=75,height=35)
                self.sec_c = tk.Label(self.section_frame,text='|SEC-C',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=150,y=0,width=75,height=35)
                self.sec_d = tk.Label(self.section_frame,text='SEC-D|',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=225,y=0,width=75,height=35)
                self.sec_e = tk.Label(self.section_frame,text='SEC-E',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=300,y=0,width=150,height=35)
                self.sec_f = tk.Label(self.section_frame,text='|SEC-F',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=450,y=0,width=75,height=35)
                self.sec_g = tk.Label(self.section_frame,text='SEC-G|',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=525,y=0,width=75,height=35)
                self.sec_h = tk.Label(self.section_frame,text='|SEC-H',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=600,y=0,width=75,height=35)
                self.sec_i = tk.Label(self.section_frame,text='SEC-I|',anchor="center",font=("","16","bold"),bg="#272727",fg='white').place(x=675,y=0,width=75,height=35)
                
                self.av = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.bv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.cv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.dv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.ev = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.fv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.gv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.hv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))
                self.iv = tk.Label(self.section_frame,text=f'{self.tex}',anchor="center",font=("","14"))

                self.av.place(x=0,y=40,width=75,height=35)
                self.bv.place(x=75,y=40,width=75,height=35)
                self.cv.place(x=150,y=40,width=75,height=35)
                self.dv.place(x=225,y=40,width=75,height=35)
                self.ev.place(x=300,y=40,width=150,height=35)
                self.fv.place(x=450,y=40,width=75,height=35)
                self.gv.place(x=525,y=40,width=75,height=35)
                self.hv.place(x=600,y=40,width=75,height=35)
                self.iv.place(x=675,y=40,width=75,height=35)
                Thread(target=self.fetch_1()).start()
                Thread(target=self.step_three_table()).start()
                #a________end of init function | step three


                #a___________init function for |step two
            def step_two_fun(self):
                self.step_two_frame.tkraise()
                #a____________end of init funtion |step two

                #a_________init fun for step one
            def step_one_fun(self):
                self.step_one_frame.tkraise() 
                #g_________________Create a frame for table frame
                self.table_frame=tk.Frame(self.step_one_frame)
                self.table_frame.place(x=710,y=120,width=500,height=500)
                #g____________creat scrollbar
                self.tree_scroll_y = tk.Scrollbar(self.table_frame,orient="vertical")
                self.tree_scroll_x = tk.Scrollbar(self.table_frame,orient="horizontal")
                self.tree_scroll_y.pack(side="right",fill="y")
                self.tree_scroll_x.pack(side="bottom",fill="x")

                top_l = tk.Label(self.step_one_frame,text="Registered Candidate",font=(("Courier","20")),fg='black',bg='#c3073f',anchor="center")
                top_l.place(x=710,y=20,width=500)
                self.search_by_label = tk.Label(self.step_one_frame,text='Search By: ',font=(("Dungeon",'13')),bg='grey',fg='white')
                self.search_by_label.place(x=715,y=70)
                self.search_by_var = tk.StringVar()
                self.cc_box= ttk.Combobox(self.step_one_frame,font=("","12"),textvariable=self.search_by_var,state='readonly',cursor='circle')
                self.cc_box['values']=('name','mobile no','email','date of birth')
                self.search_by_var.set("Search By")
                self.cc_box.place(x=830,y=71,width=100)
                self.cc_entry = tk.Entry(self.step_one_frame,font=("","14"))
                self.cc_entry.place(x=940,y=70,width=150)
                
                self.search_btn = tk.Button(self.step_one_frame,font=("","10"),text='Search',bg='#c3073f',activebackground='#c3073f',activeforeground='black',fg='black')
                self.search_btn.place(x=1100,y=68,width=100)
                #g____________________Style "Treeview"
                self.style = ttk.Style()
                self.style.theme_use("alt")
                self.style.configure("Treeview",rowheight=30,
                    background='#Feffff',
                    forground='black',
                    fieldbackground='#Feffff'    
                        )

                self.style.map('Treeview',background=[('selected','#c3073f')])
                    #g__________________Create tree view
                self.my_tree = ttk.Treeview(self.table_frame,yscrollcommand=self.tree_scroll_y.set,xscrollcommand=self.tree_scroll_x.set)
                self.my_tree.pack(fill="both",expand=1)
                    #g__________________scrollbar configure
                self.tree_scroll_y.configure(command=self.my_tree.yview)
                self.tree_scroll_x.configure(command=self.my_tree.xview)
                    #g__________________define column
                self.my_tree['columns']=('SNo',"Name","Mobile No","Email","Father","Father Mobile Number")
                    #g___________________format our column
                self.my_tree.column("#0",width=0,anchor='w')

                self.my_tree.column("SNo",anchor='w',width=35,minwidth=30)
                self.my_tree.column("Name",anchor="w",width=120,minwidth=100)
                self.my_tree.column("Mobile No",anchor="w",width=120,minwidth=100)
                self.my_tree.column("Email",anchor="w",width=120,minwidth=100)
                self.my_tree.column("Father",anchor="w",width=120,minwidth=100)
                self.my_tree.column("Father Mobile Number",width=120,minwidth=100,anchor="w")
                    #g___________________Create heading
                self.my_tree.heading("#0",text='')
                self.my_tree.heading("SNo",anchor='w',text='S.No')
                self.my_tree.heading("Name",text="Can.. Name",anchor="center")
                self.my_tree.heading("Mobile No",text='Mobile No.',anchor="center")
                self.my_tree.heading("Email",text='Email',anchor="center")
                self.my_tree.heading("Father",text='Father',anchor="center")
                self.my_tree.heading("Father Mobile Number",text='Father Mobile Number',anchor="center")
                self.my_tree['show']='headings'
                    #g__________________Event Binding
                self.my_tree.bind("<ButtonRelease-1>",self.get_cursor)
                    #g___________________Style widget
                self.my_tree.tag_configure('oddrow',background="white")
                self.my_tree.tag_configure('evenrow',background="#dbdbdb")
                    # -------------------------------------------------------- #
                    #              first box  -> canditate detials             #
                    # -------------------------------------------------------- #
                self.first_box = tk.Frame(self.step_one_frame)
                self.first_box.place(x=20,y=20,width=680,height=640)
 
                toplabel = tk.Label(self.first_box,text='Candidate Details',font=(("Courier","20")),fg='black',bg='#c3073f',width=680,anchor="center")
                toplabel.pack()

                        #g_______________________________________Entry boxes 
                #a_______________________Variables   
                self.name_var = tk.StringVar()
                self.cmobile_var = tk.StringVar()
                self.gender_var = tk.StringVar()
                self.dob_var = tk.StringVar()
                self.cemail_var = tk.StringVar()
                self.img_url_var=tk.StringVar()
                self.father_var = tk.StringVar()
                self.mother_var = tk.StringVar()
                self.fmobile_var = tk.StringVar()
                #a______________________________
                self.full_name_var = tk.StringVar()
                self.address_line1_var = tk.StringVar()
                self.city_var = tk.StringVar()
                self.post_var = tk.StringVar()
                self.pincode_var = tk.StringVar()
                self.district_var = tk.StringVar()
                self.state_var = tk.StringVar()
                self.checkbutton_var=tk.IntVar()
                #g__________________________________
                name = tk.Label(self.first_box,text='Candidate Name:',font=("","13",'bold'))
                name.place(x=5,y=60)
                self.name_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.name_var)
                self.name_entry.place(x=150,y=60)

                mobile = tk.Label(self.first_box,text='Cand.. Mobile No:',font=("","13",'bold'))
                mobile.place(x=5,y=100)
                self.mobile_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.cmobile_var)
                self.mobile_entry.place(x=150,y=100)

                gender = tk.Label(self.first_box,text='Gender:',font=("","13",'bold'))
                gender.place(x=5,y=140)
                self.gender_entry = ttk.Combobox(self.first_box,font=("","13"),textvariable=self.gender_var,state='readonly',cursor='hand2')
                self.gender_entry.place(x=150,y=140,width=100)
                self.gender_var.set("Select")
                self.gender_entry['values']=('Male','Female','Other')

                dob = tk.Label(self.first_box,text='D.O.B',font=("","13",'bold'))
                dob.place(x=5,y=190)
                self.dob_entry=tk.Entry(self.first_box,font=("","13"),textvariable=self.dob_var)
                self.dob_entry.place(x=150,y=190)
                self.dob_var.set('eg:d/m/y')

                email = tk.Label(self.first_box,text="Cand.. Email:",font=("","13",'bold'))
                email.place(x=5,y=230)
                self.email_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.cemail_var)
                self.email_entry.place(x=150,y=230)

                father =tk.Label(self.first_box,text='Father\'s Name:',font=("","13",'bold'))
                father.place(x=360,y=60)
                self.father_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.father_var)
                self.father_entry.place(x=490,y=60)

                mother = tk.Label(self.first_box,text='Mother\'s Name:',font=("","13",'bold'))
                mother.place(x=360,y=100)
                self.mother_entry = tk.Entry(self.first_box,font=('','13'),textvariable=self.mother_var)
                self.mother_entry.place(x=490,y=100)

                father_mob = tk.Label(self.first_box,text='Father Mobile:',font=('','13','bold'))
                father_mob.place(x=360,y=140)
                self.father_mob_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.fmobile_var)
                self.father_mob_entry.place(x=490,y=140)

                cand_img=tk.Label(self.first_box,text='Upload Photo:',font=("","13",'bold'))
                cand_img.place(x=5,y=270)

                self.cand_img_url = tk.Entry(self.first_box,font=("","13"),textvariable=self.img_url_var,state='readonly')
                self.cand_img_url.place(x=150,y=270,width=100)
                
                self.select_btn = tk.Button(self.first_box,text='SELECT',font=("","10"),command=self.select_fun,cursor='hand2')
                self.select_btn.place(x=260,y=267)

                hline = tk.Label(self.first_box,text='',bg='black')
                hline.place(height=1,x=0,y=310,relwidth=1)

                add1 = tk.Label(self.first_box,text='Correspondence Address',font=("","15",'bold'),bg='grey')
                add1.place(width=680,height=20,x=0,y=310)

                full_name = tk.Label(self.first_box,text="Full Name:",font=('',"13","bold"))
                full_name.place(x=5,y=335)
                self.full_name_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.full_name_var)
                self.full_name_entry.place(x=110,y=335,width=222)

                address_line1 = tk.Label(self.first_box,text='Address Line 1:',font=("","13","bold"))
                address_line1.place(x=5,y=375)
                self.address_line1_entry = tk.Entry(self.first_box,font=('','13'),textvariable=self.address_line1_var)
                self.address_line1_entry.place(x=25,y=400,width=300)

                desc_label = tk.Label(self.first_box,text='house no.| floor no. | bulding name | street name | Area Name',font=("","8",'italic'))
                desc_label.place(x=30,y=425)

                city = tk.Label(self.first_box,text='City:',font=("","13","bold"))
                city.place(x=5,y=445)
                self.city_entry = tk.Entry(self.first_box,font=('','13'),textvariable=self.city_var)
                self.city_entry.place(x=150,y=445)

                post = tk.Label(self.first_box,text='Post Office:',font=("","13","bold"))
                post.place(x=5,y=485)
                self.post_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.post_var)
                self.post_entry.place(x=150,y=485)

                pincode = tk.Label(self.first_box,text="Pincode:",font=("","13","bold"))
                pincode.place(x=360,y=335)
                self.pincode_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.pincode_var)
                self.pincode_entry.place(x=490,y=335)

                district = tk.Label(self.first_box,text='District:',font=('',"13",'bold'))
                district.place(x=360,y=375)
                self.district_entry = tk.Entry(self.first_box,font=('',"13",'bold'),textvariable=self.district_var)
                self.district_entry.place(x=490,y=375)

                state = tk.Label(self.first_box,text="State:",font=("","13","bold"))
                state.place(x=360,y=415)
                self.state_entry = tk.Entry(self.first_box,font=("","13"),textvariable=self.state_var)
                self.state_entry.place(x=490,y=415)

                self.conform_checkbox = tk.Checkbutton(self.first_box,text='Conform to Provided All Information is correct',onvalue=1,offvalue=0,variable=self.checkbutton_var,cursor='hand2',takefocus=0,selectcolor='#c3073f',activebackground='#c3073f')
                self.conform_checkbox.place(x=370,y=470)
                    #g_______________________________________________
                bottom_hline = tk.Label(self.first_box,text='',bg='black')
                bottom_hline.place(x=0,y=570,relwidth=1,height=1)
                    #h______________________________________________
                self.register_btn = tk.Button(self.first_box,text="Register",font=("","13",'bold'),bg='#c3073f',activebackground='#c3073f',command=self.register_fun,cursor='hand2')
                self.register_btn.place(x=530,y=585,width=130,height=40)

                bottom_hline2 = tk.Label(self.first_box,text='',bg='black')
                bottom_hline2.place(x=0,y=520,relwidth=1,height=1)

                self.update_btn = tk.Button(self.first_box,text='Update',font=("","13"),bg='grey',fg='white',activebackground='grey',activeforeground='white',command=self.update_fun,cursor='hand2')
                self.update_btn.place(x=5,y=530,width=130,height=30)

                self.clear_btn = tk.Button(self.first_box,text='Clear',font=('',"13"),bg='grey',fg='white',activebackground='grey',activeforeground='white',command=self.clear_fun,cursor='hand2')
                self.clear_btn.place(x=140,y=530,width=130,height=30)

                self.delete_btn = tk.Button(self.first_box,text='Delete',font=('','13'),bg='grey',fg='white',activebackground='grey',activeforeground='white',command=self.delete_fun,cursor='hand2')
                self.delete_btn.place(x=275,y=530,width=130,height=30)
                Thread(target=self.fetch_data()).start()
                #a_______end of init function step one
        
            #a__method for addmission class | step three

            def step_three_table(self):
                try:
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon.cursor()
                    sql = """CREATE  TABLE if not exists seat_allotment(
                        id int primary key not null,
                        foreign key(id) references table7(id),
                        rollno int,
                        branch varchar(15),
                        sec varchar(15),
                        erp varchar(20),
                        id_img_url varchar(200)
                    )"""
                    mycur.execute(sql)
                    dbcon.close()
                except Exception as es:
                    print(es)
            def fetch_1(self):
                try:
                    for row in self.my_tree4.get_children():
                        self.my_tree4.delete(row)

                    print("data is fetched")
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon.cursor()
                    sql = "SELECT id,cnmae,father,cmobile,cemail,img_url FROM table7"
                    mycur.execute(sql)
                    data = mycur.fetchall()
                    
                    dbcon.close()
                    count=0
                    for row in data:
                        self.my_tree4.insert(parent='',iid=count,text='',index="end",values=(row[0],row[1],row[2],row[3],row[4],row[5]))
                        count+=1
                    print("insert int table completed")
                except Exception as es:
                    print("this is exception")
                    print(es)
            def clear_sec_branch(self):
                self.branch_var.set("BRANCH")
                self.sec_var.set("SECTION")
            def select2table(self,e):
                self.clear_sec_branch()
                try:
                    selected = self.my_tree4.focus()
                    values = self.my_tree4.item(selected,'values')

                    self.regno.config(text=f"Reg.No   : {values[0]}")
                    self.name.config(text=f"Student Name   : {values[1]}")
                    self.father.config(text=f"Father\'s Name   : {values[2]}")
                    self.email.config(text=f"Email Id   : {values[4]}")
                    images = ImageTk.PhotoImage(file=values[5])
                    self.image_label.config(image=images)
                    self.image_label.image=images
                    self.id=int(values[0])
                    self.nm = values[1]
                except Exception as es:
                    print(es)
                try:
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon.cursor()
                    sql="""insert into seat_allotment(id)
                            select * from(select %s as id) as temp
                            where not exists(
                                select id from seat_allotment where id=%s
                            )limit 1
                        """    
                    
                                                 #adsjkf"""""""
                    req_tuple = (self.id,self.id)
                    mycur.execute(sql,req_tuple)
                    dbcon.commit()
                    dbcon.close()
                except Exception as ex:
                    print(ex)                
                try:
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon.cursor()
                    sql = "SELECT * FROM seat_allotment WHERE id=%s"
                    tup =(self.id,)
                    mycur.execute(sql,tup)
                    data = mycur.fetchall()
                    dbcon.close()
                    print(data)
                    self.id_img_url = data[0][5]
                    self.rollno_= data[0][1]
                    if self.rollno_!=None:
                        self.rollno.config(text=f'Roll No   : {data[0][1]}')
                        self.section.config(text=f"Section   : {data[0][3]}")
                        self.brach.config(text=f'Branch   : {data[0][2]}')
                    else:
                        self.rollno.config(text=f'Roll No   : {self.tex*3}')
                        self.section.config(text=f'Section   : {self.tex*3}')
                        self.brach.config(text=f'Branch   : {self.tex*3}')
                except Exception as ex:
                    print(ex)
            #a
            def gen_rollno(self):
                if self.branch_var.get()=='BRANCH' or self.sec_var.get()=='SECTION':
                    print("001")
                    messagebox.showinfo("SHOW INFO",f"Please Select SECTION AND BRANCH for {self.nm} ")
                else:
                    try:
                        print("002")
                        dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        mycur = dbcon.cursor()
                        mycur.execute("select rollno from seat_allotment where id =%s",(self.id,))
                        ed=mycur.fetchall()
                        
                        dbcon.close()
                        
                        if ed[0][0] == None:
                            s = self.sec_var.get().split('-')
                            l=s[1]
                            print(l)
                            self.roll_no = 20240000+self.id
                            tu =(self.roll_no,self.branch_var.get(),l,self.id)
                            dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                            mycur = dbcon.cursor()

                            sql = "update seat_allotment set rollno=%s,branch=%s,sec=%s where id=%s"
                            print("step3")
                            mycur.execute(sql,tu)
                            dbcon.commit()
                            dbcon.close
                            try:
                                self.rollno.config(text=f'Roll No   : {self.roll_no}')
                                self.section.config(text=f"Section   : {self.sec_var.get()}")
                                self.brach.config(text=f"Branch   : {self.branch_var.get()}")
                            except:
                                pass
                            messagebox.showinfo("STEP-3",f"Hi.. {self.nm} Your Rollno : {self.roll_no} generate \n ")   
                        else:
                            
                            print("0003")
                            messagebox.showinfo("STEP-3",f"{self.nm} Your Rollno :{ed[0][0]} is already created !")

                    except:
                        pass
                
            
                
                pass
            def gen_id(self):
                self.select2table(1)
                if self.rollno_!=None:
                    if self.id_img_url !=True:
                        self.path=os.path.join(os.getcwd()+"\id_card",self.nm)
                        try:
                            os.makedirs(self.path)
                            #,exist_ok = True
                            print(self.path)

                            rt = (self.id,)
                            dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                            mycur = dbcon.cursor()
                            sql="""
                                select cnmae,sec,rollno,branch,cmobile,father,mother,cemail,dob,img_url
                                from table7 join seat_allotment on table7.id=seat_allotment.id where table7.id=%s  
                            """          """"""
                            mycur.execute(sql,rt)
                            data=mycur.fetchall()
                            print(data)
                            box=(32,125,152,245)
                            im = Image.open(data[0][9])
                            im.resize((120,120))
                            bigsize = (im.size[0]*3,im.size[1]*3)
                            mask = Image.new('L',bigsize,0)
                            draw = ImageDraw.Draw(mask)
                            draw.ellipse((0,0)+bigsize,fill=255)
                            mask =mask.resize(im.size,Image.ANTIALIAS)
                            im.putalpha(mask)
                            output = ImageOps.fit(im,mask.size,centering=(0.5,0.5))
                            output.putalpha(mask)
                            template = Image.open('id2.png')
                            template.paste(im,box,im)
                            
                            qrdata = data[0][2]
                            qrsize = 185
                            qrbox2 = (408,307,593,492)
                            qrbox = (408,310)
                            qr = pyqrcode.create(qrdata)
                            # qr.png(self.path+"\\"+self.nm+"qr"+'.png',scale=6)
                            r = os.path.join(self.path.strip(),self.nm.strip()+'s.png')
                            qr.png(r,scale=6)
                            print(r)
                            imqr = Image.open(r)
                            # imqr = Image.open(self.path+"\\"+self.nm+"qr"+'.png')
                            template.paste(imqr,qrbox)
                            draw_text = ImageDraw.Draw(template)
                            # (112,181)(112,304)(112,327)(112,349)(112,372)(112,395)()
                            # (482,35)(482,58)(482,81)
                            # (443,104)(443,127)(443,149)
                            # (462,171)
                            draw_text.text((112,281),data[0][0],fill='black')
                            draw_text.text((112,304),data[0][1],fill='black')
                            draw_text.text((112,327),str(data[0][2]),fill='black')
                            draw_text.text((112,349),str(data[0][3]),fill='black')
                            draw_text.text((112,372),'Not Avilable',fill='black')
                            draw_text.text((112,395),'Not Avilable',fill='black')

                            draw_text.text((482,35),str(data[0][4]),fill='black')
                            draw_text.text((482,58),str(data[0][5]),fill='black')
                            draw_text.text((482,81),str(data[0][6]),fill='black')
                            draw_text.text((443,104),str(data[0][7]),fill='black')
                            draw_text.text((443,127),'Not Avilable',fill='black')
                            draw_text.text((443,149),str(data[0][8]),fill='black')
                            draw_text.text((462,171),'Not Avilable',fill='black')
                            template.show()
                            template.save(self.path+'\\'+self.nm.strip()+'.png')
                            # template.save()
                            messagebox.showinfo("STEP-3",f"{self.nm} Id Card Created !")
                        except Exception as ef:
                            print(ef)
                            messagebox.showinfo("STEP-3 ",f"{self.nm} Id Card is Already Created !")
                    else:
                        messagebox.showinfo(f"STEP-3",f"{self.nm} Id Already Generated !")    
                else:
                    messagebox.showinfo("STEP-3","Create Rollno Then Create Id Card")    
            

                
            #a___end of method of admission class | step three



            #a_ method for step one
            def back_fun(self,frame):
                frame.tkraise()
                #a________________________Fetch Data
            def fetch_data(self):
                self.my_tree.delete(*self.my_tree.get_children())
                dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                mycursor=dbcon.cursor()
                sql ="""SELECT cnmae,cmobile,cemail,father,fmobile FROM table7"""
                mycursor.execute(sql)
                self.my_data=mycursor.fetchall()
                count=0
                for record in self.my_data:
                    if count%2==0:
                        self.my_tree.insert(parent='',index='end',iid=count,text='',values=(count+1,record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',))
                    else:
                        self.my_tree.insert(parent='',index='end',iid=count,text='',values=(count+1,record[0],record[1],record[2],record[3],record[4]),tags=('oddrow'))
                    count+=1

                
                dbcon.close()
                #a_________________________Get cursor
            def get_cursor(self,e):
                try:
                    row = self.my_tree.focus()    ##>get iid value
                    record = self.my_tree.item(row)     ##>fetch dictonary by iid
                    data = record['values']         #>> Fetch values key 
                    self.register_btn['state']='disabled'
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycursor = dbcon.cursor()
                    sql = "SELECT * FROM table7 WHERE cnmae=%s or cmobile=%s"
                    filter_data = (data[1],data[2])
                    mycursor.execute(sql,filter_data)
                    result = mycursor.fetchone()
                    dbcon.close()
                    self.id = result[0]
                    self.name_var.set(result[3]), 
                    self.cmobile_var.set(result[4]), 
                    self.gender_var.set(result[5]), 
                    self.dob_var.set(result[6]), 
                    self.cemail_var.set(result[7]), 
                    self.img_url_var.set(result[11]),
                    self.father_var.set(result[8]), 
                    self.mother_var.set(result[9]), 
                    self.fmobile_var.set(result[10]) 
                except:
                    pass
                #g_____________________update Function
                
            def update_fun(self):
                try:
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycursor = dbcon.cursor()
                    self.tuple2=(
                    self.name_var.get(), 
                    self.cmobile_var.get(), 
                    self.gender_var.get(), 
                    self.dob_var.get(), 
                    self.cemail_var.get(), 
                    self.father_var.get(), 
                    self.mother_var.get(), 
                    self.fmobile_var.get(),
                    
                    self.id              
                        )
                    sql = "UPDATE table7 SET cnmae=%s,cmobile=%s,gender=%s,dob=%s,cemail=%s,father=%s,mother=%s,fmobile=%s  WHERE id=%s"
                    mycursor.execute(sql,self.tuple2)
                    dbcon.commit()
                    dbcon.close()
                    
                    self.clear_fun()
                    Thread(target=self.fetch_data()).start()
                except Exception as ls:
                    pass
                #g___________________delete funtion

            def delete_fun(self):
                self.register_btn['state']='active'
                try:

                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycursor = dbcon.cursor()
                    sql = "DELETE FROM table7 WHERE id=%s"
                    mycursor.execute(sql,(self.id,))
                    dbcon.commit()
                    dbcon.close()
                    self.clear_fun()
                    self.fetch_data()
                except Exception as ss:
                    pass

            
                #g______________________Select Function
            
            def select_fun(self):
                self.file_path = filedialog.askopenfilename(initialdir=os.getcwd(),title='Select Photo',filetypes=(('Image File','*.jpg'),('All Files','*.*')))
                if self.file_path =='':
                    self.image_url='file path not find'
                    self.img_url_var.set(self.image_url)                    
                    pass
                else:
                    
                    self.file_name=f"{self.name_var.get()}{self.cemail_var.get()}.jpg"
                    if os.path.exists('student_image') == False:
                        os.mkdir('student_image')
                    self.new_file_path=os.path.join(os.getcwd(),f'student_image\{self.file_name}')
                    print(self.new_file_path)
                    self.img_url_var.set(self.new_file_path)
                        

                # -------------------------------------------------------- #
                #                     register Funtion                     #
                # -------------------------------------------------------- #

            def register_fun(self):
                
                if self.file_name=='':
                    pass
                else:
                    self.image = Image.open(self.file_path)
                    try:
                        width,height=self.image.size

                        if width > height:
                            print("first Okay 1")
                            print(width)
                            k = width-height
                            left=k/2
                            top= 0 
                            right= width-k/2
                            bottom= height
                            self.crop_image = self.image.crop((left,top,right,bottom))
                            self.new_image = self.crop_image.resize((120,120))
                            print("second Okay")
                            self.new_image.save(self.new_file_path)
                            self.new_image.show()
                            print("Okay")
                        else:
                            print("First Okay")
                            k = height-width
                            left= 0
                            top= k/2
                            right= width
                            bottom= height -k/2
                            self.crop_image = self.image.crop((left,top,right,bottom))
                            self.new_image = self.crop_image.resize((120,120))
                            self.new_image.save(self.new_file_path) 
                            self.new_image.show()  
                            print("Okay")             

                    except:
                        pass


                self.tuple=(
                self.name_var.get(), 
                self.cmobile_var.get(), 
                self.gender_var.get(), 
                self.dob_var.get(), 
                self.cemail_var.get(), 
                self.father_var.get(), 
                self.mother_var.get(), 
                self.fmobile_var.get(),
                self.new_file_path               
                )
                    #a_____________________Create database
                try:
                    dbcon=mysql.connector.connect(host='localhost',user='root',password='')
                    mycursor = dbcon.cursor()
                    sql = "CREATE DATABASE IF NOT EXISTS database5"
                    mycursor.execute(sql)
                    dbcon.commit()
                    dbcon.close()
                except Exception as es:
                    print(es)
                finally:
                    pass
                    #a______________________Create table
                try:
                    dbcon=mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycursor = dbcon.cursor()
                    sql = """CREATE TABLE IF NOT EXISTS table7 (
                        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        cdate date,
                        ctime time,
                        cnmae varchar(30),
                        cmobile varchar(20),
                        gender varchar(10),
                        dob varchar(10),
                        cemail varchar(30),
                        father varchar(30),
                        mother varchar(30),
                        fmobile varchar(20),
                        img_url varchar(200)

                        )"""
                    mycursor.execute(sql)
                    dbcon.commit()
                    dbcon.close()
                except Exception as es:
                    print(es)
                finally:
                    pass
                
                
                    #a________Insert data into function
                try:
                    dbcon=mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycursor = dbcon.cursor()

                    sql="INSERT INTO table7(cdate,ctime,cnmae,cmobile,gender,dob,cemail,father,mother,fmobile,img_url) VALUES(curdate(),curtime(),%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    mycursor.execute(sql,self.tuple)                    
                    dbcon.commit()
                    dbcon.close() 
                except Exception as es:
                    print('himanshu'+str(es))                  
                self.clear_fun()
                self.fetch_data()
                # -------------------------------------------------------- #
                #                       clear Funtion                      #
                # -------------------------------------------------------- #
            def clear_fun(self):
                try:
                    self.register_btn['state']='active'
                except:
                    pass
                self.name_var.set(""), 
                self.cmobile_var.set(""), 
                self.gender_var.set("Select"), 
                self.dob_var.set("eg:d/m/y"), 
                self.cemail_var.set(""), 
                self.img_url_var.set(""),
                self.father_var.set(""), 
                self.mother_var.set(""), 
                self.fmobile_var.set("") 
                
                #a______________________________
        admission_obj = Admission_class(admission_frame,self.container_frame)

            # -------------------------------------------------------- #
            #                      fees_frame_fun                      #
            # -------------------------------------------------------- #

    def fees_frame_fun(self):
        fees_frame = tk.Frame(self.root,bg='#ebf2ea')
        fees_frame.place(x=0,y=0,relheight=1,relwidth=1)
        class Fees_class:
            def __init__(self,fees_frame,container_frame):
                self.fees_frame = fees_frame
                self.container_frame=container_frame


                self.top_frame = tk.Frame(self.fees_frame,bg='#c0334d')
                self.top_frame.place(x=140,y=0,relwidth=1,height=120)


                top_label = tk.Label(self.top_frame,text='Fees Management',font=("Courier","45",""),bg='#c0334d',fg='black')
                top_label.place(x=320,y=20)


                self.left_frame = tk.Frame(self.fees_frame,bg='#d6618f')
                self.left_frame.place(x=0,y=0,width=140,relheight=1)


                self.right_frame = tk.Frame(self.fees_frame,bg='white')
                self.right_frame.place(x=140,y=120,relheight=1,relwidth=1)

                self.back_btn = tk.Button(self.left_frame,text='\U0001F530 Home',font=("","16"),bg='#d6618f',activebackground='#d6618f',command=lambda:self.back_fun(self.container_frame)).place(x=0,y=730,width=140)
                
                paid_btn = tk.Button(self.right_frame,text='PAID',font=("","15"),cursor='hand2')
                paid_btn.place(x=890,y=90,width=100,height=30)
                unpaid_btn = tk.Button(self.right_frame,text='UNPAID',font=("","15"),cursor='hand2')
                unpaid_btn.place(x=990,y=90,width=100,height=30)
                all_btn = tk.Button(self.right_frame,text='  ALL  ',font=("","15"),cursor='hand2')
                all_btn.place(x=1090,y=90,width=100,height=30)
                
                self.tree_frame = tk.Frame(self.right_frame)
                self.tree_frame.place(x=840,y=130,width=400,height=538)
                self.my_tree1 = ttk.Treeview(self.tree_frame)

                self.tree_scroll = tk.Scrollbar(self.tree_frame,orient="vertical",command=self.my_tree1.yview)
                self.tree_scroll.pack(side="right",fill="y")

                self.my_tree1.place(x=0,y=0,width=400,height=538)
                self.my_tree1.configure(yscrollcommand=self.tree_scroll.set)
                self.my_tree1['columns']=('Reg.no','Student Name',"Fees Status")

                
                self.my_tree1.column("#0",width=0,stretch="no")
                self.my_tree1.column("Reg.no",width=30,anchor='w')
                self.my_tree1.column("Student Name",width=140,anchor = "w")
                self.my_tree1.column("Fees Status",width=120,anchor = "w")


                self.my_tree1.heading("#0",text='')
                self.my_tree1.heading("Reg.no",text='Reg.no',anchor='w')
                self.my_tree1.heading("Student Name",text="Student Name")
                self.my_tree1.heading("Fees Status",text="Fees Status")
                self.my_tree1.bind("<ButtonRelease-1>",self.select_record)
          

                self.reg_no = tk.Label(self.right_frame,text="Reg.No : ",font=("","17","underline"),bg='white')
                self.reg_no.place(x=20,y=10)
                self.reg_no_box = tk.Label(self.right_frame,text='__________',font=("","17"),bg='white')
                self.reg_no_box.place(x=160,y=10)

                self.name = tk.Label(self.right_frame,text="Student Name :",font=("","13","bold"),bg='white')
                self.name.place(x=20,y=50)
                self.name_box = tk.Label(self.right_frame,text="__________",font=("","13"),bg='white')
                self.name_box.place(x=160,y=50)

                self.email = tk.Label(self.right_frame,text='Student Email : ',font=("","13","bold"),bg='white')
                self.email.place(x=390,y=50)
                self.email_box = tk.Label(self.right_frame,text="___________",font=("","13"),bg='white')
                self.email_box.place(x=530,y=50)

                self.father = tk.Label(self.right_frame,text='Father\'s Name :',font=("","13","bold"),bg='white')
                self.father.place(x=20,y=90)
                self.father_box = tk.Label(self.right_frame,text="__________",font=("","13"),bg='white')
                self.father_box.place(x=160,y=90)

                self.mobile = tk.Label(self.right_frame,text='Mobile No :',font=("","13","bold"),bg='white')
                self.mobile.place(x=390,y=90)
                self.mobile_box = tk.Label(self.right_frame,text="___________",font=("","13"),bg='white')
                self.mobile_box.place(x=530,y=90)

                self.image_label = tk.Label(self.right_frame)
                self.image_label.place(x=700,y=5,width=120,height=120)

                self.fees_frame = tk.Frame(self.right_frame,bg='#e0e0e0')
                self.fees_frame.place(x=10,y=130,width=820,height=300)

                self.fees_status = tk.Label(self.fees_frame,text='Fees Status :',font=("","13","bold"),bg='#e0e0e0')
                self.fees_status.place(x=5,y=5)
                self.fees_status_box = tk.Label(self.fees_frame,text="",font=("","13"),bg='#e0e0e0')
                self.fees_status_box.place(x=120,y=5)

                hline =tk.Label(self.fees_frame,text='',bg='black')
                hline.place(x=0,y=35,relwidth=1,height=1)

                self.fees = tk.Label(self.fees_frame,text='Total Fees  |  Tution Fees  |  Devlopment Fees  |  Institute Security  |  Exam Charge  ',font=("","13"),bg='#e0e0e0')
                self.fees.place(x=10+80,y=40)


                self.total_fees_box_var = tk.StringVar()
                self.tution_fees_box_var = tk.StringVar()
                self.development_fees_box_var = tk.StringVar()
                self.inst_security_fees_box_var = tk.StringVar()
                self.exam_fees_box_var = tk.StringVar()
                self.scholarship_box_var = tk.IntVar()
                self.onb_var = tk.StringVar()


                self.total_fees_box = tk.Entry(self.fees_frame,textvariable = self.total_fees_box_var,bg='pink',bd='1',selectbackground='pink',selectforeground='black',relief='groove',justify='center',state='readonly',font=("","12"))
                self.total_fees_box.place(x=10+80,y=70,width=92,height=30)


                self.tution_fees_box = tk.Entry(self.fees_frame,textvariable = self.tution_fees_box_var,bg='pink',bd='1',selectbackground='pink',selectforeground='black',relief='groove',justify='center',state='readonly',font=("","12"))
                self.tution_fees_box.place(x=102+80,y=70,width=113,height=30)

                self.development_fees_box = tk.Entry(self.fees_frame,textvariable = self.development_fees_box_var,bg='pink',bd='1',selectbackground='pink',selectforeground='black',relief='groove',justify='center',state='readonly',font=("","12"))
                self.development_fees_box.place(x=213+80,y=70,width=149,height=30)

                self.inst_security_fees_box = tk.Entry(self.fees_frame,textvariable = self.inst_security_fees_box_var,bg='pink',bd='1',selectbackground='pink',selectforeground='black',relief='groove',justify='center',state='readonly',font=("","12"))
                self.inst_security_fees_box.place(x=363+80,y=70,width=148,height=30)

                self.exam_fees_box = tk.Entry(self.fees_frame,textvariable = self.exam_fees_box_var,bg='pink',bd='1',selectbackground='pink',selectforeground='black',relief='groove',justify='center',state='readonly',font=("","12"))
                self.exam_fees_box.place(x=511+80,y=70,width=120,height=30)

                self.edit_btn = tk.Button(self.fees_frame,text='@edit fees str',bg='#e0e0e0',fg='green',activebackground='white',activeforeground='green',bd=0,relief="flat",font=("","12"))
                self.edit_btn.place(x=713,y=78)


                self.total_fees_box_var.set('0000')
                self.tution_fees_box_var.set('000')
                self.development_fees_box_var.set('000')
                self.inst_security_fees_box_var.set('000')
                self.exam_fees_box_var.set('00000')

                hline =tk.Label(self.fees_frame,text='',bg='black')
                hline.place(x=55,y=105,width=690,height=1)

                self.scholarship_box = tk.Entry(self.fees_frame,font=("","18","bold"),fg='red',justify="center",textvariable=self.scholarship_box_var)
                self.scholarship_box.place(x=90,y=110,width=60,height=40)

                per = tk.Label(self.fees_frame,text='%',font=("","20","bold"),fg='red')
                per.place(x=150,y=110,height=40)
                self.onthe = tk.Entry(self.fees_frame,font=("","13"),fg="red",justify="center",textvariable=self.onb_var)
                self.onthe.place(x=200,y=110,width=250,height=40)
                
                self.apply_btn = tk.Button(self.fees_frame,text='Apply Scholarship',font=("Fixedsys","17"),command=self.apply,bg='#272727',fg='white',activebackground='#272727',activeforeground='white',cursor='hand2')
                self.apply_btn.place(x=470,y=110,height=40)
       
                hline =tk.Label(self.fees_frame,text='',bg='black')
                hline.place(x=0,y=155,relwidth=1,height=1)

                label_g = tk.Label(self.fees_frame,text='Total Fees  |    Paid    |  Remaning  |  Deposit + ',font=("","15","bold"),bg='#272727',fg='white')
                label_g.place(x=91,y=220)

                self.label_h = tk.Label(self.fees_frame,text='100000',font=("","15",""),anchor="center",bg='#272727',fg="#FF652F")
                self.label_h.place(x=91,y=250,width=118)

                self.label_i = tk.Label(self.fees_frame,text='100000',font=("","15",""),anchor="center",bg='#272727',fg='#14A76C')
                self.label_i.place(x=209,y=250,width=95)

                self.label_j = tk.Label(self.fees_frame,text='100000',font=("","15",""),anchor="center",bg='#272727',fg='#FFE400')
                self.label_j.place(x=304,y=250,width=124)
                

                # rs_label = tk.Label(self.fees_frame,text='Rs.',font=("","15"),fg='red')
                # rs_label.place(x=428,width=30,height=30,y=250)
                self.deposite_var = tk.IntVar()
                self.deposit_entry = tk.Entry(self.fees_frame,font=("","15"),justify="center",fg='white',textvariable=self.deposite_var,bg='#272727')
                self.deposit_entry.place(x=428,y=250,width=114,height=30)

                self.deposit_btn = tk.Button(self.fees_frame,text='Deposit +',font=("Fixedsys","15"),bg='red',activebackground='red',activeforeground='black',command=self.deposit_fun,fg='black',cursor='hand2')
                self.deposit_btn.place(x=552,y=220,width=100,height=60)

                Thread(target=self.fetch_data2()).start()
                  
                # self.select_record(10)
            def fetch_data2(self):
                try:
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon.cursor()
                    sql = """ 
                            SELECT  id,cnmae,cemail,cmobile,father,img_url FROM table7;
                        """
                    mycur.execute(sql)
                    mydata = mycur.fetchall()
                    
                    print(mydata)
                except Exception as el:
                    print(el)
                try:
                    dbcon5 = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon5.cursor()
                    sql = "select * from fees_table where id=%s"
                    mycur.execute(sql,(self.reg_num,))

                except:
                    pass
                count=0
                for record in mydata:
                    self.my_tree1.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],'unknown',record[2],record[3],record[4],record[5]))
                    count+=1
            
            def select_record(self,e):
                self.reg_no_box.config(text='')
                self.name_box.config(text='')
                self.email_box.config(text='')
                self.mobile_box.config(text='')
                self.father_box.config(text='')
                # self.image_label.config(text='')

                selected = self.my_tree1.focus()
                data = self.my_tree1.item(selected,'values')
                # print(data)

                self.reg_no_box.config(text=data[0])
                self.name_box.config(text=data[1])
                self.email_box.config(text=data[3])
                self.mobile_box.config(text=data[4])
                self.father_box.config(text=data[5])
                self.reg_num = data[0]

                images = ImageTk.PhotoImage(file=data[6])
                self.image_label.config(image=images)
                self.image_label.image=images

                
                def create_row():

                    try:
                        dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        mycur = dbcon.cursor()
                        sql = """INSERT INTO fees_table (rno,id)
                            SELECT * FROM (SELECT %s as rno, %s as id) as tmp
                            WHERE NOT EXISTS(SELECT id FROM fees_table WHERE id = %s ) LIMIT 1
                            """
                        mycur.execute(sql,('',self.reg_num,self.reg_num))
                        dbcon.commit()
                        dbcon.close()
                        pass
                    except Exception as es:
                        print(es)
                create_row()
                def fees_m():
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur = dbcon.cursor()
                    sql = "select * from fees_table where id=%s"
                    mycur.execute(sql,(self.reg_num,))

                    dbcon.close()
                    fees_data = mycur.fetchall()

                    self.def_fees = fees_data[0][13]
                    self.totalf = fees_data[0][2]
                    self.rem = fees_data[0][10]


                    self.fees_status_box.config(text=fees_data[0][12])
                    self.total_fees_box_var.set(fees_data[0][2])
                    self.tution_fees_box_var.set(fees_data[0][3])
                    self.development_fees_box_var.set(fees_data[0][4])
                    self.inst_security_fees_box_var.set(fees_data[0][5])
                    self.exam_fees_box_var.set(fees_data[0][6])
                    self.scholarship_box_var.set(fees_data[0][7])
                    self.onb_var.set(fees_data[0][8])
                    self.label_h.config(text=fees_data[0][2])
                    self.label_i.config(text=fees_data[0][9])
                    self.label_j.config(text=fees_data[0][10])
                    # self.deposite_var.set(fees_data[0][9])
                    self.deposite_var.set('')
                
                fees_m()    
            def deposit_fun(self):
                if self.deposite_var.get()<=self.rem:
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',database='database5')
                    mycur = dbcon.cursor()
                    sql = "UPDATE fees_table SET paid=(SELECT paid from fees_table WHERE id = %s)+%s,deposite=%s WHERE id = %s" 
                    rdata = (self.reg_num,self.deposite_var.get(),self.deposite_var.get(),self.reg_num)
                    mycur.execute(sql,rdata)
                    dbcon.commit()
                    dbcon.close()

                    dbcon2 = mysql.connector.connect(host='localhost',user='root',password='',database='database5')
                    mycur2 = dbcon2.cursor()
                    sql2 = "UPDATE fees_table SET rem=(SELECT totalf from fees_table where id=%s)-(select paid from fees_table where id=%s) where id=%s"
                    sdata = (self.reg_num,self.reg_num,self.reg_num)
                    mycur2.execute(sql2,sdata)
                    dbcon2.commit()
                    dbcon2.close()
                    
                    self.select_record(10)
                    
                else:
                    pass
                if self.rem==0:
                    dbcon3 = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycur3 = dbcon3.cursor()
                    sql = "UPDATE fees_table set fees_table.status='paid' where id=%s"
                    mycur3.execute(sql,(self.reg_num,))
                    dbcon3.commit()
                    dbcon3.close()
                    self.select_record(10)
            def apply(self):
                dbcon = mysql.connector.connect(host='localhost',user='root',password='',database='database5')
                mycur = dbcon.cursor()
                if self.totalf==self.totalf:
                    per = round((self.scholarship_box_var.get()/100)*self.def_fees,4)
                    print(per)
                    sql = "UPDATE fees_table SET totalf=(SELECT def_fees from fees_table where id=%s)-%s,tutionf=(select def_fees from fees_table where id=%s)-30000-%s,onb=%s,scholarship=%s WHERE id=%s"
                    tdata=(self.reg_num,per,self.reg_num,per,self.onb_var.get(),self.scholarship_box_var.get(),self.reg_num)
                    mycur.execute(sql,tdata)
                    dbcon.commit()
                    dbcon.close()
                else:
                    pass
                self.select_record(10)
                
                pass
            def back_fun(self,frame):
                frame.tkraise()
        Fees_class_object = Fees_class(fees_frame,self.container_frame)

            # -------------------------------------------------------- #
            #                   Attendence Frame fun                   #
            # -------------------------------------------------------- #
    def attendence_frame_fun(self):
        class Atdnc:
            def __init__(self,container_frame,root):
                self.root= root
                self.container_frame = container_frame
                self.attendence_frame = tk.Frame(self.root)
                self.attendence_frame.place(relwidth=1,relheight=1,x=0,y=0)
                Tframe = tk.Frame(self.attendence_frame,bg='grey')
                Tframe.place(x=160,y=0,height=120,relwidth=1)
                Lframe = tk.Frame(self.attendence_frame,bg='lightblue')
                Lframe.place(x=0,y=0,width=160,relheight=1)
 
                back_Button = tk.Button(Lframe,text='\U0001F530 Home',command=lambda : self.back_fun(self.container_frame),font=("","16","bold"),fg='blue',bg='lightblue',activebackground='lightblue',activeforeground='blue',bd=1,relief="flat")
                back_Button.place(x=0,width=160,height=60,y=730)

                secA = tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_a",None,None)).start(),text='\U0001F4C8  Section-A',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secA.place(x=0,y=140,width=160,height=50)

                secB =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_b",None,None)).start(),text='\U0001F4C8  Section-B',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secB.place(x=0,y=200,width=160,height=50)

                secC =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_c",None,None)).start(),text='\U0001F4C8  Section-C',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secC.place(x=0,y=260,width=160,height=50)

                secD =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_d",None,None)).start(),text='\U0001F4C8  Section-D',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secD.place(x=0,y=320,width=160,height=50)

                secE =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_e",None,None)).start(),text='\U0001F4C8  Section-E',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secE.place(x=0,y=380,width=160,height=50)

                secF =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_f",None,None)).start(),text='\U0001F4C8  Section-F',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secF.place(x=0,y=440,width=160,height=50)

                secG =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_g",None,None)).start(),text='\U0001F4C8  Section-G',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secG.place(x=0,y=500,width=160,height=50)

                secH =  tk.Button(Lframe,command=lambda : Thread(target=self.fillTable,args=("sec_h",None,None)).start(),text='\U0001F4C8  Section-H',font=("","15"),bd=0,relief="flat",bg='lightblue',activebackground='lightblue')
                secH.place(x=0,y=560,width=160,height=50)
                Thread(target=self.Sec_CallBack).start()
                Thread(target=self.fillTable,args=("sec_a",None,None)).start()
                Thread(target=self.leftToolBox,args=()).start()
            def Sec_CallBack(self):
                #1220,305,101
                self.Rframe = tk.Frame(self.attendence_frame,bg='blue')
                self.Rframe.place(x=160,y=120,height=57,relwidth=1)
                tk.Label(self.Rframe,text='Name :',font=("","17","bold")).grid(row=0,column=0,padx=5,pady=10)
                self.name_box=tk.Entry(self.Rframe,font=("",17),width=14)
                self.name_box.grid(row=0,column=1,padx=5,pady=12)
                tk.Label(self.Rframe,text='To : ',font=("",17,"bold")).grid(row=0,column=2,padx=5,pady=12)
                self.to_var = tk.StringVar()
                self.to_var.set('2020-11-11')
                self.from_var = tk.StringVar()
                self.from_var.set('2020-11-14')
                self.to_box = tk.Entry(self.Rframe,textvariable=self.to_var,font=("",17),width=10)
                self.to_box.grid(row=0,column=3,padx=5,pady=12)
                to_btn = tk.Button(self.Rframe,command=lambda : Thread(target=self.to_Fun,args=(True,False)).start(),text='\U0001F4C6',font=("",19))
                to_btn.grid(row=0,column=4,padx=5,pady=0)
                tk.Label(self.Rframe,text='From :',font=("",17,"bold")).grid(row=0,column=5,padx=5,pady=12)
                self.from_box = tk.Entry(self.Rframe,textvariable=self.from_var,font=("",17),width=10)
                self.from_box.grid(row=0,column=6,padx=5,pady=12)
                from_btn = tk.Button(self.Rframe,command=lambda : Thread(target=self.to_Fun,args=(False,False)).start(),text='\U0001F4C6',font=("",19))
                from_btn.grid(row=0,column=7,padx=5,pady=0)
                self.pass_sec()
                search_btn = tk.Button(self.Rframe,command=lambda:Thread(target=self.fillTable,args=('',self.to_var.get(),self.from_var.get())).start(),text='\U0001F50D Search',font=("","15"))
                search_btn.grid(row=0,column=8,padx=5,pady=0)
                
                pass
                
            def to_Fun(self,x,y):
                tLevel = tk.Toplevel(self.Rframe,bg='white')
                blank_space="   "
                def okay():
                    if x==True and y==False:
                        print(cal.selection_get())
                        self.to_var.set(cal.selection_get())
                    else:
                        self.from_var.set(cal.selection_get())
                cal = Calendar(tLevel,selectmode="day")
                w = tLevel.winfo_width()
                h = tLevel.winfo_height()
                tLevel.geometry('+700+210')
                ok= tk.Button(tLevel,text=f"\U00002714 select",font=("","16"),activeforeground='green',bd=0,relief="flat",fg='green',command=okay)
                close_btn= tk.Button(tLevel,command=lambda: tLevel.destroy(),text=f"\U0000274C {blank_space*12}",font=("",16),bd=0,relief="flat",fg="red",bg='white',activeforeground='red',activebackground="white")
                close_btn.pack(side="top")
                cal.pack()
                ok.pack(side="bottom",fill="x")
                tLevel.overrideredirect(1)

            def fillTable(self,sec,sd,ed):
                self.sd=sd
                self.ed=ed
                self.sec=sec
                if self.sec!='':
                    self.secx=self.sec
                    self.pass_sec()
                if self.sd ==None and self.ed==None:
                
                    #a__________fetch columns
                    dbc = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mcur = dbc.cursor()
                    sql=f"show columns in {self.sec}"
                    mcur.execute(sql)
                    self.matrix=mcur.fetchall()
                    dbc.close()
                    #a__________formating column
                    self.h_List=[]
                    self.h_List.insert(0,"S.no")
                    countx=0
                    for h in self.matrix:
                        self.h_List.append(h[0].replace('_','-'))
                        countx+=1
                    #a______________fetch attendence data
                    dbc2 = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mcur2 = dbc2.cursor()
                    sql2=f"select * from {self.sec}"
                    mcur2.execute(sql2)
                    self.matrix2=mcur2.fetchall()
                    dbc2.close()
                    #a_________________formating attendenc data
                    count=1
                    self.matrix3=[]
                    for i in self.matrix2: 
                        i=list(i)
                        i.insert(0,count)
                        self.matrix3.append(i)
                        print(i)
                        count+=1
                else:

                    dbcon=mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    cur = dbcon.cursor()
                    cur2 = dbcon.cursor()
                    sql2 =f"show columns from {self.svar.get()}"
                    cur2.execute(sql2)
                    matrix2 = cur2.fetchall()
                    self.h_List =[i[0] for i in matrix2]
                    
                    
                    try:
                        self.sd = int(self.sd.replace('-',"_"))
                        self.ed = int(self.ed.replace('-',"_"))
                        
                    except Exception as ef:
                       print(ef)
                    try:
                        def fun(i):
                            if i in ("id","name","roll_no","tclass","tpresent","tabsent","per"):
                                return i
                            else:
                                try:
                                    i = int(i.replace("_",""))
                                    if self.sd<= i <=self.ed:
                                        
                                        i = str(i)
                                        iList = [j for j in i]
                                        iList.insert(4,"_")
                                        iList.insert(7,"_")
                                        ("attribute insert used")
                                        k = "".join(iList)
                                        print(k)
                                        return(k)
                                    else:
                                        pass
                                except Exception as es:
                                    print(es)

                        sColumnList=[fun(i) for i in self.h_List if fun(i)!=None]
                        sql=f"select "+",".join(sColumnList) +f" from {self.svar.get()}"
                        cur.execute(sql)
                        self.h_List.insert(0,'S.No')
                        matrix2=cur.fetchall()
                        self.matrix3=[]
                        count=1
                        for i in matrix2:
                            j=list(i)
                            j.insert(0,count)
                            self.matrix3.append(j)
                            count+=1
                        print(self.h_List)
                        print(self.matrix3)
                    except Exception as es:
                        print('third me',es)     
                #a___________style treeview
                self.style2 = ttk.Style()   
                self.style2.theme_use("vista")
                self.style2.configure("Treeview",
                    background='white',
                    foreground='red',
                    rowheight=30,
                    filedbackground='white'
                )      
                self.style2.map('Treeview',
                        background=[('selected','red')]
                        )     
                                         
                #a_____table frame
                table_frame = tk.Frame(self.attendence_frame,bg='pink')
                table_frame.place(x=170,y=180,width=1100,height=610)

                #a_____________scrollbar and treeview
                sby = tk.Scrollbar(table_frame,orient="vertical")
                sby.place(x=1080,y=0,height=610)
                sbx = tk.Scrollbar(table_frame,orient="horizontal")
                sbx.place(x=0,y=591,width=1080)

                tbl = ttk.Treeview(table_frame,yscrollcommand=sby.set,xscrollcommand=sbx.set)
                tbl.place(x=0,y=0,width=1080,height=588)

                sbx.config(command=tbl.xview)
                sby.config(command=tbl.yview)
                #a__________tags

                tbl.tag_configure('oddrow',background="white")
                tbl.tag_configure('evenrow',background="lightblue") 
                #a__________define column in treeview
                tbl['columns']=self.h_List
                #a__________define heading 
                count=0
                for head in self.h_List:
                    if count==2 or count==3:
                        tbl.heading(head,text=head,anchor="w")
                    else:
                        tbl.heading(head,text=head,anchor="center")
                count+=1
                tbl['show']='headings'


                #a_______________formating column
                count=0
                for head in self.h_List:
                    if count<2:
                        tbl.column(head,width=45,minwidth=45,anchor="center")
                    elif 1 < count < 4 :
                        tbl.column(head,width=100,minwidth=100,anchor="w")
                    else:
                        tbl.column(head,width=70,minwidth=70,anchor="center")
                    count+=1
                #a____________________inserting data into treeview
                count=0
                self.matrix3.extend(self.matrix3)
                self.matrix3.extend(self.matrix3)
                self.matrix3.extend(self.matrix3)
                
                for row in tbl.get_children():
                    tbl.delete(row)

                for row in self.matrix3:
                    if row[0]%2==0:
                        tbl.insert(parent='',iid=count,index="end",text='',values=row,tags=("evenrow",))
                    else:
                        tbl.insert(parent='',iid=count,index="end",text='',values=row,tags=("oddrow",))
                    count+=1
                
            def leftToolBox(self):
                leftToolBox_frame=tk.Frame(self.attendence_frame,bg='red')
                leftToolBox_frame.place(x=1270,height=610,y=180,width=110)
                # excel_btn = tk.Button(leftToolBox_frame,text='\U0001F4E4',anchor="n",padx=5,fg='green',font=("","50"))
                # excel_btn.place(x=0,y=0,width=110,height=80)

            def searchDate(self):
                
                pass
            def grab(self):
                
                pass
            def pass_sec(self):
                self.svar=tk.StringVar()
                self.s = tk.Entry(self.Rframe,textvariable=self.svar)
                self.svar.set(self.secx)
            def back_fun(self,frame):
                    frame.tkraise()
                
                
                
        Obj_Atdn = Atdnc(self.container_frame,self.root) 
            # -------------------------------------------------------- #
            #                     student_frame_fun                    #
            # -------------------------------------------------------- #

    def student_frame_fun(self):
        student_frame = tk.Frame(self.root,width=1370,height=700,bg='#C4DFE6').place(x=0,y=0,relwidth=1,relheight=1)
        class Student_class:
            def __init__(self,student_frame,container_frame):
                self.container_frame=container_frame
                self.student_frame = student_frame
                    # -------------------------------------------------------- #
                    #                         top frame                        #
                    # -------------------------------------------------------- #
                self.top_frame = tk.Frame(self.student_frame,bg='#17252A')
                self.top_frame.place(x=0,y=0,relwidth=1,height=100)
                self.top_label = tk.Label(self.top_frame,text='Student Profile & Detials',font=("Courier","30"),bg ='#17252A',fg='#ffffff')
                self.top_label.place(x=430,y=30)
                    # -------------------------------------------------------- #
                    #i                left frame  >student Page               #
                    # -------------------------------------------------------- #
                    
                def back_fun(frame):
                    frame.tkraise()
                self.left_frame = tk.Frame(self.student_frame,bg='#2B7A78')
                self.left_frame.place(x=0,y=0,relheight=1,width=140)
                self.back_btn = tk.Button(self.left_frame,text='Back',command=lambda:back_fun(self.container_frame),cursor = "hand2")
                self.back_btn.pack(side=tk.BOTTOM)

                    

                
                    # -------------------------------------------------------- #
                    #                      k right frame                       #
                    # -------------------------------------------------------- #


                    ##>>Creat a mainFrame  #l---------------Lframe
                
                
                self.main_frame = tk.Frame(self.student_frame,bd=0,relief=tk.GROOVE,bg='#FEFFFF')
                #k                 this is adustable
                self.main_frame.place(x=500,y=100,relheight=1,width=870)

                    ##>Creat a Canvas 
                self.my_canvas = tk.Canvas(self.main_frame,bg='#FEFFFF')
                self.my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

                    ##>Add Scroll To the Canvas
                self.my_scrollbar = ttk.Scrollbar(self.main_frame,orient=tk.VERTICAL,command=self.my_canvas.yview,cursor='hand2')
                self.my_scrollbar.pack(side = tk.RIGHT,fill = tk.Y)

                    ##>Configure the canvas
                self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
                self.my_canvas.bind('<Configure>',lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

                    ##>creat second Frame
                self.second_frame = tk.Frame(self.my_canvas,bg='#FEFFFF')
                self.my_canvas.create_window((0,0),window=self.second_frame,anchor=tk.NW)
           
                    # -------------------------------------------------------- #
                    #         lets code on secon window (second_frame)         #
                    # -------------------------------------------------------- #
                class Student_class_2:
                    count_instance = 0 
                    def __init__(self,second_frame,data_tuple,grid_tuple,alter_list):
                        Student_class_2.count_instance+=1
                        self.second_frame=second_frame
                        self.data_tuple = data_tuple
                        self.grid_tuple=grid_tuple
                        self.alter_list=alter_list
                        self.row,self.column = self.grid_tuple
                        
                        self.id,self.cdate,self.ctime,self.cname,self.cmobile,self.gender,self.dob,self.cemail,self.father,self.mother,self.fmobile,self.img_url = self.data_tuple 
                        self.hellowframe()        
                    def hellowframe(self):
                        if self.alter_list==0:
                            self.frame22 = tk.Frame(self.second_frame,width=400,height=200,bg='#cfcfcf')
                            self.frame22.grid(row=self.row,column=self.column,padx=12,pady=5)
                            self.frame22.pack_propagate(0)
                        else:
                            self.frame22 = tk.Frame(self.second_frame,width=400,height=200,bg='#ededed')
                            self.frame22.grid(row=self.row,column=self.column,padx=12,pady=5)
                            self.frame22.pack_propagate(0)

                        def show():
                            im = ImageTk.PhotoImage(file=self.img_url)
                            lc = tk.Label(self.frame22,image=im,bd=0,relief="flat")
                            lc.image=im
                            lc.place(x=4,y=25)
                            
                        show()
                        def des():
                            sec='E'
                            branch='CSE'
                            rollno = '1900330100101'
                            date = self.cdate
                            if self.alter_list==0:
                                hline = tk.Label(self.frame22,text='',bg='black').place(x=0,y=25,relwidth=1,height=1)   
                                branch_label = tk.Label(self.frame22,text=f"Branch: {branch}",bg='#cfcfcf').place(x=2,y=0) 
                                tlabel = tk.Label(self.frame22,text=f"Sec: {sec}",bg='#cfcfcf').place(x=80,y=0)
                                vline = tk.Label(self.frame22,text='',bg='black').place(x=124,y=0,height=25,width=1)
                                rollno= tk.Label(self.frame22,text=f"{rollno}",bg='#cfcfcf').place(x=150,y=0)
                                vline = tk.Label(self.frame22,text='',bg='black').place(x=276,y=0,height=25,width=1)
                                ldate = tk.Label(self.frame22,text=f"R.date: {date}",bg='#cfcfcf').place(x=280,y=0)
                                name = tk.Label(self.frame22,text=f"Name:  {self.cname}",bg="#cfcfcf",font=("Candara Light","12",'bold')).place(x=140,y=28)
                                mobile = tk.Label(self.frame22,text=f"Mobile:  {self.cmobile}",bg="#cfcfcf",font=("Candara Light","12",'bold')).place(x=140,y=50)
                                father = tk.Label(self.frame22,text=f"Father Name: {self.father}",bg="#cfcfcf",font=("Candara Light","12",'bold')).place(x=140,y=72) 
                                mfather = tk.Label(self.frame22,text=f"Fahter Mn:  {self.fmobile}",bg="#cfcfcf",font=("Candara Light","12",'bold')).place(x=140,y=94)       
                                dob = tk.Label(self.frame22,text=f"D.O.B  {self.dob}",bg="#cfcfcf",font=("Candara Light","12",'bold')).place(x=140,y=116)
                                
                                def ex2():
                                    class one:
                                        def __init__(self,name,frame22):
                                            self.frame22=frame22
                                            self.top_label = tk.Toplevel(self.frame22)
                                            self.top_label.geometry('500x500+0+0')
                                            self.name=name
                                            
                                            self.labe = tk.Label(self.top_label,text=self.name).pack()
                                    two = one(self.cname,self.frame22)
                                
                                perf_btn = tk.Button(self.frame22,text='\U0001F680 show Performance',command=ex2,cursor='hand2')
                                perf_btn.place(x=10,y=160)
                                


                            else:
                                hline = tk.Label(self.frame22,text='',bg='black').place(x=0,y=25,relwidth=1,height=1) 
                                branch_label = tk.Label(self.frame22,text=f"Branch: {branch}",bg='#ededed').place(x=2,y=0) 
                                tlabel = tk.Label(self.frame22,text=f"Sec:{sec}",bg='#ededed').place(x=80,y=0)
                                vline = tk.Label(self.frame22,text='',bg='black').place(x=124,y=0,height=25,width=1)
                                rollno = tk.Label(self.frame22,text=f"{rollno}",bg='#ededed').place(x=150,y=0)
                                vline = tk.Label(self.frame22,text='',bg='black').place(x=276,y=0,height=25,width=1)
                                ldate = tk.Label(self.frame22,text=f"R.date: {date}",bg='#ededed').place(x=280,y=0)
                                name = tk.Label(self.frame22,text=f"Name:  {self.cname}",bg="#ededed",font=("Candara Light","12",'bold')).place(x=140,y=28)
                                mobile = tk.Label(self.frame22,text=f"Mobile:  {self.cmobile}",bg="#ededed",font=("Candara Light","12",'bold')).place(x=140,y=50)
                                father = tk.Label(self.frame22,text=f"Father Name: {self.father}",bg="#ededed",font=("Candara Light","12",'bold')).place(x=140,y=72)
                                mfather = tk.Label(self.frame22,text=f"Fahter Mn:  {self.fmobile}",bg="#ededed",font=("Candara Light","12",'bold')).place(x=140,y=94)
                                dob = tk.Label(self.frame22,text=f"D.O.B  {self.dob}",bg="#ededed",font=("Candara Light","12",'bold')).place(x=140,y=116)
                    
                                def ex2():
                                    class One:
                                        def __init__(self,name,frame22):
                                            self.name=name
                                            self.frame22=frame22
                                            self.top_label = tk.Toplevel(self.frame22)
                                            self.top_label.geometry('500x500+0+0')
                                            self.label = tk.Label(self.top_label,text=self.name).pack()
                                    two = One(self.cname,self.frame22)
                                
                                perf_btn = tk.Button(self.frame22,text='\U0001F680 show Performance',command=ex2,cursor='hand2')
                                perf_btn.place(x=10,y=160)
                        des()    

                        # -------------------------------------------------------- #
                        #                make Student_class_2 Object               #
                        # -------------------------------------------------------- #

               
                def xxx(): 
                    for widget in self.second_frame.winfo_children():
                        widget.destroy()
                    dbcon = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                    mycursor = dbcon.cursor()
                    var =self.search_var.get()
                    mycursor.execute("SELECT * FROM table7 WHERE cnmae LIKE '%"+str(self.search_var.get())+"%'")
                    lists = mycursor.fetchall()      
                    rowlen = len(lists)
                    empty_list =[("","","","","","","","","","","",r"C:\Users\himan\Desktop\asms\student_image\danieldaniel@gmial.com.jpg"),("","","","","","","","","","","",r"C:\Users\himan\Desktop\asms\student_image\danieldaniel@gmial.com.jpg")]
                    if rowlen %2 !=0:
                        rowlen=(rowlen//2)+1
                        lists.extend(empty_list) 
                    else:
                        rowlen = rowlen//2+1 
                        lists.extend(empty_list) 

                    grid_tuple =[]
                    for i in range(rowlen):
                        for j in range(2):
                            grid_tuple.append((i,j))

                    alter_list=[]
                    for i in range(rowlen):
                        if i%2==0:
                            alter_list.extend([0,1])
                        else:
                            alter_list.extend([1,0])
                    count=0
                    for k in grid_tuple:
                        Student_class_2_object = Student_class_2(self.second_frame,lists[count],k,alter_list[count])
                        count+=1
                
                #g______________________Operational Button
                self.opr_frame = tk.Frame(self.student_frame,bg='#C4DFE6')
                self.opr_frame.place(x=140,width=360,y=100,relheight=1)
                search_frame = tk.Frame(self.opr_frame,bg="#ed5eb4").place(x=0,y=0,width=360,height=100)    
                self.search_var = tk.StringVar()
                search_box = tk.Entry(search_frame,font=("","13"),bg="#C4DFE6",fg='black',width=30,textvariable=self.search_var,justify="center")
                search_box.place(x=170,y=120,width=300)
                search_btn = tk.Button(search_frame,text='\U0001F30F  Search',bg='#C4DFE6',fg='black',activebackground='#C4DFE6',activeforeground='black',width=10,command=xxx,cursor='hand2')
                search_btn.place(x=280,y=155) 
                cse_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\smsicon\cse.jpg')
                civil_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\smsicon\civil.jpg')
                eee_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\smsicon\eee.png')
                me_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\smsicon\me.jpg')
                it_img = ImageTk.PhotoImage(file=r'C:\Users\himan\Desktop\asms\smsicon\it.jpg')

                self.cse_btn = tk.Button(self.opr_frame,image=cse_img,bd=0,relief="flat",cursor='hand2')
                self.cse_btn.image=cse_img
                self.cse_btn.place(x=0,y=100)  
                self.civil_btn = tk.Button(self.opr_frame,image=civil_img,bd=0,relief="flat",cursor='hand2')
                self.civil_btn.image=civil_img
                self.civil_btn.place(x=0,y=200)  
                self.eee_btn = tk.Button(self.opr_frame,image=eee_img,bd=0,relief="flat",cursor='hand2')
                self.eee_btn.image=eee_img
                self.eee_btn.place(x=0,y=300)  
                self.me_btn = tk.Button(self.opr_frame,image=me_img,bd=0,relief="flat",cursor='hand2')
                self.me_btn.image=me_img
                self.me_btn.place(x=0,y=400)  
                self.it_btn = tk.Button(self.opr_frame,image=it_img,bd=0,relief="flat",cursor='hand2')
                self.it_btn.image=it_img
                self.it_btn.place(x=0,y=500)  
 
                    # -------------------------------------------------------- #
                    #                     call xxx funtion                     #
                    # -------------------------------------------------------- #

                xxx()   
            def after_init_fun(self):
                pass                        
                         #k             Right Frame End
        Student_class_object = Student_class(student_frame,self.container_frame)
            # -------------------------------------------------------- #
            #               result Monitoring and update Funtion       #
            # -------------------------------------------------------- #
    def result_monitor_fun(self):
        result_monitor_frame = tk.Frame(self.root,bg='green')
        result_monitor_frame.place(x=0,y=0,relwidth=1,relheight=1)
        class Result_monitor_class:
            def __init__(self,result_monitor_frame,container_frame):
                self.result_monitor_frame = result_monitor_frame
                self.container_frame=container_frame
                self.back_btn = tk.Button(self.result_monitor_frame,text='Back',command=lambda:self.back_fun(self.container_frame))
                self.back_btn.pack()
                pass
            def back_fun(self,frame):
                frame.tkraise()
        Result_monitor_class_object = Result_monitor_class(result_monitor_frame,self.container_frame)
class Scan(Main):
    def __init__(self):
        super().__init__(root)        
        self.scan_btn = tk.Button(self.container_frame,command=lambda:Thread(target=self.scan).start(),text='\U0001F3A6',font=("","18"),bg='white',activebackground='white')
        self.scan_btn.place(x=1006,y=130)
        self.pause = tk.Button(self.container_frame,text='\U000023F8',font=("","18"),bg='white',activebackground='white').place(x=1070,y=130)
        self.r_Tuple =[("sec_a","A"),("sec_b","B"),("sec_c","C"),("sec_d","D"),("sec_e","E"),("sec_f","F"),("sec_g","G"),("sec_H","H")]
        
        Thread(target=self.addUpdate).start()
        Thread(target=self.updateDate).start()

    def addUpdate(self):
        for tuple_ in self.r_Tuple:
            try:
                dbcon= mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                cur = dbcon.cursor()
                var,var2=tuple_
                sql = f'''
                    insert ignore into {var} (id,name,roll_no)
                    (select seat_allotment.id,cnmae,rollno from table7 join seat_allotment
                        on table7.id=seat_allotment.id where seat_allotment.sec='{var2}'
                    ) '''
                print("sql called")
                cur.execute(sql)
                dbcon.commit()
                dbcon.close()
                pass
            except Exception as es:
                print(es)

    def updateDate(self):
        try:
            d = str(date.today())
            d_ = (d.replace('-','_'))
            dbcon= mysql.connector.connect(host='localhost',user='root',password='',db='database5')
            cur = dbcon.cursor()
            sec_S = ('sec_a','sec_b','sec_c','sec_d','sec_e','sec_f','sec_g','sec_h')
            # sec_S = ('sec_a',)
            for sec in sec_S:
                sql = f"alter table {sec} add column if not exists {d_} text(4)"
                print(sec)
                print("sql called")
                cur.execute(sql)
                dbcon.commit()
            dbcon.close()
            '''
            for sec in sec_S:
                dbcon= mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                cur = dbcon.cursor()
                sql =f"alter table {sec} drop column 2020_11_11"
                cur.execute(sql)
                dbcon.commit()
            dbcon.close()
            '''
        except Exception as es:
            print(es)
          
    def scan(self):

        print("Scan Method is called")
        capture = cv2.VideoCapture(0)
        self.recived_data = None
        while True:
            _, frame = capture.read()
            decoded_data = decode(frame)
            try:
                data=decoded_data[0][0]
                if data != self.recived_data:
                    self.recived_data=data
                    self.rdata=int(self.recived_data)
                    self.td=str(date.today()).replace('-','_')

                    try:
                        dbcon= mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        cur = dbcon.cursor()
                        sql="select sec from seat_allotment where rollno=%s"
                        cur.execute(sql,(self.rdata,))
                        thatSec = cur.fetchone()
                        self.rSec = thatSec[0]
                        self.rSec_ = (thatSec[0],)
                        dbcon.close()
                        print(self.rSec)
                    except Exception as es:
                        print(es)
                    try:
                        # secA=('sec_a','sec_b','sec_c','sec_d','sec_e','sec_f','sec_g','sec_h')
                        # for sec in secA:
                        dbcon= mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        cur = dbcon.cursor()
                        if self.rSec=='A':
                            sql= f"update sec_a set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='B':
                            sql= f"update sec_b set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='C':
                            sql= f"update sec_c set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='D':
                            sql= f"update sec_d set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='E':
                            sql= f"update sec_e set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='F':
                            sql= f"update sec_f set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='G':
                            sql= f"update sec_g set {self.td} ='A' where {self.td} is NULL"
                        elif self.rSec=='H':
                            sql= f"update sec_h set {self.td} ='A' where {self.td} is NULL"
                        else:
                            pass
                        cur.execute(sql)
                        dbcon.commit()
                        dbcon.close()
                        pass
                    except Exception as es:
                        print(es)
                    try:
                        print(self.td)
                        print(self.rdata)
                        dbcon= mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        cur = dbcon.cursor()
                        if self.rSec=='A':
                            print('present funtion is called')
                            sql = f"update sec_a set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='B':
                            sql = f"update sec_b set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='C':
                            sql = f"update sec_c set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='D':
                            sql = f"update sec_d set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='E':
                            sql = f"update sec_e set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='F':
                            sql = f"update sec_f set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='G':
                            sql = f"update sec_g set {self.td} ='P' where roll_no = {self.rdata} "
                        elif self.rSec=='H':
                            sql = f"update sec_h set {self.td} ='P' where roll_no = {self.rdata} "
                        else:
                            pass

                        cur.execute(sql)
                        dbcon.commit()
                        dbcon.close()

                    except Exception as es:
                        print(es)
                    try:
                        dbcon=mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        cur = dbcon.cursor()
                        if self.rSec=='A':
                            sql = f"select * from sec_a where roll_no={self.rdata}"
                        elif self.rSec=='B':
                            sql = f"select * from sec_b where roll_no={self.rdata}"
                        elif self.rSec=='C':
                            sql = f"select * from sec_c where roll_no={self.rdata}"
                        elif self.rSec=='D':
                            sql = f"select * from sec_d where roll_no={self.rdata}"
                        elif self.rSec=='E':
                            sql = f"select * from sec_e where roll_no={self.rdata}"
                        elif self.rSec=='F':
                            sql = f"select * from sec_f where roll_no={self.rdata}"
                        elif self.rSec=='G':
                            sql = f"select * from sec_g where roll_no={self.rdata}"
                        elif self.rSec=='H':
                            sql = f"select * from sec_h where roll_no={self.rdata}"
                        else:
                            pass
                        cur.execute(sql)
                        matrix = cur.fetchone()
                        dbcon.close()
                        self.absent=0
                        self.present=0
                        for item_ in matrix:
                                if item_=='A':
                                    self.absent+=1
                                elif item_=='P':
                                    self.present+=1
                        self.tclass=self.absent+self.present
                        self.per = (self.present/self.tclass)*100
                        print("himanshu raj",self.absent,self.present,self.tclass,self.per)
                        dbcon2 = mysql.connector.connect(host='localhost',user='root',password='',db='database5')
                        cur2 = dbcon2.cursor()
                        if self.rSec=='A':
                            print('present funtion is called')
                            sql2 = f"update sec_a set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='B':
                            sql2 = f"update sec_b set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='C':
                            sql2 = f"update sec_c set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='D':
                            sql2 = f"update sec_d set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='E':
                            sql2 = f"update sec_e set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='F':
                            sql2 = f"update sec_f set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='G':
                            sql2 = f"update sec_g set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        elif self.rSec=='H':
                            sql2 = f"update sec_h set tclass={self.tclass},tpresent={self.present},tabsent={self.absent},per={self.per} where roll_no = {self.rdata} "
                        else:
                            pass
                        cur2.execute(sql2)
                        dbcon2.commit()
                        dbcon2.close()

                        pass
                    except Exception as es:
                        print(es)
                else:
                    print("Your Attendence is Already Recorded !")
            except:
                pass
            cv2.imshow('QR Code Scaner',frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
root = tk.Tk()
obj1 = Main(root)
obj2 = Scan()
root.mainloop()