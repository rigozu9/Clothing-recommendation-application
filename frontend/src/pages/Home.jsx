import { useState, useEffect } from "react";
import api from "../api/api";
import { ping } from "../api/ping";
import { getImages } from "../api/image";

const Home = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [images, setImages] = useState([]);
  const [pong, setPong] = useState("");

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

  useEffect(() => {
    const fetchPing = async () => {
      try {
        const data = await ping();
        setPong(data.message);
      } catch (error) {
        setPong("Virhe yhteydessä backendiin");
      }
    };

    fetchPing();
  }, []);

  useEffect(() => {
    getImages().then(setImages);
  }, []);


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
      <p>{pong}</p>
      <div>
        {images.map((img) => (
          <img
            key={img.image_id}
            src={img.url}
            alt="clothing"
            width="200"
            onError={(e) => {
              e.target.style.display = "none";
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default Home;