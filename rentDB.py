import abc

class NotExistedRentError(Exception):
    def __init__(self):
        super.__init__('존재하지 않는 대여 정보입니다.')

class Rent:
    def __init__(self, title, description, deposit, daily_rent_fee, lender, owner, uuid):
        self.uuid = uuid
        self.title = title
        self.description = description
        self.deposit = deposit
        self.daily_rent_fee = daily_rent_fee
        self.lender = lender
        self.owner = owner

    def __repr__(self):
        return str(self.__dict__)

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
    def getLendList(self, Lender):
        """
        Lender 필드의 값이 Lender와 일치하는 모든 Rent 정보들을 리스트에 담아 반환합니다
            param
                Lender: 찾고자 하는 User id(PK)값
            return
                Rent 정보들의 리스트 [{}, {}, ...]
        """
        raise NotImplemented

    @abc.abstractmethod
    def getRentList(self):
        raise NotImplemented

class RentDBImpl(RentDBInterface):
    def __init__(self):
        self.RentDB = {}
        self.rentCnt = 0

    def getInfo(self, uuid):
        if uuid in self.RentDB:
            return self.RentDB[uuid]
        else:
            raise NotExistedRentError

    def createRent(self, newRent):
        newRent["uuid"] = self.rentCnt
        newRent["lender"] = None
        self.RentDB[newRent["uuid"]] = newRent
        self.rentCnt += 1
        return True

    def setLender(self, uuid, newLender):
        if uuid in self.RentDB:
            self.RentDB[uuid]["lender"] = newLender
            return True
        else:
            return False

    def getLendList(self, Lender):
        l = []
        for key in self.RentDB:
            if self.RentDB[key]["lender"] == Lender:
                l.append(self.RentDB[key])
        return l

    def getRentList(self):
        l = []
        for key in self.RentDB:
            l.append(self.RentDB[key])
        return l
