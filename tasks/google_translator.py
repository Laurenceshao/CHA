"""
A part of the task implementation is borrowed from LangChain: 
https://github.com/langchain-ai/langchain
"""
from tasks.task import BaseTask
from typing import Any, List, Dict
from pydantic import model_validator


class GoogleTranslate(BaseTask):
    name: str = "google_translator"
    chat_name: str = "GoogleTranslator"
    description: str = (
        "Translates queries between different languages."
    )
    dependencies: List[str] = []
    inputs: List[str] = ["text to be translated", "destination language"]
    outputs: List[str] = []
    output_type: bool = False

    translator: Any = None  #: :meta private:

    @model_validator(mode='before')
    def validate_environment(cls, values: Dict) -> Dict:
        """
        Validate that api key and python package exists in environment.

        Args:
            cls (object): The class itself.
            values (Dict): The dictionary containing the values for validation.
        Return:
            Dict:The original values.
        Raise:
            ImportError: If the 'playwright' package is not installed.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        try:
            from googletrans import Translator

            values["translator"] = Translator()
        except ImportError:
            raise ValueError(
                "Could not import googletrans python package. "
                "Please install it with `pip install googletrans-py`."
            )
        return values

    def parse_input(
            self,
            input: str,
    ) -> List[str]:
        """
        Parse the input string into a list of strings.

        Args:
            input (str): Input string to be parsed.
        Return:
            List[str]: List of parsed strings.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return input.split("$#")

    def execute(
            self,
            input: str,
    ) -> str:
        """
        Abstract method representing the execution of the task.

        Args:
            input (str): Input data for the task.
        Return:
            str: Result of the task execution.
        Raise:
            NotImplementedError: Subclasses must implement the execute method.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        inputs = self.parse_input(input)
        print("inputs translate", inputs)
        dest = inputs[1] if inputs[1] is not None else "en"
        result = self.translator.translate(inputs[0], dest=dest)
        return result.text, result.src

    def explain(
            self,
    ) -> str:
        """
        Provide a sample explanation for the task.

        Return:
            str: Sample explanation for the task.



        Example:
            .. code-block:: python

                from langchain import ReActChain, OpenAI
                react = ReAct(llm=OpenAI())

        """

        return (
            "This task uses google translate to translate between languages"
        )
