import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const RentList = ({ itemList }) => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-wrap">
      {itemList.map((item) => (
        <div
          key={item.uuid}
          className="px-4 py-3 border w-[300px] space-y-3 hover:cursor-pointer rounded-md hover:bg-gray-50 mx-2 my-2"
          onClick={() => {
            navigate(`/rentList/${item.uuid}`);
          }}
        >
          <div>
            <span className="text-xl">{item.title}</span>
          </div>
          <div>
            <span className="text-xs text-gray-400">보증금</span>
            <span className="ml-2 text-orange-400">
              {item.deposit.toLocaleString("ko-KR")}원
            </span>
          </div>
          <div>
            <span className="text-xs text-gray-400">일당</span>
            <span className="ml-2 text-orange-300">
              {item.daily_rent_fee.toLocaleString("ko-KR")}원
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RentList;
