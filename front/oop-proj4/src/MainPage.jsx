import iphone from "./assets/apple-mockup.png";

const MainPage = () => {
  return (
    <div>
      <div className="flex items-center w-full h-full justify-center relative">
        <img src={iphone} width={400} className="rotate-90" />
        <div className="absolute">
          <div className="flex ">
            <div className="text-5xl font-bold space-y-3 flex-col -ml-52">
              <h1>당신 근처의</h1>
              <h1 className="text-orange-400">BORROW SHOP</h1>
              <h4 className="text-lg font-medium text-gray-800">
                필요한 물품을 필요한 만큼만 <br />
                가깝고 따뜻한 당신의 근처를 만들어요.
              </h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
