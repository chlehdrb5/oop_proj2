import RegisterRent from "./RegisterRent";
import RentInfo from "./RentInfo";
import RentList from "./RentList";
import UserInfo from "./UserInfo";
import axios from "axios";
import { useEffect, useState } from "react";
import { Routes, Route, BrowserRouter } from "react-router-dom";

function App() {
  const [itemList, setItemList] = useState([]);
  useEffect(() => {
    (async () => {
      const res = await axios.get("http://127.0.0.1:5000/rent");
      setItemList(res.data);
    })();
  }, []);

  return (
    <div>
      <h1 className="text-2xl mb-4 ml-2">BORROW SHOP 최신 상품들</h1>
      <RentList itemList={itemList} />
    </div>
  );
}

export default App;
