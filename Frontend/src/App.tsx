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

  interface ApiResponse {
    respone: string;
  }

  const handleSublit = async (e: FormEvent) => {
    e.preventDefault();
    try{
      const res = await axios.post<ApiResponse>('http://127.0.0.1:5000/ask', {query})
      setResponse(res.data.respone);
    }
    catch(error) {
      setResponse("Error: Unable to fetch response.")
    }
  }
  return (
    <main>
      <div className="headers">
        <p>
          <FontAwesomeIcon icon={faQuestionCircle} size="1x" color="grey" />{" "}
          FAQs
        </p>
        <h1>Frequently Asked Questions</h1>
      </div>
      <div className="input-field">
        <input
          type="text"
          placeholder="How efficient is the FAQ answering assistant?"
        />
        <button>
          <FontAwesomeIcon icon={faSearch} className="search" />
        </button>
      </div>
      <div className="response"></div>
      <div className="faqs">
        {faqData.map((faq, index) => (
          <div className="ques" key={faq.id}>
            <p>{faq.question}</p>
            <p className="add">+</p>
          </div>
        ))}
      </div>
    </main>
  );
}

export default App;
