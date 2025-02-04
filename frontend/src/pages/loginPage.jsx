import { Navigate } from "react-router-dom";
import { Link, useNavigate } from "react-router-dom";

const LoginPage = () => {
const navigate = useNavigate()
    const handleLogin = ()=>{
        navigate('/dashboard/pendaftaran')
    }
  return (
    <div className="min-h-screen">
      <div className="flex justify-center items-center min-h-screen">
        <div className="  bg-gray-400 w-3/5 h-96 grid grid-cols-2">
          <div className="flex justify-center items-center">
            <div className="w-64 h-64 bg-white"></div>
          </div>
          <div>
            <h1>Login</h1>
            <input
              type="email"
              placeholder="email"
              className="my-2 rounded-md px-1 w-56"
            />
            <br />
            <input
              type="password"
              placeholder="password"
              className="rounded-md px-1 w-56 mb-2"
            />
            <br />
            <button onClick={handleLogin} className="bg-blue-400 w-56 rounded-md">submit</button>
          </div>
        </div>
      </div>
    </div>
  );
};
 export default LoginPage