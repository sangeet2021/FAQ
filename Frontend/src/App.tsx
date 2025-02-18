import "./App.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import faqData from "../data/db.json";
import { FormEvent, useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  interface ApiResponse {
    response: string;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      console.log("Sending query:", query); // Log the query
      const res = await axios.post<ApiResponse>("http://127.0.0.1:5000/ask", {
        query,
      });
      console.log("Received response:", res.data); // Log the response
      setResponse(res.data.response);
    } catch (error) {
      console.error("API Error:", error); // Log the error
      setResponse("Error: Unable to fetch response.");
    }
    setLoading(false);
  };

  const handleQuery = (data: string) => {
    setQuery(data);
  };

  return (
    <main>
      <div className="headers">
        <p>
          <FontAwesomeIcon icon={faQuestionCircle} size="1x" color="grey" />{" "}
          FAQs
        </p>
        <h1>Frequently Asked Questions</h1>
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query.charAt(0).toUpperCase() + query.slice(1)}
          placeholder="How efficient is the FAQ answering assistant?"
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">
          <FontAwesomeIcon icon={faSearch} className="search" />
        </button>
      </form>
      {/* {response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )} */}
      <div className="response">
        {loading ? (
          <div className="loading-dots">
            <div className="dot"></div>
            <div className="dot"></div>
            <div className="dot"></div>
          </div>
        ) : (
          <div className="respons">
            <p>{response}</p>
          </div>
        )}
      </div>
      <div className="faqs">
        {faqData.map((faq, index) => (
          <div className="ques" key={faq.id}>
            <p>{faq.question}</p>
            <p className="add" onClick={() => handleQuery(faq.question)}>
              +
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}

export default App;
