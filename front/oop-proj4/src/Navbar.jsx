import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div className="h-20 w-full shadow-md flex justify-center">
      <div className="flex w-[1024px] justify-between items-center">
        <div className="flex items-center justify-between">
          <div className="flex">
            <Link to="/" className="text-orange-400">
              <span className="p-4 text-2xl font-bold text-orange-400">
                BORROW SHOP
              </span>
            </Link>
          </div>
          <div className="p-4">
            <ul className="flex space-x-4 font-semibold">
              <Link to="/" className="text-orange-400">
                메인 페이지
              </Link>
              <Link to="/rentList">전체 대여 목록</Link>
              <Link to="/registerRent">대여 등록하기</Link>
            </ul>
          </div>
        </div>
        <div className="flex font-bold">
          <Link to="/userInfo">내정보 보기</Link>
        </div>
      </div>
    </div>
  );
};
export default Navbar;
