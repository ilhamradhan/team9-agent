from __future__ import annotations

import re
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOCUMENTS_DIR = PROJECT_ROOT / "data" / "hr"
STOP_WORDS = {
    "a", "an", "and", "are", "do", "does", "for", "from", "get", "how",
    "i", "in", "is", "it", "me", "of", "on", "the", "to", "what", "when",
    "where", "which", "who", "why", "with", "you", "your",
}
FALLBACK = "I couldn't find this information in the provided HR documents. Please ask HR."


class RetrievedSection(TypedDict):
    content: str
    source: str


class HRState(TypedDict, total=False):
    question: str
    retrieved: list[RetrievedSection]
    answer: str
    sources: list[str]


def _tokens(text: str) -> set[str]:
    return {
        token[:-1] if token.endswith("s") and len(token) > 3 else token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOP_WORDS
    }


def _load_sections(documents_dir: Path) -> list[RetrievedSection]:
    sections: list[RetrievedSection] = []
    for path in sorted(documents_dir.rglob("*.md")):
        title: str | None = None
        body: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                if title and " ".join(body).strip():
                    sections.append({
                        "content": " ".join(body).strip(),
                        "source": f"{path.relative_to(documents_dir)}#{title}",
                    })
                title = line[3:].strip()
                body = []
            elif title and line.strip() and not line.startswith("# "):
                body.append(line.strip())
        if title and " ".join(body).strip():
            sections.append({
                "content": " ".join(body).strip(),
                "source": f"{path.relative_to(documents_dir)}#{title}",
            })
    return sections


def build_graph(documents_dir: Path = DEFAULT_DOCUMENTS_DIR):
    """Build the small HR Q&A graph with a deterministic demo answer step."""

    def retrieve(state: HRState) -> dict[str, list[RetrievedSection]]:
        query = _tokens(state.get("question", ""))
        ranked = []
        for section in _load_sections(Path(documents_dir)):
            score = len(query & _tokens(section["source"] + " " + section["content"]))
            if score >= 2:
                ranked.append((score, section))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return {"retrieved": [section for _, section in ranked[:1]]}

    def generate(state: HRState) -> dict[str, object]:
        retrieved = state.get("retrieved", [])
        if not retrieved:
            return {"answer": FALLBACK, "sources": []}
        section = retrieved[0]
        return {
            "answer": f"The sample policy says: {section['content']} [Source: {section['source']}]",
            "sources": [section["source"]],
        }

    graph = StateGraph(HRState)
    graph.add_node("retrieve_hr_documents", retrieve)
    graph.add_node("generate_answer", generate)
    graph.add_edge(START, "retrieve_hr_documents")
    graph.add_edge("retrieve_hr_documents", "generate_answer")
    graph.add_edge("generate_answer", END)
    return graph.compile()
