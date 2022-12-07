import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk as ttk
import tkinter.messagebox as msgbox
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

import abc

class RentDBInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getInfo(self, uuid):
        """
        매개변수로 들어온, uuid 값을 가지는 Rent 정보를 전부 dictionary 형태로, 반환합니다. eg. {title: ..., description: ..., ...}
            param
                uuid: 정보를 가져 오고자 하는 대여 UUID
            return
                Rent 정보가 담긴 dict
        """
        raise NotImplemented

    @abc.abstractmethod
    def createRent(self, newRent):
        """
        매개변수로 들어온, newRent를 DB상에 등록합니다
            param
                newRent: 새로운 대여의 정보를 가지고 있는 dictionary
            return
                True : 저장 성공
                False : 저장 실패
        """
        raise NotImplemented

    @abc.abstractmethod
    def setLender(self, uuid, newLender):
        """
        uuid 값을 PK로 하는 대여항목에 Lender 필드를 갱신합니다
            param
                uuid: 수정하고자 하는 Rent의 uuid
                newLender: 등록하고자 하는 유저의 id(PK)값
            return
                True : 성공
                False : 실패
        """
        raise NotImplemented

    @abc.abstractmethod
    def getRendList(self, Lender):
        """
        Lender 필드의 값이 Lender와 일치하는 모든 Rent 정보들을 리스트에 담아 반환합니다
            param
                Lender: 찾고자 하는 User id(PK)값
            return
                Rent 정보들의 리스트 [{}, {}, ...]
        """
        raise NotImplemented

class MockRentDBImpl(RentDBInterface):
    def getInfo(self, uuid):
        return {
            "UUID": uuid,
            "title": "title",
            "description": "lorem ipsum",
            "deposit": 1000,
            "daily_rent_fee": 100,
            "lender": None,
        }

    def createRent(self, newRent):
        return True

    def setLender(self, uuid, newLender):
        return True

    def getRendList(self, Lender):
        return [{
            "UUID": 0,
            "title": "title",
            "description": "lorem ipsum",
            "deposit": 1000,
            "daily_rent_fee": 100,
            "lender": Lender,
        }, {
            "UUID": 1,
            "title": "title 2",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
            "lender": Lender,
        }]

class UserDBInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getInfo(self, id):
        """
        해당 id 를 가지는 유저 정보를 dict 형태로 반환합니다.
            param
                id 찾고자 하는 유저 id(PK)
            return
                유저 정보가 담긴 dictionary
        """
        raise NotImplemented

    @abc.abstractmethod
    def setPoint(self, id, newPoint):
        """
        해당 id 를 가지는 유저의 point 필드값을 newPoint로 수정합니다
            param
                id: 수정하고자 하는 유저의 id(PK)
                newPoint: point의 수정값
            return
                True: 성공
                False : 실패
        """
        raise NotImplemented

class MockUserDBImpl(UserDBInterface):
    def getInfo(self, id):
        return {
            "id": id,
            "membership": "bronze",
            "point": 10000,
            "trade_cnt": 0
        }

    def setPoint(self, id, newPoint):
        return True






#GUI 메인 창

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.__Product_info_Dict=dict() #사용자가 등록한 상품에 대한 dict
        self.__UUid_to_show=int() # 목록에서 상품을 클릭시 보여줄 상품의 uuid
        self.__UUid_to_rent=int() # 사용자가 대여한 상품의 uuid
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("480x480+500+300")
        self.resizable(False,False)


        self.title_font = tkfont.Font(family='Helvetica', slant="italic")
        self.inf_font=tkfont.Font(family="맑은 고딕",slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (StartPage, Rental_Reg_Page, Loan_app_page,Prod_Info,Rent_info):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.  
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()





    #목록에서 상품을 클릭시 선택된 상품의 uuid에 대한 set() + get()
    def set_UUid_to_show(self,a):
        self.__UUid_to_show=a
    def get_UUid_to_show(self):
        return self.__UUid_to_show

    # 사용자가 등록할 상품에 대한 정보를 담은 딕셔너리에 대한 set() + get()
    def set_dict(self,a):
        
        self.__Product_info_Dict=a.copy()
        #print(self.__Product_info_Dict)
    def get_dict(self):
        return self.__Product_info_Dict
    
    # 사용자가 대여하려고 하는 상품의 uuid set() + get()
    def set_UUid_to_rent(self,a):
        self.__UUid_to_rent=a
    def get_UUid_to_rent(self):
        return self.__UUid_to_rent
        
#첫번째 페이지
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="OOP project 4", font=controller.title_font,width=10,height=5)
        

        info=MockUserDBImpl.getInfo(MockUserDBImpl,id)
        #print(info)
        '''
        "id": id,
            "membership": "bronze",
            "point": 10000,
            "trade_cnt": 0
        '''
        
        info_lf=tk.LabelFrame(self,text="정보")


        id_label=tk.Label(info_lf,text=str("ID : "+str(info["id"])),font=controller.inf_font)####################################
        membership_label=tk.Label(info_lf,text=str("Membership : "+str(info["membership"])),font=controller.inf_font)####################################
        point_label=tk.Label(info_lf,text=str("Point : "+str(info["point"])),font=controller.inf_font)
        trade_cnt_label=tk.Label(info_lf,text=str("Trade count : "+str(info["trade_cnt"])),font=controller.inf_font)

        
        
        #1. 대여등록 버튼
        #Rental registration
        rental_reg_but=tk.Button(self,text="1. 대여등록",width=100,padx=20,pady=10,relief='solid',command=lambda: controller.show_frame("Rental_Reg_Page"))
        

        #2. 대여신청 버튼
        #a loan application
        loan_application_but=tk.Button(self,text="2. 대여신청",width=100,padx=20,pady=10,relief='solid',command=lambda: controller.show_frame("Loan_app_page"))

        #3. 현재 대여 버튼
        #Current rental
        cur_rental_but=tk.Button(self,text="3. 현재대여",width=100,padx=20,pady=10,relief='solid',command=lambda:controller.show_frame("Rent_info"))
        
        

        label.pack(side='top',fill="y")
        
        cur_rental_but.pack(side='bottom')
        loan_application_but.pack(side='bottom')
        rental_reg_but.pack(side='bottom')
        info_lf.pack(side='bottom',fill='both',padx=10,pady=10)
        # info_lf.pack(side='bottom',fill='both',expand=True)
        

        id_label.pack(anchor='w',side="top")
        membership_label.pack(anchor='w',side="top")
        point_label.pack(anchor='w',side="top")
        trade_cnt_label.pack(anchor='w',side="top")


#대여할 상품 등록 페이지
class Rental_Reg_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        welcome_label=tk.Label(self,text="대여할 상품에 대한 정보를 입력해주세요!",font=controller.title_font)
        welcome_label.grid(row=0,columnspan=2)
        
        title_label=tk.Label(self,text="제목 -> ",font=controller.inf_font)####################################
        title_label.grid(row=1,column=0)
        title_entry= tk.Entry(self,width=50)
        title_entry.grid(row=1,column=1,sticky="NEWS")

        description_label=tk.Label(self,text="설명 -> ",font=controller.inf_font)
        description_label.grid(row=3,column=0,sticky="NEWS")
        description_txt=tk.Text(self,width=50,height=10)
        description_txt.grid(row=3,column=1)

        deposit_label=tk.Label(self,text="보증금 -> ",font=controller.inf_font)
        deposit_label.grid(row=4,column=0)
        deposit_entry=tk.Entry(self,width=50)
        deposit_entry.grid(row=4,column=1)

        loan_amount_label=tk.Label(self,text="대여금액 -> ",font=controller.inf_font)
        loan_amount_label.grid(row=5,column=0)
        loan_amount_entry=tk.Entry(self,width=50)
        loan_amount_entry.grid(row=5,column=1)

        rental_date_label=tk.Label(self,text="대여일 -> ",font=controller.inf_font)
        rental_date_label.grid(row=6,column=0)
        rental_date_entry=tk.Entry(self,width=50)
        rental_date_entry.grid(row=6,column=1)

        self.info_dict=dict()

        def btncmd():
            if(title_entry.get()==''):
                msgbox.showerror("에러", "제목을 입력해주세요!!!")
            elif(description_txt.get(1.0)=='\n'):
                msgbox.showerror("에러", "설명을 입력해주세요!!!")
            elif(deposit_entry.get()==''):
                msgbox.showerror("에러", "보증금을 입력해주세요!!!")
            elif(loan_amount_entry.get()==''):
                msgbox.showerror("에러", "대여 금액을 입력해주세요!!!")
            elif(rental_date_entry.get()==''):
                msgbox.showerror("에러", "날짜를 입력해주세요!!!")
            else:
                self.info_dict["Title"]=title_entry.get()
                self.info_dict["Description"]=description_txt.get("1.0","end")
                self.info_dict["Deposit"]=deposit_entry.get()
                self.info_dict["Loan"]=loan_amount_entry.get()
                self.info_dict["Date"]=rental_date_entry.get()
                controller.set_dict(self.info_dict)
                msgbox.showinfo("", "저장됐습니다!")
                #print(controller.get_dict())

                #텍스트 창 비우기
                title_entry.delete(0, "end")
                description_txt.delete('1.0', "end")
                deposit_entry.delete(0, "end")
                loan_amount_entry.delete(0, "end")
                rental_date_entry.delete(0, "end")
                controller.show_frame("StartPage")
                
        save_btn=tk.Button(self,text="SAVE",font=controller.inf_font,command=btncmd)
        save_btn.grid(row=7,columnspan=2,sticky="NEWS")
        
        button_back = tk.Button(self, text="Back",font=controller.inf_font,
                           command=lambda: controller.show_frame("StartPage"))
        button_back.grid(row=8,columnspan=2,sticky="NEWS")
    

#대여 목록(모든 상품 출력 페이지)
class Loan_app_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="대여할 상품을 고르세요", font=controller.title_font)
        label.pack(side="top")# fill="x", pady=10

        scrollbar=tk.Scrollbar(self)
        scrollbar.pack(side="right",fill="y")
        table=ttk.Treeview(self,height=10,columns=[0,1,2,3,4],show="headings",yscrollcommand=scrollbar.set,displaycolumns=[1,2,3,4])
        table.pack()
        
        
        table.column("1", width=100,anchor="center")
        table.heading("1", text="Title")

        table.column("2", width=100, anchor="center")
        table.heading("2", text="Description", anchor="center")

        table.column("3", width=100, anchor="center")
        table.heading("3", text="Deposit", anchor="center")

        table.column("4", width=100, anchor="center")
        table.heading("4", text="Daily rent fee", anchor="center")
        
        scrollbar.config(command=table.yview)
        
        
        # 리스트를 여기에 받았다고 가정
        list_of_products=[{
            "UUID": 55,
            "title": "title",
            "description": "lorem ipsum",
            "deposit": 1000,
            "daily_rent_fee": 100,
        }, {
            "UUID": 1,
            "title": "title 2",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }, {
            "UUID": 2,
            "title": "title 3",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }, {
            "UUID": 3,
            "title": "title 4",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }, {
            "UUID": 4,
            "title": "title 5",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }]


        '''
        이런식으로 list of product에 들어온다고 가정
        {'UUID': 0, 'title': 'title', 'description': 'lorem ipsum', 'deposit': 1000, 'daily_rent_fee': 100}
        {'UUID': 1, 'title': 'title 2', 'description': 'lorem ipsum', 'deposit': 2000, 'daily_rent_fee': 200}
        '''


        temp_list=list()
        for prod_dict in list_of_products:
            temp_list.append(list(prod_dict.values()))

        for val in temp_list:
            table.insert("","end",values=(val),iid=val[0])   

        def selectItem(a):
            selectItem=table.selection()
            controller.set_UUid_to_show(selectItem[0]) ###### 현재 사용자가 보고 있는 상품의 uuid 저장
            #print(controller.get_UUid_to_show())
            controller.show_frame("Prod_Info")
        table.bind('<ButtonRelease-1>', selectItem)


        button = tk.Button(self, text="BACK",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        
#특정 상품페이지
class Prod_Info(tk.Frame):

     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        ############
        
        #받을 dict 이걸로 가정                                              #######
        Product_info={
            "UUID": 55,
            "title": "title",
            "description": "lorem ipsum",
            "deposit": 1000,
            "daily_rent_fee": 100,
        }

        name_of_prod=Product_info['title']
        description=Product_info['description']
        deposit=Product_info['deposit']
        daily_rent_fee=Product_info["daily_rent_fee"]

        ###################### 제목 프레임 설정
        labelf_name=tk.LabelFrame(self,text="제목",font=controller.inf_font)
        labelf_name.pack(side="top",fill='x',pady=10)
        txt_name=tk.Text(labelf_name,height=2,width=2)
        txt_name.insert(1.0,str(name_of_prod))
        txt_name.configure(state='disabled')
        txt_name.pack(fill='both')
        
        ##################### 설명 프레임 설정
        labelf_desc=tk.LabelFrame(self,text="설명",font=controller.inf_font)
        labelf_desc.pack(side="top",fill='x',pady=10)

        txt_box=tk.Text(labelf_desc,height=10)
        txt_box.insert(1.0,str(description))
        txt_box.configure(state='disabled')
        txt_box.pack(fill='both')

        scrollbar=tk.Scrollbar(txt_box)
        txt_box.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right',fill="y")
        scrollbar.config(command=txt_box.yview)

        ##### deposit 프레임 설정
        labelf_deposit=tk.LabelFrame(self,text="보증금",font=controller.inf_font)
        labelf_deposit.pack(side="top",fill='x',pady=10)
        txt_name=tk.Text(labelf_deposit,height=2,width=2)
        txt_name.insert(1.0,str(deposit))
        txt_name.configure(state='disabled')
        txt_name.pack(fill='both')

        #############   daily_rent_fee 프레임 설정
        labelf_name=tk.LabelFrame(self,text="수수료",font=controller.inf_font)
        labelf_name.pack(side="top",fill='x',pady=10)
        txt_name=tk.Text(labelf_name,height=2,width=2)
        txt_name.insert(1.0,str(daily_rent_fee))
        txt_name.configure(state='disabled')
        txt_name.pack(fill='both')

        
        button_back = tk.Button(self, text="Back",font=controller.inf_font,width=6,
                            command=lambda: controller.show_frame("StartPage"))
        button_back.pack(side='bottom',fill='x')

        def btncmd():
            controller.set_UUid_to_rent(Product_info["UUID"])
            controller.show_frame("StartPage")
            #print(controller.get_UUid_to_rent())
        
        button_rent=tk.Button(self,text="빌리기",width=6,font=controller.inf_font,command=btncmd)
        button_rent.pack(side='bottom',fill='x')
        

#사용자 대여 목록 페이지
class Rent_info(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="대여한 상품들입니다", font=controller.title_font)
        label.pack(side="top")# fill="x", pady=10


        scrollbar=tk.Scrollbar(self)
        scrollbar.pack(side="right",fill="y")
        table=ttk.Treeview(self,height=10,columns=[0,1,2,3,4],show="headings",yscrollcommand=scrollbar.set,displaycolumns=[1,2,3,4])
        table.pack()
        
        
        table.column("1", width=100,anchor="center")
        table.heading("1", text="Title")

        table.column("2", width=100, anchor="center")
        table.heading("2", text="Description", anchor="center")

        table.column("3", width=100, anchor="center")
        table.heading("3", text="Deposit", anchor="center")

        table.column("4", width=100, anchor="center")
        table.heading("4", text="Daily rent fee", anchor="center")
        
        scrollbar.config(command=table.yview)
        
        
        # 리스트를 받았다고 가정
        list_of_products=[{
            "UUID": 55,
            "title": "title",
            "description": "lorem ipsum",
            "deposit": 1000,
            "daily_rent_fee": 100,
        }, {
            "UUID": 1,
            "title": "title 2",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }, {
            "UUID": 2,
            "title": "title 3",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }, {
            "UUID": 3,
            "title": "title 4",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }, {
            "UUID": 4,
            "title": "title 5",
            "description": "lorem ipsum",
            "deposit": 2000,
            "daily_rent_fee": 200,
        }]


        temp_list=list()

        for prod_dict in list_of_products:
            temp_list.append(list(prod_dict.values()))

        for val in temp_list:
            table.insert("","end",values=(val),iid=val[0])   


        button = tk.Button(self, text="BACK",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        
        
    
## main
app = SampleApp()

app.mainloop()
