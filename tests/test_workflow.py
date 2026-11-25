from hr_agent.workflow import build_graph


def fixed_answer(question, retrieved):
    return "You get one paid working day off."


def test_answers_from_retrieved_document_with_source():
    result = build_graph(answerer=fixed_answer).invoke(
        {"question": "How many paid days off do I get for my wedding?"}
    )

    assert result["answer"] == (
        "You get one paid working day off. "
        "[Source: leave_policy.md#Wedding leave]"
    )
    assert result["sources"] == ["leave_policy.md#Wedding leave"]


def test_falls_back_when_documents_do_not_cover_question():
    result = build_graph(answerer=fixed_answer).invoke(
        {"question": "What is the policy for payroll corrections?"}
    )

    assert result["answer"] == (
        "I couldn't find this information in the provided HR documents. "
        "Please ask HR."
    )
    assert result["sources"] == []
