import "./App.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import faqData from "../data/db.json";

function App() {
  const askQuestion = async() => {
    window.alert("Question Asked")
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
        <button onClick={askQuestion}>
          <FontAwesomeIcon icon={faSearch} className="search" />
        </button>
      </div>
      <div className="faqs">
        {faqData.map((faq, index) => (
          <div className="ques"  key={faq.id}>
            <p>{faq.question}</p>
            <p className="add">+</p>
          </div>
        ))}
      </div>
    </main>
  );
}

export default App;
