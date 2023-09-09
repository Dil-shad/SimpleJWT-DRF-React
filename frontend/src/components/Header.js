import React, { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const Header = () => {
  const { user,logoutUser } = useContext(AuthContext);

  return (
    <div>
      <Link to="/">Home</Link>
      <span> | </span>
      {!user ? (
        <Link to="/login">Login</Link>
      ) : (
        <p className="d-inline" onClick={logoutUser}>Logout</p>
      )}
      <p>user: {user ? user.username : "Guest"}</p>
    </div>
  );
};

export default Header;
