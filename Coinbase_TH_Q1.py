# Author: Jesse Fimbres
# Last Modified: 01/23/2025
# Project: Coinbase Take Home Project Question 1

from openai import OpenAI
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.arxiv_toolkit import ArxivToolkit

import logging

logging.basicConfig(level=logging.INFO)

# Agents for each data source
search_engine_agent = Agent(
    name="Search Engine Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

archive_agent = Agent(
    name="Archive Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[ArxivToolkit()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

'''
Selects agent to be used for the input query.
Returns String
'''
def choose_agent(query):
    # Use the GPT model to decide which agent is more applicable
    prompt = f"Given the following user query, determine which Phidata tool should be used; \
    			for topics in maths and sciences prefer Arxiv, else DuckDuckGo:\n \
             	Query: '{query}'\n \
             	Options: ['DuckDuckGo', 'Arxiv']\n \
             	Return only 'DuckDuckGo' or 'Arxiv'.\n"

    try:
    	# Send prompt through GPT model to determine best data souce to query from context
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0,
            n=1
        )

        result = response.choices[0].message.content.strip().lower()
        logging.info(f"GPT selected agent: {result}")
        if result not in ["DuckDuckGo", "Arxiv"]:
            return "DuckDuckGo"
        return result

    except Exception as e:
        print("Error with OpenAI API:", e)
        return "DuckDuckGo"

'''
Gets query from input and pushes to agent.
Input string should be either query or path of pdf file to use as query.
'''
def generate_ai_summary():
	query = input('Enter your query here:\n')

	selected_agent = choose_agent(query)

	if selected_agent == "DuckDuckGo":
		search_engine_agent.print_response(query, stream=True)
	else:
		archive_agent.print_response(query, markdown=True)

generate_ai_summary()
