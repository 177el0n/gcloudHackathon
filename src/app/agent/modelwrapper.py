from vertexai.preview.language_models import TextGenerationModel
from langchain_core.runnables import Runnable

class GeminiModelWrapper(Runnable):
    def __init__(self, model_name: str):
        self.model = TextGenerationModel.from_pretrained(model_name)

    def __call__(self, prompt: str, **kwargs):
        response = self.model.predict(prompt, **kwargs)
        return response.text

    def invoke(self, input_data: str, **kwargs):
        response = self.model.predict(input_data, **kwargs)
        return response.text