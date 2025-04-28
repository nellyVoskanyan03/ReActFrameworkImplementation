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

## Flow of Execution

- **Input**:  
  The agent starts by receiving a task in natural language. This task is passed into the core language model (LLM), such as Gemini Pro, which interprets what needs to be done. The LLM acts as the agent’s "brain," initiating the task. The user provides the task, and the agent's goal is to leverage available tools to solve it.

- **Reasoning**:  
  The LLM analyzes the task, plans the steps required, and decides on an approach based on available information and registered tools.

- **Action with External Environments**:  
  The agent has access to external environments — currently Google Search, Wikipedia, and a Calculator tool.
  - **Google Search**: Looks up real-time information from the web.
  - **Wikipedia**: Gathers factual knowledge and general information.
  - **Calculator**: Performs mathematical calculations when required.  

- **Observation and Memory**:  
  After executing an action, the agent observes the result and stores relevant information in its memory. This allows the agent to track past actions, avoid repetition, and build context for future reasoning steps.

- **Feedback Loop**:  
  The agent iterates through reasoning, action, and observation repeatedly. After each new observation, it reassesses the task using updated knowledge. This loop helps the agent refine its approach. The loop continues until an end condition is met or the maximum number of iterations (`max_iterations`) is reached. Memory is leveraged to maintain context across iterations.

- **Response**:  
  Once enough information has been gathered, the agent formulates a final response based on everything collected and reasoned over multiple cycles. If a satisfactory outcome isn't reached within the maximum iterations, it returns the best attempt or an apology message.


### Example Walkthrough:

**Query**: "What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?"

1. **Thought** -> 💭 Thought: The query asks for the elevation range of the area where the eastern sector of the Colorado orogeny extends. I need to find information about the Colorado orogeny, specifically its eastern sector, and then determine the elevation range of that area. I will start by using Wikipedia to get general information about the Colorado orogeny.
Action Planned🛠️: wikipedia
Reason📋: Wikipedia is a good starting point for general information about geological features like the Colorado orogeny.
Input✏️: Colorado orogeny
2. **Action** -> 👉 USING WIKIPEDIA TOOL
3. **Observation** -> 👀 From wikipedia: {...}
4. **Thought** -> 💭 Thought: The Wikipedia article provides information about the Colorado orogeny's timing and location, but it doesn't mention anything about the elevation range of the area it affected, especially the eastern sector. The article mentions that the orogen extends southward into New Mexico, but this doesn't give specific elevation information for the eastern sector. I need to find a source that discusses the geographical extent of the *eastern* sector of the Colorado orogeny and its corresponding elevations. A Google search might help me find more specific information about the eastern sector and its elevation range.
Action Planned🛠️: google
Reason📋: Google search might provide more detailed information about the eastern sector of the Colorado orogeny and its elevation range.
Input✏️: eastern sector Colorado orogeny elevation range

5. **Action** -> 👉 USING GOOGLE TOOL
6. **Observation** -> 👀 From google: {...}
7. **Thought** -> 💭 Thought: The Google search results indicate that the eastern sector of the Colorado orogeny extends into the High Plains. Therefore, to answer the query, I need to determine the elevation range of the High Plains. I will use Google to search for the elevation range of the High Plains.
Action Planned🛠️: google
Reason📋: Google search can provide the elevation range of the High Plains.
Input✏️: elevation range High Plains
8. **Action** -> 👉 USING GOOGLE TOOL
9. **Observation** -> 👀 From google: {...}
10. **Thought** -> 💭 Thought: The Google search results for "elevation range High Plains" provide a range of elevations. The first result from Wikipedia states the High Plains rise in elevation from around 1,500 to 6,000 ft (460 to 1,830 m). The second result from Britannica states the altitude at the base of the Rockies is between 5,000 and 6,000 feet (1,500 and 1,800 metres). The third result from USGS mentions an elevation of about 7,800 feet. I will take the lowest and highest values to provide a comprehensive range. Thus, the elevation range for the area that the eastern sector of the Colorado orogeny extends into is approximately 1,500 to 7,800 feet.
Action Planned🛠️: Unknown
Reason📋: No reason provided
Input✏️: No input provided
11. **Final Answer** -> ✅ FINAL ANSWER: The elevation range for the area that the eastern sector of the Colorado orogeny extends into is approximately 1,500 to 7,800 feet.

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

