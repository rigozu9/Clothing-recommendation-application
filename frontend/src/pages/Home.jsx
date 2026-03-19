import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/api";

const Home = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleCreateUser = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/users", {
        username,
        password,
      });

      setMessage(`Created user: ${res.data.username} (id ${res.data.id})`);
      setUsername("");
      setPassword("");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Clothing Recommender</h1>

      <form onSubmit={handleCreateUser}>
        <div>
          <input
            type="text"
            placeholder="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div>
          <input
            type="password"
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit">Create user</button>
      </form>
      <p>{message}</p>
      <p>
        <Link to="/images">Go to images</Link>
      </p>
    </div>
  );
};

export default Home;