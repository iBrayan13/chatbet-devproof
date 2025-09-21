from typing_extensions import List

from langchain_core.tools.base import BaseToolkit, BaseTool

class AuthToolkit(BaseToolkit):

    def get_tools(self) -> List[BaseTool]:
        return []