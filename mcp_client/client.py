from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

class MCPClient:

    async def call_tool(self, server_url, tool_name, args):

        async with sse_client(server_url) as streams:

            async with ClientSession(*streams) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    args
                )

                return result.content