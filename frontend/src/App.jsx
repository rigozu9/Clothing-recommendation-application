import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Images from "./pages/Images";
import PlotComponent from "./pages/Plot";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/images" element={<Images />} />
        <Route path="/plot" element={<PlotComponent />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;