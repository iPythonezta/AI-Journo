from smolagents import OpenAIServerModel

def get_model(gemini_api_key: str) -> OpenAIServerModel:
    """
    Returns the model instance for text generation.
    """
    model = OpenAIServerModel(
        model_id="gemini-2.0-flash",
        api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=gemini_api_key
    )
    return model