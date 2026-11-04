import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ValidationError

from app.services.agent.base_tool import BaseAgentTool, ToolExecutionContext, ToolResult

logger = logging.getLogger(__name__)


class AgentToolRegistry:
    """
    Central Registry for Autonomous Agent Tools.
    Enforces the Open-Closed principle: adding a new tool is as simple as registering
    an instance of BaseAgentTool, without modifying the agent loop.
    """
    def __init__(self):
        self._tools: Dict[str, BaseAgentTool] = {}

    def register(self, tool: BaseAgentTool) -> None:
        if tool.name in self._tools:
            logger.warning(f"Overwriting already registered tool: {tool.name}")
        self._tools[tool.name] = tool
        logger.info(f"Registered agent tool: {tool.name} [{tool.category.value}]")

    def get(self, name: str) -> Optional[BaseAgentTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[BaseAgentTool]:
        return list(self._tools.values())

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Generates standard JSON schema definitions suitable for LLM function calling / tools.
        """
        definitions = []
        for tool in self._tools.values():
            schema = tool.input_schema.model_json_schema()
            definitions.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": schema,
                }
            })
        return definitions

    async def execute_tool(
        self,
        tool_name: str,
        ctx: ToolExecutionContext,
        arguments: Dict[str, Any],
    ) -> ToolResult:
        tool = self.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                summary=f"Tool '{tool_name}' not found.",
                error_message=f"Tool '{tool_name}' is not registered in the system registry.",
            )

        try:
            params = tool.input_schema(**arguments)
            return await tool.execute(ctx, params)
        except ValidationError as ve:
            logger.warning(f"Validation error executing {tool_name}: {ve}")
            return ToolResult(
                success=False,
                summary=f"Invalid arguments for {tool_name}",
                error_message=str(ve),
            )
        except Exception as e:
            logger.exception(f"Unhandled error executing tool {tool_name}: {e}")
            return ToolResult(
                success=False,
                summary=f"Execution error in {tool_name}",
                error_message=str(e),
            )
