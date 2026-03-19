import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Images from "./pages/Images";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/images" element={<Images />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;