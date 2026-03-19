import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getImages } from "../api/image";

const Images = () => {
  const [images, setImages] = useState([]);

  useEffect(() => {
    getImages().then(setImages);
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Images</h1>
      <p>
        <Link to="/">Back to home</Link>
        <Link to="/plot">View Plot</Link>
      </p>
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

export default Images;
