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
            user = self.userDB.getInfo(lender)
            prod = self.rentDB.getInfo(rent_item)
            if prod["lender"]: return False
            deposit   = prod["deposit"]
            daily_fee = prod["daily_rent_fee"]
            total_fee = deposit + daily_fee * prod["date"]
            discount  = self.discountPolicy.discount(user, total_fee)
            total_fee = total_fee - discount
            new_point = user["point"] - (total_fee)
            if new_point >= 0:
                self.rentDB.setLender(rent_item, lender)
                self.userDB.setPoint(lender, new_point)
                self.userDB.increaseTradeCnt(lender)
                if user["trade_cnt"] >= 2:
                    self.userDB.setMembership(lender, MembershipEnum.GOLD.value)
                return True
            else:
                print("ERROR need more point")
                return False
        except Exception as e:
            print("예외 발생 ", e)
            print("ERROR")
            return False
