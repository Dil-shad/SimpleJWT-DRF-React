import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./App.css";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Header from "./components/Header";
import PrivateRoute from "./utils/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <div className="App">
      <h1>My App Title</h1>
      <Router>
        <AuthProvider>
          <Header />
          <PrivateRoute component={HomePage} path="/" exact />
          <Route path="/login" component={LoginPage} />
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
