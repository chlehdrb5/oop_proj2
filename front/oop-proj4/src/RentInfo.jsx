import { AiOutlineUser } from "react-icons/ai";
import { useState, useEffect } from "react";
import API from "./api";
import { useParams, useNavigate } from "react-router-dom";
import { toast } from "react-hot-toast";

const RentInfo = () => {
  const [loading, setLoading] = useState(true);
  const [rentInfo, setRentInfo] = useState({});
  const { uuid } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      setRentInfo(await API.getRent(uuid));
      setLoading(false);
    })();
  }, []);

  const handleSubmit = async () => {
    await API.createOrder(uuid);
    navigate("/userInfo");
    toast.success("대여 성공!");
  };

  if (loading) return <></>;

  return (
    <div className="w-[700px] px-8 space-y-2">
      <div>
        <span className="text-3xl font-bold">{rentInfo.title}</span>
      </div>
      <div>
        <span className="text-xs text-gray-400">보증금</span>
        <span className="ml-2 text-orange-400">
          {rentInfo.deposit.toLocaleString("ko-KR")}원
        </span>
        <span className="text-xs text-gray-400 ml-4">일당</span>
        <span className="ml-2 text-orange-300">
          {rentInfo.daily_rent_fee.toLocaleString("ko-KR")}원
        </span>
      </div>
      <div className="flex items-center">
        <AiOutlineUser />
        <span className="ml-2 text-gray-500">{rentInfo.owner}</span>
      </div>
      <div>
        <pre>{rentInfo.description}</pre>
      </div>
      <div className="flex flex-row-reverse pt-4">
        <button
          className="bg-orange-400 px-4 py-3 text-white rounded-xl hover:bg-orange-300"
          onClick={handleSubmit}
        >
          대여하기
        </button>
      </div>
    </div>
  );
};

export default RentInfo;
