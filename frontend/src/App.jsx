import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Images from "./pages/Images";
import PlotComponent from "./pages/Plot";
import RecommendationsPage from "./pages/RecommendationsPage";
import RegisterPage from "./pages/RegisterPage";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/images" element={<Images />} />
        <Route path="/plot" element={<PlotComponent />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;