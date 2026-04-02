import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  const username = localStorage.getItem("username");

  const handleLogout = () => {
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");
    navigate("/");
  };

  return (
    <nav className="w-full bg-gray-900 text-white border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

        {/* Left */}
        <div className="flex items-center gap-6">
          <Link to="/images" className="font-semibold text-lg">
            Clothing App
          </Link>
          <Link to="/recommendations" className="text-gray-300 hover:text-white transition">
            Recommendations
          </Link>
        </div>

        {/* Right */}
        <div className="flex items-center gap-4">
          {username && (
            <span className="text-gray-400 text-sm">
              {username}
            </span>
          )}

          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-white text-black rounded-lg hover:bg-gray-200 transition"
          >
            Logout
          </button>
        </div>

      </div>
    </nav>
  );
};

export default Navbar;