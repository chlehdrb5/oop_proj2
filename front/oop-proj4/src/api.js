import axios from "axios";

const API_PATH = "http://127.0.0.1:5000";
const user = "hyeseungmoon";

class API {
  async getRentList() {
    const res = await axios.get(`${API_PATH}/rent`);
    return res.data;
  }
  async createRent(newRentInfo) {
    await axios.post(`${API_PATH}/rent`, newRentInfo);
  }
  async getRent(uuid) {
    const res = await axios.get(`${API_PATH}/rent/${uuid}`);
    return res.data;
  }
  async createOrder(uuid) {
    await axios.post(`${API_PATH}/order`, {
      lender: user,
      rent_item: rentInfo.uuid,
    });
  }
  async getUserInfo() {
    const res = await axios.get(`${API_PATH}/user/${user}`);
    return res.data;
  }
  async getOrderListWithLender() {
    const res = await axios.get(`${API_PATH}/order/${user}`);
    return res.data;
  }
  async increaseUserPoint() {
    await axios.put(`${API_PATH}/user`, { user_id: user });
  }
}
export default new API();
