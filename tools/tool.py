from instructor.function_calls import OpenAISchema

class Tool(OpenAISchema):
    def execute(**kwargs):
        raise NotImplementedError("execute method not implemented")