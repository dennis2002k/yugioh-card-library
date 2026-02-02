import { useEffect, useState } from "react";
import LibraryFilters from "../components/LibraryFilters";
import GlobalCardSearch from "../components/GlobalCardSearch";
import "../index.css"

function Library() {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [fetching, setFetching] = useState(false);


  async function addToLibrary(cardId) {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:8000/me/library/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ id: cardId }),
      });

      if (!response.ok) throw new Error("Failed to add");

      const data = await response.json();
      console.log("Added:", data);
      fetchLibrary();
    //   if (onAdd) onAdd(data); // notify parent to update library
    } catch (err) {
      console.error("Error adding card:", err);
    }
  }


  async function removeFromLibrary(cardId) {
    try {
      const token = localStorage.getItem("token");
  
      const response = await fetch(
        `http://localhost:8000/me/library/delete/${cardId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
  
      if (!response.ok) {
        throw new Error("Failed to remove card");
      }
  
      // Update UI optimistically
      setCards((prev) =>
        prev
          .map((card) =>
            card.id === cardId
              ? { ...card, quantity: card.quantity - 1 }
              : card
          )
          .filter((card) => card.quantity > 0)
      );
    } catch (err) {
      console.error("Error removing card:", err);
    }
  }
 

  async function fetchLibrary(filters = {}) {
    try {
      setFetching(true);

      const token = localStorage.getItem("token");

      const params = new URLSearchParams();
      Object.entries(filters).forEach(([k, v]) => {
        if (v) params.append(k, v);
      });

      const response = await fetch(
        `http://localhost:8000/me/library/search?${params.toString()}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 401) {
        throw new Error("unauthorized");
      }

      if (response.status === 403) {
        throw new Error("forbidden");
      }

      if (!response.ok) {
        throw new Error("unknown");
      }

      const data = await response.json();
      setCards(data);
    } catch (err) {
      console.log("Error:", err.message);

      if (err.message === "unauthorized") {
        setError("Session expired. Please login again.");
      } else {
        setError("Could not load library.");
      }
    } finally {
        setLoading(false);
        setFetching(false);
    }
  }

  // initial load
  useEffect(() => {
    fetchLibrary();
  }, []);

  if (loading) {
    return <p>Loading library...</p>;
  }
  if (error) return <p>{error}</p>;

  return (
    <div style={{ display: "flex", height: "100vh" }}>
  {/* LEFT SIDE */}
  <div style={{ width: "70%", display: "flex", flexDirection: "column" }}>

    {/* FIXED TOP AREA */}
    <div style={{
      padding: "20px",
      borderBottom: "1px solid #333",
      background: "#000",
      flexShrink: 0,
    }}>
      <LibraryFilters onSearch={fetchLibrary} />
      <h2>Your Library</h2>
    </div>

    {/* SCROLLING CONTENT */}
    <div style={{
      padding: "20px",
      overflowY: "auto",
      flex: 1,
    }}>
      {cards.length === 0 ? (
        <p>No cards in your collection.</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))",
            gap: "16px",
          }}
        >
          {cards.map((card) => {
            let imageUrl = card.card_images?.image_url;

            if (imageUrl?.startsWith("../")) {
              imageUrl = imageUrl.replace("../", "/");
            }

            imageUrl = "http://localhost:8000" + imageUrl;

            return (
              <div
                key={card.id}
                className="card library-card"
                style={{
                  border: "1px solid #ccc",
                  borderRadius: "8px",
                  padding: "8px",
                  textAlign: "center",
                }}
              >
                {imageUrl && (
                  <img
                    src={imageUrl}
                    alt={card.name}
                    style={{ width: "70%" }}
                  />
                )}
                <p>{card.name}</p>
                <p>Quantity: {card.quantity}</p>
                <button
                  className="remove-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFromLibrary(card.id);
                  }}
                >
                  − Remove
                </button>
                <button
                  className="add-btn small"
                  onClick={(e) => {
                    e.stopPropagation();
                    addToLibrary(card.id);
                  }}
                >
                  + Add
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  </div>

  {/* RIGHT SIDE */}
  <GlobalCardSearch refreshLibrary={fetchLibrary} addToLibrary={addToLibrary}/>
</div>

  );
}

export default Library;

  