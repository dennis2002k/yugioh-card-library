import { useState, useEffect } from "react";
import GlobalFilters from "./GlobalFilters";
import "../index.css";

export default function GlobalCardSearch({refreshLibrary, addToLibrary}) {
  const [filters, setFilters] = useState({});
  const [results, setResults] = useState([]);

  async function searchCards(currentFilters) {
    console.log("Searching with filters:", currentFilters); // <-- This should run
    try {
      const token = localStorage.getItem("token");
      const params = new URLSearchParams(currentFilters).toString();
      const response = await fetch(`http://127.0.0.1:8000/card/search?${params}`,
      {
        headers: {
            Authorization: `Bearer ${token}`,
        }
      }
      );
      if (!response.ok) throw new Error();
      const data = await response.json();
      console.log("Got results:", data); // <-- This should also run
      setResults(data.slice(0, 20));
    } catch (err) {
      console.log("Search error", err);
      setResults([]);
    }
  }

  // Debounce effect for live typing
  useEffect(() => {
    // Call search immediately only if filters is not empty
    if (Object.keys(filters).length === 0) return;

    const timeout = setTimeout(() => {
      searchCards(filters);
    }, 150);

    return () => clearTimeout(timeout);
  }, [filters]);

  return (
    <div style={{ width: "30%", padding: "10px", borderLeft: "1px solid #ccc" }}>
      <h3>Global Search</h3>
      <GlobalFilters onChange={setFilters} />

      {results.length > 0 && (
        <div style={{ border: "1px solid #ccc", borderRadius: "6px", maxHeight: "400px", overflowY: "auto", background: "white", marginTop: "8px" }}>
          {results.map(card => {
            let images = [];
            const imageUrl = card.card_images[0].image_url?.replace("../","/");
            console.log(imageUrl)
            const fullUrl = imageUrl ? "http://127.0.0.1:9000/ygo-card-images" + imageUrl : null;

            return (
              <div key={card.id} className="card"  style={{ display: "flex", alignItems: "center", gap: "10px", padding: "6px", borderBottom: "1px solid #eee" }}
              onClick={() => addToLibrary(card.id)}
              >
                {fullUrl && <img src={fullUrl} alt={card.name} style={{ width: "40px" }} />}
                <span>{card.name}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}


