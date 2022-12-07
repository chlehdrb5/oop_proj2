import Navbar from "./Navbar";
import { Outlet } from "react-router-dom";
import { Toaster } from "react-hot-toast";

const Root = () => {
  return (
    <div className="flex-col justify-center">
      <Toaster />
      <Navbar />
      <div className="flex mt-8 justify-center">
        <div className="w-[1024px]">
          <Outlet />
        </div>
      </div>
    </div>
  );
};
export default Root;
