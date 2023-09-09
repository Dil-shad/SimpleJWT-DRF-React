import { createContext, useEffect, useState } from "react";
import jwt_decode from "jwt-decode";
import { useHistory } from "react-router-dom";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  //console.log("Stored Token:", localStorage.getItem("authToken"));

  let [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authToken") ? localStorage.getItem("authToken") : null
  );
  //console.log(authTokens);
  let [user, setUser] = useState(() =>
    localStorage.getItem("authToken")
      ? jwt_decode(JSON.parse(localStorage.getItem("authToken")).access)
      : null
  );

  const [loading, setLoading] = useState(true);

  const history = useHistory();

  let loginUser = async (e) => {
    e.preventDefault();

    let response = await fetch("http://127.0.0.1:8000/api/token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: e.target.username.value,
        password: e.target.password.value,
      }),
    });
    let data = await response.json();

    // console.log("fetch " + JSON.stringify(data));
    if (response.status === 200) {
      setAuthTokens(JSON.stringify(data));
      setUser(jwt_decode(data.access));
      localStorage.setItem("authToken", JSON.stringify(data));
      history.push("/");
    } else {
      alert("something went wrong");
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authToken");
    history.push("/login");
    console.log("logged out");
  };
  const updateToken = async () => {
    console.log("update token called");

    let token = JSON.parse(authTokens);

    console.log("@ Refresh Called:");

    let response = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: token?.refresh }),
    });

    const data = await response.json();

    if (response.status === 200) {
      setAuthTokens(JSON.stringify(data));
      setUser(jwt_decode(data.access));
      localStorage.setItem("authToken", JSON.stringify(data));
    } else {
      logoutUser();
    }
    if (loading) {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (loading) {
      updateToken();
    }
    const fourMinutes = 4 * 60 * 1000;

    const interval = setInterval(() => {
      if (authTokens) {
        updateToken();
      }
    }, fourMinutes);
    return () => clearInterval(interval);
  }, [authTokens, loading]);

  const contextData = {
    user: user,
    authTokens: authTokens,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  );
};
