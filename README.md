# **ReAct Framework Implementation 🤖**

This project implements an intelligent agent using ReAct (Reasoning and Acting) prompting to answer user queries based on a combination of tools like Google Search, Wikipedia, and external API calls. The agent uses reasoning to break down the query, search relevant data, and generate a final answer.

For more information about ReAct framework read [ReAct](https://arxiv.org/pdf/2210.03629) .

## 🛠️ Project Structure

- `src/tools/`: Contains implementations for Google Search (via SERP API), Wikipedia search and Calculator tool which uses [MathFunctions](https://github.com/nellyVoskanyan03/MathFunctions) submodule.
- `src/react_agent/`: Houses the core ReAct agent implementation.

## **Features 🚀**
- **ReAct Prompting**: The agent can reason through a problem by using a chain of thought approach, iterating over multiple steps to gather more data if necessary.
- **Tool Integration**: The agent integrates with several tools, such as:
  - **Google Search** 🔍 for external information.
  - **Wikipedia** 📚 for general knowledge and article summaries.
  - **Calculator** ➗ for basic mathematical operations.
  - **Gemini API** 🔮 for advanced reasoning.
- **Iterative Process**: The agent can refine its answers by using multiple iterations, ensuring a thorough exploration of the query.

## **How It Works 🔧**

1. **Initial Query**: The user provides a query.
2. **Reasoning**: The agent identifies the best approach to answer the query by reasoning through the context.
3. **Action (Searching, Calculating)**: The agent uses available tools to search for relevant data.
4. **Iterative Answer Refining**: The agent continues refining its answer based on additional searches or new information obtained from its reasoning process.
5. **Final Answer**: After multiple iterations, the agent generates a final, comprehensive answer.

### Example Walkthrough:

**Query**: "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?"

1. 🤔 The agent starts by reasoning that it needs to find information about the Colorado orogeny, especially the eastern sector's elevation range.
2. 📚 It uses Wikipedia to get general information about the Colorado orogeny.
3. 🌍 Based on the Wikipedia data, it identifies that the eastern sector extends into the High Plains.
4. 🔍 It searches for the elevation range of the High Plains.
5. 📊 After gathering data, it provides the final answer: "The elevation range for the area that the eastern sector of the Colorado orogeny extends into is approximately 1,500 to 7,800 feet."

## **Technologies Used 🛠️**
- **Python** 🐍: The core programming language for implementing the agent.
- **Gemini API** 🔮: For advanced reasoning and response generation.
- **Google Search API** 🔍: For external searches.
- **Wikipedia API** 📚: For retrieving article summaries.
- **MathFunctions** ➗: For sin, cos, and polynomial calculations.

## **Getting Started ⚙️**

To run this project, you'll need:
1. **Python 3.9+** 
2. **API Keys**: Set up Gemini and Serp API keys.

### Installation

1. Clone the repository: Use the following command to clone the repository and initialize its submodules (MathFunctions):
   ```
   git clone --recurse-submodules https://github.com/nellyVoskanyan03/ReActFrameworkImplementation.git
   cd ReActFrameworkImplementation
   ```
    Pulling submodules: Use the following command to pull commits that include submodules (MathFunctions):
    ```
    git pull --rebase --recurse-submodules
    ```
2. Set up a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install Poetry (if not already installed):
   ```
   pip install poetry
   ```

4. Install project dependencies:
   ```
   poetry install
   ```

5. Set up environment variables:
   ```
     export PYTHONDONTWRITEBYTECODE=1
     export PYTHONPATH=$PYTHONPATH:.
   ```

### Setting up Credentials

   - Navigate to the `src` directory and create a `credentials` directory if it doesn't exist:
     ```bash
     cd src
     mkdir credentials
     cd credentials
     ```
   - Sign up for a SERP API account at https://serpapi.com/.
   - Obtain your API key from the dashboard.
   - Add your SERP API token in the following format:
   - Inside the `credentials` directory, create a `key.json` file with your API keys:
      ```json
      {
          "serp": {
              "key": "your_serp_api_key"
          },
          "gemini": {
              "key": "your_gemini_api_key"
          }
      }
      ```

## 🖥️ Usage
 Run for continuous communication with the ReAct agent:
   ```
   python -m src
   ```

