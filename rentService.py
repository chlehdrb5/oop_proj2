import abc
from membershipEnum import MembershipEnum

class RentServiceInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def createRent(self, title, description, deposit, daily_rent_fee, owner):
        raise NotImplemented

class RentServiceImpl(RentServiceInterface):
    def __init__(self, rentDB, userDB, discountPolicy):
        self.rentDB = rentDB
        self.userDB = userDB
        self.discountPolicy = discountPolicy

    def createRent(self, title, description, deposit, daily_rent_fee, owner):
        try:
            self.userDB.getInfo(owner)
            self.rentDB.createRent(
                {
                    "title": title,
                    "description": description,
                    "deposit": deposit,
                    "daily_rent_fee": daily_rent_fee,
                    "owner": owner
                }
            )
        except:
            print("ERROR owner not found!")

    def createOrder(self, lender, rent_item):
        try:
            self.userDB.getInfo(lender)
            self.rentDB.getInfo(rent_item)
            new_point = self.userDB.getInfo(lender)["point"] - (self.rentDB.getInfo(rent_item)["deposit"] - self.discountPolicy.discount(self.userDB.getInfo(lender),
                                                            self.rentDB.getInfo(rent_item)["deposit"]))
            if new_point >= 0:
                self.rentDB.setLender(rent_item, lender)
                self.userDB.setPoint(lender, new_point)
                self.userDB.increaseTradeCnt(lender)

                if self.userDB.getInfo(lender)["trade_cnt"] >= 2:
                    self.userDB.setMembership(lender, MembershipEnum.GOLD.value)
                return True
            else:
                print("ERROR need more point")
                return False
        except:
            print("ERROR")
