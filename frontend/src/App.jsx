import { useCallback, useEffect, useState } from "react";
import api from "./api/client";
import "./App.css";

function App() {
  const [notes, setNotes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [suggestions, setSuggestions] = useState([]);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");

  const [keyword, setKeyword] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [targetId, setTargetId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    try {
      setError("");
      const [notesResponse, graphResponse, tagsResponse] =
        await Promise.all([
          api.get("/notes/"),
          api.get("/graph/"),
          api.get("/notes/tags/suggestions"),
        ]);

      setNotes(notesResponse.data);
      setGraph(graphResponse.data);
      setSuggestions(tagsResponse.data);
    } catch {
      setError(
        "Could not connect to the API. Ensure FastAPI is running on port 8000."
      );
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function searchNotes(event) {
    event?.preventDefault();

    try {
      setError("");
      const response = await api.get("/notes/", {
        params: {
          keyword: keyword.trim() || undefined,
          tag: tagFilter.trim() || undefined,
        },
      });

      setNotes(response.data);
    } catch {
      setError("Unable to search notes.");
    }
  }

  async function createNote(event) {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");

    try {
      const response = await api.post("/notes/", {
        title,
        content,
        tags: tags.split(",").map((tag) => tag.trim()).filter(Boolean),
      });

      setTitle("");
      setContent("");
      setTags("");
      setSelected(response.data);
      setMessage("Note created successfully.");
      await refresh();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to create note."
      );
    } finally {
      setLoading(false);
    }
  }

  async function openNote(id) {
    try {
      setError("");
      const response = await api.get(`/notes/${id}`);
      setSelected(response.data);
    } catch {
      setError("Unable to load note details.");
    }
  }

  async function linkNote(event) {
    event.preventDefault();

    if (!selected || !targetId) return;

    try {
      setError("");
      await api.patch(`/notes/${selected.id}/link`, {
        target_id: Number(targetId),
      });

      setTargetId("");
      setMessage("Notes linked successfully.");
      await openNote(selected.id);
      await refresh();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to link notes."
      );
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="/">
          <span className="brand-icon">K</span>
          <span>Knowledge<span className="brand-accent">Graph</span></span>
        </a>
        <span className="api-status">
          <span className="status-dot" />
          API workspace
        </span>
      </header>

      <main className="workspace">
        <section className="hero">
          <p className="eyebrow">YOUR PERSONAL KNOWLEDGE BASE</p>
          <h1>Connect your ideas.</h1>
          <p className="hero-copy">
            Capture what you learn and discover how your notes connect.
          </p>
          <div className="stats">
            <div className="stat-card">
              <span className="stat-number">{graph.nodes.length}</span>
              <span className="stat-label">Notes</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">{graph.edges.length}</span>
              <span className="stat-label">Connections</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">{suggestions.length}</span>
              <span className="stat-label">Unique tags</span>
            </div>
          </div>
        </section>

        {error && <div className="alert error">{error}</div>}
        {message && <div className="alert success">{message}</div>}

        <div className="main-grid">
          <section className="panel create-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">CAPTURE AN IDEA</p>
                <h2>New note</h2>
              </div>
              <span className="heading-symbol">＋</span>
            </div>

            <form onSubmit={createNote} className="note-form">
              <label htmlFor="note-title">Title</label>
              <input
                id="note-title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Give your note a title"
                maxLength={200}
                required
              />

              <label htmlFor="note-content">Content</label>
              <textarea
                id="note-content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder={"Write your thoughts...\n\nUse [[Note Title]] to link an existing note."}
                rows={6}
              />

              <label htmlFor="note-tags">Tags</label>
              <input
                id="note-tags"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="learning, programming"
              />

              {suggestions.length > 0 && (
                <div className="suggestion-area">
                  <span className="muted">Existing tags</span>
                  <div className="tag-list">
                    {suggestions.slice(0, 12).map((tag) => (
                      <button
                        type="button"
                        className="tag-chip clickable"
                        key={tag}
                        onClick={() =>
                          setTags((current) => {
                            const currentTags = current
                              .split(",")
                              .map((t) => t.trim())
                              .filter(Boolean);

                            if (
                              currentTags.some(
                                (t) => t.toLowerCase() === tag.toLowerCase()
                              )
                            ) {
                              return current;
                            }

                            return [...currentTags, tag].join(", ");
                          })
                        }
                      >
                        + {tag}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <button className="primary-button" disabled={loading}>
                {loading ? "Saving..." : "Create note →"}
              </button>
            </form>
          </section>

          <section className="panel notes-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">YOUR COLLECTION</p>
                <h2>All notes</h2>
              </div>
              <span className="count-pill">{notes.length}</span>
            </div>

            <form className="search-form" onSubmit={searchNotes}>
              <input
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Search titles and content..."
                aria-label="Search notes"
              />
              <input
                value={tagFilter}
                onChange={(e) => setTagFilter(e.target.value)}
                placeholder="Filter by tag"
                aria-label="Filter by tag"
                list="available-tags"
              />
              <datalist id="available-tags">
                {suggestions.map((tag) => (
                  <option value={tag} key={tag} />
                ))}
              </datalist>
              <button className="secondary-button">Search</button>
              <button
                className="text-button"
                type="button"
                onClick={() => {
                  setKeyword("");
                  setTagFilter("");
                  api.get("/notes/").then((r) => setNotes(r.data));
                }}
              >
                Clear
              </button>
            </form>

            <div className="note-list">
              {notes.map((note) => (
                <button
                  key={note.id}
                  className={`note-card ${
                    selected?.id === note.id ? "selected" : ""
                  }`}
                  onClick={() => openNote(note.id)}
                >
                  <div className="note-card-top">
                    <h3>{note.title}</h3>
                    <span className="note-arrow">↗</span>
                  </div>
                  <p className="note-preview">
                    {note.content || "No content yet."}
                  </p>
                  <div className="tag-list">
                    {note.tags.map((tag) => (
                      <span className="tag-chip" key={tag}>
                        {tag}
                      </span>
                    ))}
                  </div>
                  <span className="note-id">NOTE #{note.id}</span>
                </button>
              ))}

              {notes.length === 0 && (
                <div className="empty-state">
                  <span className="empty-icon">◇</span>
                  <h3>No notes found</h3>
                  <p>Create a note or adjust your search.</p>
                </div>
              )}
            </div>
          </section>
        </div>

        <section className="panel detail-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">EXPLORE CONNECTIONS</p>
              <h2>{selected ? selected.title : "Note details"}</h2>
            </div>
            {selected && (
              <span className="count-pill">#{selected.id}</span>
            )}
          </div>

          {!selected ? (
            <p className="muted">
              Select a note above to inspect its content and connections.
            </p>
          ) : (
            <>
              <div className="detail-content">
                <p>{selected.content || "No content yet."}</p>
                <div className="tag-list">
                  {selected.tags.map((tag) => (
                    <span className="tag-chip" key={tag}>{tag}</span>
                  ))}
                </div>
              </div>

              <div className="connections-grid">
                <div className="connection-section">
                  <h3>↗ Outgoing links</h3>
                  {selected.linked_notes.length === 0 ? (
                    <p className="muted">No outgoing links.</p>
                  ) : selected.linked_notes.map((note) => (
                    <button
                      key={note.id}
                      className="connection-item"
                      onClick={() => openNote(note.id)}
                    >
                      {note.title} <span>↗</span>
                    </button>
                  ))}
                </div>

                <div className="connection-section">
                  <h3>↙ Backlinks</h3>
                  {selected.backlinks.length === 0 ? (
                    <p className="muted">No backlinks yet.</p>
                  ) : selected.backlinks.map((note) => (
                    <button
                      key={note.id}
                      className="connection-item"
                      onClick={() => openNote(note.id)}
                    >
                      {note.title} <span>↙</span>
                    </button>
                  ))}
                </div>
              </div>

              <form className="manual-link-form" onSubmit={linkNote}>
                <div>
                  <h3>Create a connection</h3>
                  <p className="muted">
                    Link this note to another note by its ID.
                  </p>
                </div>
                <select
                  value={targetId}
                  onChange={(e) => setTargetId(e.target.value)}
                  required
                >
                  <option value="">Select a target note</option>
                  {graph.nodes
                    .filter((note) => note.id !== selected.id)
                    .map((note) => (
                      <option key={note.id} value={note.id}>
                        #{note.id} — {note.title}
                      </option>
                    ))}
                </select>
                <button className="primary-button" disabled={!targetId}>
                  Link notes →
                </button>
              </form>
            </>
          )}
        </section>

        <section className="panel graph-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">KNOWLEDGE MAP</p>
              <h2>Connection overview</h2>
            </div>
            <span className="count-pill">{graph.edges.length} links</span>
          </div>

          {graph.nodes.length === 0 ? (
            <p className="muted">Your graph will appear here as you add notes.</p>
          ) : (
            <div className="graph-list">
              {graph.nodes.map((node) => {
                const outgoing = graph.edges.filter(
                  (edge) => edge.source === node.id
                );
                const incoming = graph.edges.filter(
                  (edge) => edge.target === node.id
                );

                return (
                  <button
                    className="graph-node"
                    key={node.id}
                    onClick={() => openNote(node.id)}
                  >
                    <span className="graph-node-dot" />
                    <span className="graph-node-name">{node.title}</span>
                    <span className="graph-node-meta">
                      {incoming.length} in · {outgoing.length} out
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        Personal Knowledge Graph <span>·</span> Built to connect ideas
      </footer>
    </div>
  );
}

export default App;