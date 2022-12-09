import RentList from "./RentList";
import { useEffect, useState } from "react";
import API from "./api";

function App() {
  const [itemList, setItemList] = useState([]);
  useEffect(() => {
    (async () => {
      setItemList(await API.getRentList());
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
