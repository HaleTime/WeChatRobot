from .remindme import remind_me_schema, remind_me

tools_schema = [
    {
        "type": "function",
        "function": remind_me_schema
    }
]

__all__ = [
    tools_schema,
    remind_me,
]
