# **ReAct Framework Implementation 🤖**

This project implements an intelligent agent using ReAct (Reasoning and Acting) prompting to answer user queries based on a combination of tools like Google Search, Wikipedia, and external API calls. The agent uses reasoning to break down the query, search relevant data, and generate a final answer.

## **Project Overview 🌟**

The agent is designed to answer complex questions by:
1. 🤔 Reasoning about the query.
2. 🔍 Using external tools (Google, Wikipedia, Calculator) to gather data.
3. 🧩 Combining the results to provide a coherent and accurate response.

The agent follows an iterative approach:
- 🔄 It generates an initial answer based on available data.
- 📈 If more information is needed, it refines its answer by performing additional searches or using other tools.

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
1. **Python 3.x** 🐍
2. **API Keys** 🔑: Set up Gemini and Serp API keys.
3. **Dependencies** 📦: Install the required Python libraries using `pip`.

### Steps to Set Up:

1. Clone the repository:
   Use the following command to clone the repository and initialize its submodules (MathFunctions):
    ```sh
    git clone --recurse-submodules https://github.com/nellyVoskanyan03/ReActFrameworkImplementation.git
    ```
2. Pulling submodules:
    Use the following command to pull commits that include submodules (MathFunctions):
    ```sh
    git pull --rebase --recurse-submodules
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your API keys:
   - Navigate to the `src` directory and create a `credentials` directory if it doesn't exist:
     ```bash
     cd src
     mkdir credentials
     ```
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

5. Set up a virtual environment:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```
6. Set up environment variables:
   ```sh
   export PYTHONDONTWRITEBYTECODE=1
   export PYTHONPATH=$PYTHONPATH:.

## 🖥️ Usage
 Run the ReAct agent:
   ```
   python -m src
   ```
