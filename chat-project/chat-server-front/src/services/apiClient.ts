import axios, { CanceledError, AxiosError } from "axios";
console.log(import.meta.env.VITE_BACK_END_ADDRESS);
console.log(import.meta.env.BACK_END_ADDRESS);
export default axios.create({
  baseURL: "api",
});
export { CanceledError, AxiosError };
