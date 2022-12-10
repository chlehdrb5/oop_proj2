import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk as ttk
import tkinter.messagebox as msgbox
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

import abc
from rentDB import RentDBInterface, RentDBImpl
from userDB import UserDBInterface, UserDBImpl
from discountPolicy import FixDiscountPolicy, PercentDiscountPolicy

from membershipEnum import MembershipEnum
from rentService import RentServiceInterface, RentServiceImpl

#GUI 메인 창

class SampleApp(tk.Tk):

    def __init__(self, rent_service,*args, **kwargs):
        self.__Product_info_Dict=dict() #사용자가 등록한 상품에 대한 dict
        self.__UUid_to_show=int() # 목록에서 상품을 클릭시 보여줄 상품의 uuid
        self.__UUid_to_rent=int() # 사용자가 대여한 상품의 uuid
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("480x600+500+300")
        self.resizable(False,False)

        self.rent_service = rent_service
        self.userDB = self.rent_service.userDB
        self.rentDB = self.rent_service.rentDB
        self.id = self.userDB.getUserList()[0]["id"]
        self.info=self.userDB.getInfo(self.id)


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
            # if page_name == "Rental_Reg_Page" or page_name == "Loan_app_page":
            #     frame = F(parent=container, controller=self, rentDB=self.rentDB)    
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
        if page_name != 'Rental_Reg_Page':
            frame.update_(TESTUSER)
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
        
        
        #print(info)
        '''
        "id": id,
            "membership": "bronze",
            "point": 10000,
            "trade_cnt": 0
        '''
        
        info_lf=tk.LabelFrame(self,text="정보")


        self.id_label=tk.Label(info_lf,text=str("ID : "+str(self.controller.info["id"])),font=controller.inf_font)####################################
        self.point_label=tk.Label(info_lf,text=str("Point : "+str(self.controller.info["point"])),font=controller.inf_font)
        self.membership_label=tk.Label(info_lf,text=str("Membership : "+MembershipEnum(self.controller.info["membership"]).name),font=controller.inf_font)####################################
        self.trade_cnt_label=tk.Label(info_lf,text=str("Trade count : "+str(self.controller.info["trade_cnt"])),font=controller.inf_font)

        
        
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
        

        self.id_label.pack(anchor='w',side="top")
        self.point_label.pack(anchor='w',side="top")
        self.membership_label.pack(anchor='w',side="top")
        self.trade_cnt_label.pack(anchor='w',side="top")

    def update_(self, userid):
        userinfo = self.controller.userDB.getInfo(userid)
        self.id_label.configure(        text='ID\t\t: ' + userinfo['id'])
        self.point_label.configure(     text='Point\t\t: ' + str(userinfo['point']))
        self.membership_label.configure(text='Membership\t: ' + MembershipEnum(userinfo['membership']).name)
        self.trade_cnt_label.configure( text='Trade Count\t: ' + str(userinfo['trade_cnt']))


#대여할 상품 등록 페이지
class Rental_Reg_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        welcome_label=tk.Label(self,text="등록할 상품에 대한 정보를 입력해주세요!",font=controller.title_font)
        welcome_label.grid(row=0,columnspan=2)
        
        title_label=tk.Label(self,text="제목",font=controller.inf_font)####################################
        title_label.grid(row=1,column=0)
        title_entry= tk.Entry(self,width=50)
        title_entry.grid(row=1,column=1,sticky="NEWS")

        description_label=tk.Label(self,text="설명",font=controller.inf_font)
        description_label.grid(row=3,column=0,sticky="NEWS")
        description_txt=tk.Text(self,width=50,height=10)
        description_txt.grid(row=3,column=1)

        deposit_label=tk.Label(self,text="보증금",font=controller.inf_font)
        deposit_label.grid(row=4,column=0)
        deposit_entry=tk.Entry(self,width=50)
        deposit_entry.grid(row=4,column=1)

        loan_amount_label=tk.Label(self,text="일일대여비",font=controller.inf_font)
        loan_amount_label.grid(row=5,column=0)
        loan_amount_entry=tk.Entry(self,width=50)
        loan_amount_entry.grid(row=5,column=1)

        rental_date_label=tk.Label(self,text="대여일",font=controller.inf_font)
        rental_date_label.grid(row=6,column=0)
        rental_date_entry=tk.Entry(self,width=50)
        rental_date_entry.grid(row=6,column=1)

        self.info_dict=dict()

        # self.rentDB = controller.rentDB

        def btncmd():
            if(title_entry.get()==''):
                msgbox.showerror("에러", "제목을 입력해주세요!!!")
            elif(description_txt.get(1.0)=='\n'):
                msgbox.showerror("에러", "설명을 입력해주세요!!!")
            elif(deposit_entry.get()=='' or not deposit_entry.get().isdigit()):
                msgbox.showerror("에러", "보증금을 입력해주세요!!!")
            elif(loan_amount_entry.get()=='' or not loan_amount_entry.get().isdigit()):
                msgbox.showerror("에러", "대여 금액을 입력해주세요!!!")
            elif(rental_date_entry.get()=='' or not rental_date_entry.get().isdigit()):
                msgbox.showerror("에러", "날짜를 입력해주세요!!!")
            else:
                self.info_dict["title"]=title_entry.get()
                self.info_dict["description"]=description_txt.get("1.0","end")
                self.info_dict["deposit"]=int(deposit_entry.get())
                self.info_dict["daily_rent_fee"]=int(loan_amount_entry.get())
                self.info_dict["date"]=int(rental_date_entry.get())
                self.info_dict["owner"]=TESTUSER
                controller.set_dict(self.info_dict)
                controller.rent_service.createRent(**self.info_dict)
                # controller.rentDB.createRent(self.info_dict)
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
        self.table=ttk.Treeview(self,height=10,columns=[0,1,2,3,4,5],show="headings",yscrollcommand=scrollbar.set,displaycolumns=[1,2,3,4,5])
        self.table.pack()
        
        
        self.table.column("1", width=100,anchor="center")
        self.table.heading("1", text="Title")

        self.table.column("2", width=100, anchor="center")
        self.table.heading("2", text="Description", anchor="center")

        self.table.column("3", width=100, anchor="center")
        self.table.heading("3", text="Deposit", anchor="center")

        self.table.column("4", width=100, anchor="center")
        self.table.heading("4", text="Daily rent fee", anchor="center")

        self.table.column("5", width=50, anchor="center")
        self.table.heading("5", text="On loan", anchor="center")
        
        scrollbar.config(command=self.table.yview)

        '''
        이런식으로 list of product에 들어온다고 가정
        {'UUID': 0, 'title': 'title', 'description': 'lorem ipsum', 'deposit': 1000, 'daily_rent_fee': 100}
        {'UUID': 1, 'title': 'title 2', 'description': 'lorem ipsum', 'deposit': 2000, 'daily_rent_fee': 200}
        '''

        def selectItem(a):
            selectItem=self.table.selection()
            controller.set_UUid_to_show(selectItem[0]) ###### 현재 사용자가 보고 있는 상품의 uuid 저장
            #print(controller.get_UUid_to_show())
            controller.show_frame("Prod_Info")
        self.table.bind('<ButtonRelease-1>', selectItem)


        button = tk.Button(self, text="BACK",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def update_(self, userid):
        self.list_of_products=self.controller.rentDB.getRentList()
        # print(self.list_of_products)
        self.table.delete(*self.table.get_children()) # reset table
        temp_list=list()
        for prod in self.list_of_products:
            # if self.table.exists(prod['uuid']):
            #     continue
            
            on_loan = 'O' if prod['lender'] else 'X'
            temp_list.append([
                prod['uuid'],
                prod['title'],
                prod['description'],
                prod['deposit'],
                prod['daily_rent_fee'],
                on_loan
                ])

        for val in temp_list:
            self.table.insert("","end",values=(val),iid=val[0])
        self.update()
        
#특정 상품페이지
class Prod_Info(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.product = None

        ###################### 제목 프레임 설정
        labelf_name=tk.LabelFrame(self,text="제목",font=controller.inf_font)
        labelf_name.pack(side="top",fill='x',pady=10)
        self.txt_title=tk.Text(labelf_name,height=2,width=2)

        
        ##################### 설명 프레임 설정
        labelf_desc=tk.LabelFrame(self,text="설명",font=controller.inf_font)
        labelf_desc.pack(side="top",fill='x',pady=10)
        self.txt_box=tk.Text(labelf_desc,height=10)

        scrollbar=tk.Scrollbar(self.txt_box)
        self.txt_box.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right',fill="y")
        scrollbar.config(command=self.txt_box.yview)

        ##### deposit 프레임 설정
        labelf_deposit=tk.LabelFrame(self,text="보증금",font=controller.inf_font)
        labelf_deposit.pack(side="top",fill='x',pady=10)
        self.txt_depo=tk.Text(labelf_deposit,height=2,width=2)


        #############   daily_rent_fee 프레임 설정
        labelf_fee=tk.LabelFrame(self,text="일일대여비",font=controller.inf_font)
        labelf_fee.pack(side="top",fill='x',pady=10)
        self.txt_fee=tk.Text(labelf_fee,height=2,width=2)

        #############   date 프레임 설정
        labelf_date=tk.LabelFrame(self,text="대여일",font=controller.inf_font)
        labelf_date.pack(side="top",fill='x',pady=10)
        self.txt_date=tk.Text(labelf_date,height=2,width=2)

        #############   lender 프레임 설정
        labelf_lender=tk.LabelFrame(self,text="대여중인 사용자",font=controller.inf_font)
        labelf_lender.pack(side="top",fill='x',pady=10)
        self.txt_lender=tk.Text(labelf_lender,height=2,width=2)

        button_back = tk.Button(self, text="Back",font=controller.inf_font,width=6,
                            command=lambda: controller.show_frame("StartPage"))
        button_back.pack(side='bottom',fill='x')


        def btncmd():
            self.controller.set_UUid_to_rent(self.product['uuid'])
            if self.controller.rent_service.createOrder(TESTUSER, self.product['uuid']):
                self.controller.show_frame("StartPage")
            else:
                msgbox.showerror("에러", "포인트가 부족하거나 이미 대여 중인 상품입니다.")
                button_back.invoke()
        
        button_rent=tk.Button(self,text="빌리기",width=6,font=controller.inf_font,command=btncmd)
        button_rent.pack(side='bottom',fill='x')

    def update_(self, userid):
        self.product    = self.controller.rentDB.getInfo(self.controller.get_UUid_to_show())
        name_of_prod    = self.product['title']
        description     = self.product['description']
        deposit         = self.product['deposit']
        daily_rent_fee  = self.product['daily_rent_fee']
        lender          = self.product['lender']
        date            = self.product['date']
        
        self.txt_title.configure(state='normal')
        self.txt_title.delete("1.0", "end")
        self.txt_title.insert(1.0,str(name_of_prod))
        self.txt_title.configure(state='disabled')
        self.txt_title.pack(fill='both')

        self.txt_box.configure(state='normal')
        self.txt_box.delete("1.0", "end")
        self.txt_box.insert(1.0,str(description))
        self.txt_box.configure(state='disabled')
        self.txt_box.pack(fill='both')

        self.txt_depo.configure(state='normal')
        self.txt_depo.delete("1.0", "end")
        self.txt_depo.insert(1.0,str(deposit))
        self.txt_depo.configure(state='disabled')
        self.txt_depo.pack(fill='both')

        self.txt_fee.configure(state='normal')
        self.txt_fee.delete("1.0", "end")
        self.txt_fee.insert(1.0,str(daily_rent_fee))
        self.txt_fee.configure(state='disabled')
        self.txt_fee.pack(fill='both')

        self.txt_date.configure(state='normal')
        self.txt_date.delete("1.0", "end")
        self.txt_date.insert(1.0,str(date))
        self.txt_date.configure(state='disabled')
        self.txt_date.pack(fill='both')

        self.txt_lender.configure(state='normal')
        self.txt_lender.delete("1.0", "end")
        self.txt_lender.insert(1.0,str(lender))
        self.txt_lender.configure(state='disabled')
        self.txt_lender.pack(fill='both')

        self.update()

#사용자 대여 목록 페이지
class Rent_info(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="대여한 상품들입니다", font=controller.title_font)
        label.pack(side="top")# fill="x", pady=10


        scrollbar=tk.Scrollbar(self)
        scrollbar.pack(side="right",fill="y")
        self.table=ttk.Treeview(self,height=10,columns=[0,1,2,3,4],show="headings",yscrollcommand=scrollbar.set,displaycolumns=[1,2,3,4])
        self.table.pack()
        
        
        
        self.table.column("1", width=100,anchor="center")
        self.table.heading("1", text="Title")

        self.table.column("2", width=100, anchor="center")
        self.table.heading("2", text="Description", anchor="center")

        self.table.column("3", width=100, anchor="center")
        self.table.heading("3", text="Deposit", anchor="center")

        self.table.column("4", width=100, anchor="center")
        self.table.heading("4", text="Daily rent fee", anchor="center")
        
        scrollbar.config(command=self.table.yview)
        
        button = tk.Button(self, text="BACK",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def update_(self, userid):
        self.list_of_products=self.controller.rentDB.getLendList(userid)
        # print(self.list_of_products)
        temp_list=list()
        for prod in self.list_of_products:

            if self.table.exists(prod['uuid']):
                continue
            temp_list.append([
                prod['uuid'],
                prod['title'],
                prod['description'],
                prod['deposit'],
                prod['daily_rent_fee'],
                prod['date'],
                prod['lender'],
                ])

        for val in temp_list:
            self.table.insert("","end",values=(val),iid=val[0])
        self.update()

        

if __name__ == "__main__":
    ## main
    global TESTUSER
    TESTUSER = 'test'
    userDB = UserDBImpl()
    rentDB = RentDBImpl()
    policy = FixDiscountPolicy()
    rent_service = RentServiceImpl(rentDB, userDB, policy)
    app = SampleApp(rent_service)
    app.mainloop()
