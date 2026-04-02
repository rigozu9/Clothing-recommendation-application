import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white flex items-center justify-center">
      <div className="text-center max-w-xl px-6">
        
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Clothing Recommender
        </h1>

        <p className="text-gray-300 mb-8 text-lg">
          Discover clothing that matches your personal style using AI-powered recommendations.
        </p>

        <div className="flex justify-center gap-4">
          
          <Link
            to="/login"
            className="px-6 py-3 bg-white text-black rounded-lg font-medium hover:bg-gray-200 transition"
          >
            Log in
          </Link>

          <Link
            to="/register"
            className="px-6 py-3 border border-white rounded-lg font-medium hover:bg-white hover:text-black transition"
          >
            Register
          </Link>

        </div>

      </div>
    </div>
  );
};

export default Home;