from .function_calls import OpenAISchema, openai_function, openai_schema
from .distil import FinetuneFormat, Instructions
from .dsl import MultiTask, Maybe, llm_validator, CitationMixin
from .patch import patch, unpatch
from typing import Iterable, Optional, Union
import more_itertools
import openai
import time

def create_stream_extract(system_promopt, user_msg, cls, **kwargs):
    def _stream_extract(input: str) -> Iterable[OpenAISchema]:
        MultiObj = MultiTask(cls)
        completion = openai.ChatCompletion.create(
            stream=True,
            functions=[MultiObj.openai_schema],
            function_call={"name": MultiObj.openai_schema["name"]},
            messages=[
                {"role": "system","content": system_promopt},
                {"role": "user","content": user_msg.format(input=input)},
            ],
            **kwargs
        )
        return MultiObj.from_streaming_response(completion)
    return _stream_extract
