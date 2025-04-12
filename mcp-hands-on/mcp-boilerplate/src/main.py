from mcp.server.fastmcp import FastMCP

# Import tools, resources, and prompts
from .tools.sample_tool import sample_tool_logic, another_tool_logic
from .resources.sample_resource import get_resource_by_id
from .prompts.sample_prompt import get_formatted_prompt

# Initialize FastMCP server
mcp = FastMCP("mcp-boilerplate")

# 도구, 리소스, 프롬프트 등록
mcp.tool()(sample_tool_logic)
mcp.tool()(another_tool_logic)
mcp.resource(uri="file://mcp-boilerplate/{resource_id}")(get_resource_by_id)
mcp.prompt()(get_formatted_prompt)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse', host='127.0.0.1', port=8000)
