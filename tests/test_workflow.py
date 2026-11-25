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


def test_personal_question_requests_employee_id():
    result = build_graph(answerer=fixed_answer).invoke(
        {"question": "How many vacation days do I have left?"}
    )

    assert result["answer"] == "Please provide your employee ID to look up your leave balance."
    assert result["sources"] == []


def test_personal_question_returns_only_demo_balance_for_known_id():
    result = build_graph(answerer=fixed_answer).invoke(
        {
            "question": "How many vacation days do I have left?",
            "employee_id": "TEST-001",
        }
    )

    assert result["answer"] == (
        "Your remaining annual leave balance is 12 days. "
        "[Source: demo_employees.json#TEST-001]"
    )
    assert result["sources"] == ["demo_employees.json#TEST-001"]


def test_personal_question_does_not_return_data_for_unknown_id():
    result = build_graph(answerer=fixed_answer).invoke(
        {
            "question": "How many vacation days do I have left?",
            "employee_id": "UNKNOWN",
        }
    )

    assert result["answer"] == "No matching employee ID exists in the demo records."
    assert result["sources"] == []
