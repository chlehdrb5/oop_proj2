import React, { Children } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { createBrowserRouter, RouterProvider, Route } from "react-router-dom";
import UserInfo from "./UserInfo";
import RegisterRent from "./RegisterRent";
import RentInfo from "./RentInfo";
import Root from "./Root";
import MainPage from "./MainPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        path: "/",
        element: <MainPage />,
      },
      {
        path: "/userInfo",
        element: <UserInfo />,
      },
      {
        path: "/rentList/",
        element: <App />,
      },
      {
        path: "/rentList/:uuid",
        element: <RentInfo />,
      },
      {
        path: "/registerRent",
        element: <RegisterRent />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
