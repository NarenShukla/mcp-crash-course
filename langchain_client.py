import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

# llm = ChatOpenAI()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "uv",
                "args": [
                    "run",
                    "/home/naren/mcp-crash-course/worktrees/sse/servers/math_server.py"
                ]
            },
            "weather-sse": {
                "url": "http://127.0.0.1:8000/sse/",
                "transport": "sse"
            }
        }
    )
    tools = client.get_tools()

    print("Tools: ", tools)

    # tools = await client.get_tools()

    agent = create_react_agent(llm, client.get_tools())

    print("Calling Math Server, which has stdio transport")

    result = await agent.ainvoke({"messages": "What is 2 + 2?"})

    print(result["messages"][-1].content)

    print("Calling Weather Server, which has SSE transport")

    result = await agent.ainvoke(
        {"messages": "What is the weather in Pune?"}
    )

    # result = await agent.ainvoke({
    #     "messages": [
    #         {"role": "system", "content": "Use weather-sse MCP Server. \
    #                                     Use get_weather tool to get the weather. \
    #                                     Don't make up the weather."},
    #         {"role": "user", "content": "What is the weather in Mumbai ?"}
    #     ]
    # })

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
