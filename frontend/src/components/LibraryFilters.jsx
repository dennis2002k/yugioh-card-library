import { useEffect, useState } from "react";
import "../index.css";

const attributes = [
  "DARK","LIGHT","EARTH","WATER","FIRE","WIND","DIVINE"
];

const monsterTypes = [
  "Spellcaster","Dragon","Zombie","Warrior","Beast-Warrior","Beast",
  "Winged Beast","Fiend","Fairy","Insect","Dinosaur","Reptile","Fish",
  "Sea Serpent","Aqua","Pyro","Thunder","Rock","Plant","Machine",
  "Psychic","Divine-Beast","Wyrm","Cyberse","Illusion"
];

const cardFrames = [
  "Normal","Effect","Ritual","Fusion","Synchro","XYZ",
  "Toon","Spirit","Union","Gemini","Tuner",
  "Flip","Pendulum","Link"
];

const cardTypes = ["Monster", "Spell Card", "Trap Card"]

const icons = ["Equip", "Field", "Quick-Play", "Ritual", "Continuous", "Counter", "Normal"];

function LibraryFilters({ onSearch }) {
  const [filters, setFilters] = useState({});

  function updateFilter(key, value) {
    setFilters(prev => ({
      ...prev,
      [key]: value || undefined,
    }));
  }

  // Live update
  useEffect(() => {
    const delay = setTimeout(() => {
      onSearch(filters);
    }, 150); // debounce typing

    return () => clearTimeout(delay);
  }, [filters]);

  const boxStyle = { width: "70px" };

  return (
    <div
      style={{
        padding: "10px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        marginBottom: "20px",
        display: "flex",
        flexWrap: "wrap",
        gap: "10px",
        alignItems: "center",
      }}
    >
      <input
        placeholder="Name"
        onChange={e => updateFilter("name", e.target.value)}
      />

      <select onChange={e => updateFilter("type", e.target.value)}>
        <option value="">Card Type</option>
        {cardTypes.map(t => (
          <option key={t}>{t}</option>
        ))}
      </select>

      <select onChange={e => updateFilter("attribute", e.target.value)}>
        <option value="">Attribute</option>
        {attributes.map(a => (
          <option key={a}>{a}</option>
        ))}
      </select>

      <select onChange={e => updateFilter("race", e.target.value)}>
        <option value="">Spell&Trap Type</option>
        {icons.map(t => (
          <option key={t}>{t}</option>
        ))}
      </select>

      <select onChange={e => updateFilter("race", e.target.value)}>
        <option value="">Monster Type</option>
        {monsterTypes.map(t => (
          <option key={t}>{t}</option>
        ))}
      </select>

      <select onChange={e => updateFilter("frameType", e.target.value)}>
        <option value="">Card Frame</option>
        {cardFrames.map(t => (
          <option key={t}>{t}</option>
        ))}
      </select>

      <input
        style={boxStyle}
        type="number"
        placeholder="Lvl"
        min="0"
        max="13"
        onChange={e => updateFilter("level", e.target.value)}
      />

      <input
        style={boxStyle}
        type="number"
        placeholder="Pend"
        min="0"
        max="13"
        onChange={e => updateFilter("pend_scale", e.target.value)}
      />

      <input
        style={boxStyle}
        type="number"
        placeholder="Link"
        min="1"
        max="6"
        onChange={e => updateFilter("link_rating", e.target.value)}
      />

      <input
        style={boxStyle}
        type="number"
        placeholder="ATK min"
        onChange={e => updateFilter("min_atk", e.target.value)}
      />

      <input
        style={boxStyle}
        type="number"
        placeholder="ATK max"
        onChange={e => updateFilter("max_atk", e.target.value)}
      />

      <input
        style={boxStyle}
        type="number"
        placeholder="DEF min"
        onChange={e => updateFilter("min_defense", e.target.value)}
      />

      <input
        style={boxStyle}
        type="number"
        placeholder="DEF max"
        onChange={e => updateFilter("max_defense", e.target.value)}
      />
    </div>
  );
}

export default LibraryFilters;

