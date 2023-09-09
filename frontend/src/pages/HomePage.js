import React, { useState, useEffect, useContext } from "react";
import AuthContext from "../context/AuthContext";

const HomePage = () => {
  const [notes, setNotes] = useState([]);
  const { authTokens, logoutUser } = useContext(AuthContext);
  const accessToken = JSON.parse(authTokens).access;

  useEffect(() => {
    getNotes();
  }, []);

  const getNotes = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/notes/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        logoutUser();
        console.log("response Not ok");
      } else {
        const data = await response.json();
        setNotes(data);
      }
    } catch (error) {
      console.error("Error fetching notes:", error);
    }
  };

  return (
    <div>
      <h4>You are logged into Home Page!!</h4>
      <div className="container ">
        <ol>
          {notes.map((note) => (
            <li key={note.id}>{note.body}</li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default HomePage;
