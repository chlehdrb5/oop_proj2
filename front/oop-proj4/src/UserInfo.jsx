import { useState, useEffect } from "react";
import { AiOutlineUser } from "react-icons/ai";
import classnames from "classnames";
import RentList from "./RentList";
import { toast } from "react-hot-toast";
import API from "./api";

const UserInfo = () => {
  const [userInfo, setUserInfo] = useState({
    id: "hyeseungmoon",
    membership: 0,
    point: 0,
    trade_cnt: 0,
  });
  const [curPoint, setCurPoint] = useState(0);
  const [currentRent, setCurrentRent] = useState([]);

  useEffect(() => {
    (async () => {
      const data = await API.getUserInfo();
      setUserInfo(data);
      setCurPoint(data.point);
      setCurrentRent(await API.getOrderListWithLender());
    })();
  }, []);

  const handleSubmit = async () => {
    API.increaseUserPoint();
    toast.success("1000 포인트를 적립하였습니다!");
    setCurPoint(curPoint + 1000);
  };

  return (
    <div className="w-full px-8 space-y-2">
      <div className="flex items-center space-x-2">
        <AiOutlineUser />
        <span className="uppercase font-semibold text-2xl">{userInfo.id}</span>
      </div>
      <div className="pt-4">
        <span
          className={classnames("text-lg", {
            "text-yellow-700": userInfo.membership == 0,
            "text-yellow-400": userInfo.membership == 1,
          })}
        >
          {userInfo.membership == 0 ? "BRONZE" : "GOLD"}
        </span>
      </div>
      <div>
        <span>거래 횟수</span>
        <span className="ml-2 font-bold">{userInfo.trade_cnt}</span>
      </div>
      <div>
        <span>잔액</span>
        <span className="ml-2 font-bold text-orange-400">
          {curPoint.toLocaleString("ko-KR")}
        </span>
      </div>
      <div className="flex flex-row-reverse pt-2">
        <button
          className="bg-orange-400 px-4 py-3 text-white rounded-xl hover:bg-orange-300"
          onClick={handleSubmit}
        >
          포인트 충전하기
        </button>
      </div>
      <div>
        <div className="space-y-4">
          <span className="text-2xl">현대 대여 목록</span>
          <RentList itemList={currentRent} />
        </div>
      </div>
    </div>
  );
};
export default UserInfo;
