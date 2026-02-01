// src/components/GlobalFilters.jsx
import { useState, useEffect } from "react";
import "../index.css";

const ATTRIBUTE_OPTIONS = ["dark","light","earth","water","fire","wind","divine"];
const MONSTER_TYPES = ["spellcaster","dragon","zombie","warrior","beast-warrior","beast","winged-beast","fiend","fairy","insect","dinosaur","reptile","fish","sea serpent","aqua","pyro","thunder","rock","plant","machine","psychic","divine-beast","wyrm","cyberse","illusion"];
const CARD_TYPES = ["normal","effect","ritual","fusion","synchro","xyz","toon","spirit","union","gemini","tuner","flip","pendulum","link"];

export default function GlobalFilters({ onChange }) {
  const [filters, setFilters] = useState({});

  function updateFilter(key, value) {
    setFilters(prev => ({
      ...prev,
      [key]: value || undefined,
    }));
  }

  // call onChange with debounce
  useEffect(() => {
    const delay = setTimeout(() => {
      onChange(filters);
    }, 200); // 200ms debounce

    return () => clearTimeout(delay);
  }, [filters]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
      <input
        placeholder="Card Name"
        onChange={e => updateFilter("name", e.target.value)}
      />

      <select onChange={e => updateFilter("attribute", e.target.value)}>
        <option value="">All Attributes</option>
        {ATTRIBUTE_OPTIONS.map(a => <option key={a} value={a}>{a}</option>)}
      </select>

      <select onChange={e => updateFilter("race", e.target.value)}>
        <option value="">All Monster Types</option>
        {MONSTER_TYPES.map(a => <option key={a} value={a}>{a}</option>)}
      </select>

      <select onChange={e => updateFilter("type", e.target.value)}>
        <option value="">All Card Types</option>
        {CARD_TYPES.map(a => <option key={a} value={a}>{a}</option>)}
      </select>

      <div style={{ display: "flex", gap: "4px" }}>
        <input
          type="number"
          placeholder="Level/Rank min"
          onChange={e => updateFilter("min_level", e.target.value)}
        />
        <input
          type="number"
          placeholder="Level/Rank max"
          onChange={e => updateFilter("max_level", e.target.value)}
        />
      </div>

      <div style={{ display: "flex", gap: "4px" }}>
        <input
          type="number"
          placeholder="Pendulum min"
          onChange={e => updateFilter("pend_scale", e.target.value)}
        />
        <input
          type="number"
          placeholder="Pendulum max"
          onChange={e => updateFilter("scale_max", e.target.value)}
        />
      </div>

      <div style={{ display: "flex", gap: "4px" }}>
        <input
          type="number"
          placeholder="Link rating min"
          onChange={e => updateFilter("link_rating", e.target.value)}
        />
        <input
          type="number"
          placeholder="Link rating max"
          onChange={e => updateFilter("link_rating_max", e.target.value)}
        />
      </div>

      <div style={{ display: "flex", gap: "4px" }}>
        <input
          type="number"
          placeholder="ATK min"
          onChange={e => updateFilter("min_atk", e.target.value)}
        />
        <input
          type="number"
          placeholder="ATK max"
          onChange={e => updateFilter("max_atk", e.target.value)}
        />
      </div>

      <div style={{ display: "flex", gap: "4px" }}>
        <input
          type="number"
          placeholder="DEF min"
          onChange={e => updateFilter("min_defense", e.target.value)}
        />
        <input
          type="number"
          placeholder="DEF max"
          onChange={e => updateFilter("min_defense", e.target.value)}
        />
      </div>
    </div>
  );
}
