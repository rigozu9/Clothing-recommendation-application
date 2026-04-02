import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createUser } from "../api/user";

const RegisterPage = () => {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const res = await createUser({
        username,
        password,
      });

      setMessage(`Created user: ${res.username}`);
      setUsername("");
      setPassword("");

      setTimeout(() => {
        navigate("/login");
      }, 1000);
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white flex items-center justify-center px-6">
      <div className="w-full max-w-md bg-gray-900/70 backdrop-blur-sm border border-gray-700 rounded-2xl shadow-2xl p-8">
        <h1 className="text-3xl font-bold text-center mb-2">Create account</h1>
        <p className="text-gray-400 text-center mb-8">
          Register to start using the clothing recommender.
        </p>

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-300 mb-2">Username</label>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-xl bg-gray-800 border border-gray-700 px-4 py-3 text-white placeholder-gray-400 outline-none focus:border-white"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-300 mb-2">Password</label>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl bg-gray-800 border border-gray-700 px-4 py-3 text-white placeholder-gray-400 outline-none focus:border-white"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full rounded-xl bg-white text-black font-semibold py-3 hover:bg-gray-200 transition"
          >
            Register
          </button>
        </form>

        {message && (
          <p className="mt-4 text-green-400 text-sm text-center">{message}</p>
        )}

        {error && (
          <p className="mt-4 text-red-400 text-sm text-center">{error}</p>
        )}

        <p className="mt-6 text-center text-gray-400">
          Already have an account?{" "}
          <Link to="/login" className="text-white hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;