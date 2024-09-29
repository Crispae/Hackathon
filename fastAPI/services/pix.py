from mistralai import Mistral
import os
import base64


class Pixtral:
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model = Mistral(
            api_key=self.api_key,
        )
        self.model_name = model_name

    @staticmethod
    def file_to_data_url(file_path: str):
        """
        Convert a local image file to a data URL.
        """
        with open(file_path, "rb") as image_file:
            ## Encoding url to base64
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

            ## Getting mime type
            _, extension = os.path.splitext(file_path)
            mime_type = f"image/{extension[1:].lower()}"

            ## Returning data url
            return f"data:{mime_type};base64,{encoded_string}"

    def complete(
        self,
        prompt,
        image_base46_encoding,
        image_path=None,
    ):
        if image_path is None:
            image_source = image_base46_encoding
        else:
            image_source = Pixtral.file_to_data_url(image_path)

        ## Creating messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_source}},
                ],
            },
        ]

        ## Getting response
        response = self.model.chat.complete(model=self.model_name, messages=messages)

        return response
