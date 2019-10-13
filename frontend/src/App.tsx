import React from "react";
import TodoApp from "./TodoApp";
import "todomvc-app-css/index.css";

const App: React.FC = () => {
  return (
    <>
      <TodoApp />

      <footer className="info">
        <p>
          Freely inspired by{" "}
          <a
            href="http://todomvc.com/"
            target="_blank"
            rel="noopener noreferrer"
          >
            TodoMVC
          </a>
        </p>
        <p>
          Created by{" "}
          <a href="https://github.com/davidepedranz/">davidepedranz</a> for{" "}
          <a href="https://speckand.tech/retreat/">Speck&amp;Tech Retreat v2</a>
        </p>
      </footer>
    </>
  );
};

export default App;
