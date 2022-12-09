import { useState } from "react";
import { toast } from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import API from "./api";

const RegisterRent = () => {
  const user_id = "hyeseungmoon";
  const navigate = useNavigate();
  const [newRentInfo, setNewRentInfo] = useState({
    title: "",
    description: "",
    deposit: 0,
    daily_rent_fee: 0,
    owner: user_id,
  });

  const handleSubmit = async () => {
    await API.createRent(newRentInfo());
    toast.success("물품을 성공적으로 등록하였습니다!");
    navigate("/rentList");
  };

  return (
    <div className="w-full px-8 space-y-4">
      <div className="flex justify-between h-10 items-center">
        <label className="w-10">제목</label>
        <input
          type="text"
          className="border ml-2 w-full h-full rounded-sm p-2"
          placeholder="내 제품을 잘 나타낼 수 있는 제목을 지어주세요!"
          onChange={(e) => {
            setNewRentInfo({ ...newRentInfo, title: e.target.value });
          }}
        ></input>
      </div>
      <div>
        <textarea
          type="text"
          className="border rounded-md w-full h-[250px] p-2"
          placeholder="제품의 특징에 대해서 설명해주세요&#10;가품 및 판매금지 품목은 게시가 제한될 수 있어요"
          onChange={(e) => {
            setNewRentInfo({ ...newRentInfo, description: e.target.value });
          }}
        ></textarea>
      </div>

      <div className="flex justify-between">
        <div className=""></div>
        <div className="space-y-4">
          <div className="flex flex-row-reverse items-center">
            원
            <input
              type="number"
              className="border p-1 rounded-md mx-2 w-20"
              onChange={(e) => {
                setNewRentInfo({
                  ...newRentInfo,
                  deposit: e.target.value,
                });
              }}
            ></input>
            <label>보증금</label>
          </div>
          <div>
            <label>일일 대여비</label>
            <input
              type="number"
              className="border p-1 rounded-md mx-2 w-20"
              onChange={(e) => {
                setNewRentInfo({
                  ...newRentInfo,
                  daily_rent_fee: e.target.value,
                });
              }}
            ></input>
            원
          </div>
        </div>
      </div>
      <div className="flex flex-row-reverse pt-2">
        <button
          className="bg-orange-400 px-4 py-3 text-white rounded-xl hover:bg-orange-300"
          onClick={handleSubmit}
        >
          등록하기
        </button>
      </div>
    </div>
  );
};
export default RegisterRent;
