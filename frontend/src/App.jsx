import React, { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [active, setActive] = useState("evaluate");
  const [data, setData] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // ===== CLEAN OUTPUT =====
  const cleanOutput = (text) => {
    const idx = text.indexOf("--- FINAL ANSWER ---");
    return idx !== -1 ? text.slice(idx) : text;
  };

  // ===== PARSE =====
  const parseResult = (text) => {
    const name = text.match(/^(.*?) scored/i)?.[1] || "Candidate";
    const score = parseInt(text.match(/(\d+)\/100/)?.[1] || 0);
    const strengths =
      text.match(/Strengths:\s*(.*)/i)?.[1]?.split(",") || [];
    const gaps =
      text.match(/Gaps:\s*(.*)/i)?.[1]?.split(",") || [];

    return {
      name,
      score,
      strengths: strengths.map((s) => s.trim()),
      gaps: gaps.map((g) => g.trim()),
    };
  };

  // ===== API CALLS =====
  const evaluate = async () => {
    if (!name || !role) return alert("Enter name and role");

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API}/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: `Score ${name} for our ${role} role and save results`,
        }),
      });

      const data = await res.json();
      const cleaned = cleanOutput(data.reasoning);
      setResult(parseResult(cleaned));
    } catch {
      alert("API Error");
    }

    setLoading(false);
  };

  const getAll = async () => {
    const res = await fetch(`${API}/candidates`);
    const result = await res.json();
    setData(result);
  };

  const getTop3 = async () => {
    const res = await fetch(`${API}/top3`);
    const result = await res.json();
    setData(result);
  };

  const search = async () => {
    if (!name) return alert("Enter name");

    const res = await fetch(`${API}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    const result = await res.json();
    setData(result);
  };

  const deleteCandidate = async () => {
    if (!name) return alert("Enter name");

    await fetch(`${API}/delete`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    alert("Deleted successfully");
  };

  return (
    <div className="app">
      {/* SIDEBAR */}
      <div className="sidebar">
        <div className="logo">
          <h1></h1>
          <p>Smart Hiring Assistant</p>
        </div>

        {["evaluate", "all", "top3", "search", "delete"].map((tab) => (
          <button
            key={tab}
            className={active === tab ? "active" : ""}
            onClick={() => {
              setActive(tab);
              setResult(null);
              setData([]);
            }}
          >
            {tab.toUpperCase()}
          </button>
        ))}
      </div>

      {/* MAIN */}
      <div className="main">
        {/* TOPBAR */}
        <div className="topbar">
          <div>
            <h2>Dashboard</h2>
            <h1>JOB MATCH AI</h1>
          </div>
         
        </div>

        {/* EVALUATE */}
        {active === "evaluate" && (
          <div className="card">
            <h3>Evaluate Candidate</h3>

            <input
              placeholder="Candidate Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <input
              placeholder="Role (any role)"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            />

            <button onClick={evaluate}>
              {loading ? "Processing..." : "Evaluate"}
            </button>
          </div>
        )}

        {/* RESULT */}
        {result && (
          <div className="card resultCard">
            <h2>{result.name}</h2>

            <div className="scoreCircle">{result.score}%</div>

            <div className="progressBar">
              <div
                className="progressFill"
                style={{ width: result.score + "%" }}
              />
            </div>

            <h4>Strengths</h4>
            <div className="tags">
              {result.strengths.map((s, i) => (
                <span key={i} className="tag good">
                  {s}
                </span>
              ))}
            </div>

            <h4>Gaps</h4>
            <div className="tags">
              {result.gaps.map((g, i) => (
                <span key={i} className="tag bad">
                  {g}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* ALL */}
        {active === "all" && (
          <div className="card">
            <button onClick={getAll}>Load All Candidates</button>
          </div>
        )}

        {/* TOP3 */}
        {active === "top3" && (
          <div className="card">
            <button onClick={getTop3}>Show Top 3</button>
          </div>
        )}

        {/* SEARCH */}
        {active === "search" && (
          <div className="card">
            <input
              placeholder="Search Candidate"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <button onClick={search}>Search</button>
          </div>
        )}

        {/* DELETE */}
        {active === "delete" && (
          <div className="card">
            <input
              placeholder="Delete Candidate"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <button onClick={deleteCandidate}>Delete</button>
          </div>
        )}

        {/* TABLE */}
        {data.length > 0 && (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Score</th>
                  <th>Profile</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {data.map((row, i) => (
                  <tr key={i}>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>
                      <a href={row[4]} target="_blank" rel="noreferrer">
                        View
                      </a>
                    </td>
                    <td>{row[5]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}