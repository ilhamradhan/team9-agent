import argparse

from dotenv import load_dotenv

from hr_agent.workflow import DEFAULT_DOCUMENTS_DIR, PROJECT_ROOT, build_graph


def main() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    parser = argparse.ArgumentParser(description="Ask the sample HR policy documents.")
    parser.add_argument("--mock", action="store_true", help="Use retrieved text without calling DeepSeek")
    parser.add_argument("--employee-id", help="Demo employee ID for personal leave-balance questions")
    parser.add_argument("question", help="Question about the supplied HR documents")
    args = parser.parse_args()
    answerer = (lambda question, sections: sections[0]["content"]) if args.mock else None
    state = {"question": args.question}
    if args.employee_id:
        state["employee_id"] = args.employee_id
    result = build_graph(DEFAULT_DOCUMENTS_DIR, answerer=answerer).invoke(state)
    print(result["answer"])
