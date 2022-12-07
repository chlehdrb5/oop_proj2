import abc
from membershipEnum import MembershipEnum

class DiscountPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def discount(self, user, price):
        raise NotImplemented

class FixDiscountPolicy(DiscountPolicyInterface):
    discountPrice = 100
    def discount(self, user, price):
        if user["membership"] == MembershipEnum.GOLD.value:
            return FixDiscountPolicy.discountPrice
        return 0

class PercentDiscountPolicy(DiscountPolicyInterface):
    discountPercent = 10
    def discount(self, user, price):
        if user.membership == MembershipEnum.GOLD.value:
            return price * PercentDiscountPolicy.discountPercent // 100
