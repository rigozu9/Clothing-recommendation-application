import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../api/user";

const LoginPage = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await loginUser({ username, password });

      localStorage.setItem("user_id", String(res.user_id));
      localStorage.setItem("username", res.username);

      navigate("/images");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-md bg-gray-900/70 border border-gray-700 rounded-2xl shadow-2xl p-8">
        <h1 className="text-3xl font-bold text-center mb-2">Log in</h1>
        <p className="text-gray-400 text-center mb-8">
          Sign in to view your clothing recommendations.
        </p>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-300 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              className="w-full rounded-xl bg-gray-800 border border-gray-700 px-4 py-3 text-white placeholder-gray-400 outline-none focus:border-white"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              className="w-full rounded-xl bg-gray-800 border border-gray-700 px-4 py-3 text-white placeholder-gray-400 outline-none focus:border-white"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full rounded-xl bg-white text-black font-semibold py-3 hover:bg-gray-200 transition"
          >
            Log in
          </button>
        </form>

        {error && (
          <p className="mt-4 text-red-400 text-sm text-center">{error}</p>
        )}

        <p className="mt-6 text-center text-gray-400">
          Don't have an account?{" "}
          <Link to="/register" className="text-white hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;