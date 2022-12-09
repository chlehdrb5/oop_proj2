import abc
from membershipEnum import MembershipEnum

class RentServiceInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def createRent(self, title, description, deposit, daily_rent_fee, owner):
        """
        Create Rent object via rentDB.
        """
        raise NotImplemented

    @abc.abstractmethod
    def createOrder(self, lender, rent_item):
        """
        When a lender borrows rent_item, 
        updates the lender's points and membership information.
        """
        raise NotImplemented

class RentServiceImpl(RentServiceInterface):
    def __init__(self, rentDB, userDB, discountPolicy):
        self.rentDB = rentDB
        self.userDB = userDB
        self.discountPolicy = discountPolicy

    def createRent(self, *arg, **kwargs):
        try:
            self.userDB.getInfo(kwargs['owner'])
            self.rentDB.createRent(kwargs)
        except:
            print("ERROR owner not found!")

    def createOrder(self, lender, rent_item):
        try:
            self.userDB.getInfo(lender)
            self.rentDB.getInfo(rent_item)
            discount = self.discountPolicy.discount(self.userDB.getInfo(lender),self.rentDB.getInfo(rent_item)["deposit"])
            new_point = self.userDB.getInfo(lender)["point"] - (self.rentDB.getInfo(rent_item)["deposit"] - discount)
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
        except Exception as e:
            print("예외 발생 ", e)
            print("ERROR")
            return False
