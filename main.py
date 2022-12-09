from rentDB import RentDBImpl
from userDB import UserDBImpl
from rentService import RentServiceImpl
from discountPolicy import FixDiscountPolicy
from flask_cors import CORS

from flask import Flask, request
from flask_restx import Api, Resource

rentDB = RentDBImpl()
userDB = UserDBImpl()

discountPolicy = FixDiscountPolicy()
rentService = RentServiceImpl(rentDB, userDB, discountPolicy)

userDB.addUser("hyeseungmoon")
userDB.addUser("testUser")
rentDB.createRent({
    "title": "귀걸이 쥬얼리 보관함 정리함",
    "description":
        "코스트코 유기농 루이보스에요! \n하나에 2.5g으로 보리차 끓이듯이 우려먹는 타입이에요 \n저는 많이 끓여서 물통에넣고 물대신 마셨어요 \n \n대용량 밖에 안팔아서 나머지는 당근합니당~ \n유통기한 24년5월26일",
    "deposit": 1000,
    "daily_rent_fee": 100,
    "owner": "testUser"
})

rentDB.createRent({
    "title": "화장품, 크림 (ahc,수려한)",
    "description":
        """
        화장품,크림 팝니다
        전부 새제품 미사용
        미백주름개선 외에는 서비스
        왼쪽,오른쪽 묶음으로 판매중
        
        왼쪽 (4종류:8개) 15000
        오른쪽(2종류:2개) 15000
        
        (왼쪽or오) 전부(왼+오)
        반값택배 17000 / 31000
        집택배 19000 / 32000
        """,
    "deposit": 2000,
    "daily_rent_fee": 400,
    "owner": "testUser"
})

rentDB.createRent({
    "title": "화장품, 크림 (ahc,수려한)",
    "description":
        """
        14k 하트 원터치 귀걸이
        핑크금
        착용안한 새상품~
        택배도 가능요(착불)
        68.000원
        """,
    "deposit": 3000,
    "daily_rent_fee": 400,
    "owner": "testUser"
})


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r'*': {'origins': '*'}})

@api.route("/user", "/user/<string:user_id>")
class User(Resource):
    def get(self, user_id=""):
        if user_id == "":
            return userDB.getUserList()
        return userDB.getInfo(user_id)

    def post(self, user_id):
        userDB.addUser(user_id)
        return True

    def put(self):
        user_id = request.json.get("user_id")
        userDB.setPoint(user_id, userDB.getInfo(user_id)["point"] + 1000)
        return True

@api.route("/rent", "/rent/<int:uuid>")
class Rent(Resource):
    def get(self, uuid=-1):
        if uuid == -1:
            return rentDB.getRentList()
        return rentDB.getInfo(uuid)

    def post(self):
        title = request.json.get("title")
        description = request.json.get("description")
        deposit = int(request.json.get("deposit"))
        daily_rent_fee = int(request.json.get("daily_rent_fee"))
        owner = request.json.get("owner")
        rentService.createRent(title, description, deposit, daily_rent_fee, owner)
        return True

@api.route("/order", "/order/<string:user_id>")
class Order(Resource):
    def get(self, user_id):
        return rentDB.getLendList(user_id)

    def post(self):
        lender = request.json.get("lender")
        rent_item = request.json.get("rent_item")
        rentService.createOrder(lender, rent_item)




if __name__ == "__main__":
    rentDB = RentDBImpl()
    userDB = UserDBImpl()

    discountPolicy = FixDiscountPolicy()
    rentService = RentServiceImpl(rentDB, userDB, discountPolicy)

    while True:
        t = ["모든 대여 목록", "모든 유저 목록", "유저 생성", "대여 생성", "대여 주문"]

        for i in range(len(t)):
            print(i, t[i])

        print("input : ", end="")
        choice = int(input())
        if choice == 0:
            print(*rentDB.RentDB.values(), sep="\n")

        elif choice == 1:
            print(*userDB.users, sep="\n")

        elif choice == 2:
            print("new user id : ", end="")
            new_user = input()
            userDB.addUser(new_user)

        elif choice == 3:
            print("title : ", end="")
            title = input()
            print("description : ", end="")
            description = input()
            print("deposit : ", end="")
            deposit = int(input())
            print("daily rent fee : ", end="")
            daily_rent_fee = int(input())
            print("owner id : ", end="")
            owner_id = input()

            rentService.createRent(title, description, deposit, daily_rent_fee, owner_id)

        elif choice == 4:
            print("lender : ", "")
            lender = input()
            print("rent item uuid : ", end="")
            rent_item = int(input())

            rentService.createOrder(lender, rent_item)

        print()