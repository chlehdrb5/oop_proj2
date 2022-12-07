from rentDB import RentDBImpl
from userDB import UserDBImpl
from rentService import RentServiceImpl
from discountPolicy import FixDiscountPolicy
from flask_cors import CORS

from flask import Flask, request
from flask_restx import Api, Resource

rentDB = RentDBImpl()
userDB = UserDBImpl()
userDB.addUser("hyeseungmoon")

discountPolicy = FixDiscountPolicy()
rentService = RentServiceImpl(rentDB, userDB, discountPolicy)

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