import requests
from .tools.tools4agent import function_definitions
from .tools.perplexity import perplexity_web_search
import asyncio

class LanguageModelWrapper:

    def _parse_function_call(self, response_text):
        """Parse a function call from the model's response"""
        try:
            # Extract function name and parameters
            func_name = response_text.split('(')[0].strip()
            # Extract everything between parentheses
            params_str = response_text[response_text.find('(')+1:response_text.rfind(')')]
            # Parse parameters
            params = {}
            if 'query="' in params_str:  # Handle quoted string parameters
                params['query'] = params_str.split('query="')[1].split('"')[0]
            return func_name, params
        except Exception as e:
            print(f"Error parsing function call: {e}")
            return None, None

    def _execute_function(self, func_name, params):
        """Execute the specified function with given parameters"""
        function_mapping = {
            'perplexity_web_search': perplexity_web_search,
            # Add new functions here as they become available
            # 'another_function': another_function,
        }
        
        if func_name in function_mapping:
            try:
                return function_mapping[func_name](**params)
            except Exception as e:
                print(f"Error executing function {func_name}: {e}")
                return None
        return None


    def generate_response(self, prompt, model="llama3.2:latest"):
        """Send request to local Ollama instance"""
        try:
            # First step: Research prompt
            research_prompt = f"""You are a research assistant.
            Based on the following topic, determine if you need to gather additional information.
            If you do, you can use any of these available functions:

            {function_definitions}

            Format your response exactly like this if you want to call a function:
            FUNCTION: function_name(param_name="param_value")

            If you don't need to gather information, respond with:
            NO_FUNCTION_NEEDED

            Topic: {prompt}
            """

            # Get function call decision
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": research_prompt, "stream": False},
            )
            function_response = response.json()["response"].strip()
            
            research_results = ""

            # Check if function call is needed
            if function_response.startswith("FUNCTION:"):
                function_call = function_response.replace("FUNCTION:", "").strip()
                func_name, params = self._parse_function_call(function_call)
                
                if func_name and params:
                    research_results = self._execute_function(func_name, params)


            # Second step: Tweet generation
            post_prompt = f"""You are Didier Rodrigues Lopes, founder and CEO of OpenBB.
            Write engaging, impactful tweets that reflect my voice and expertise in open source, AI, and finance.

            Tweet Style Guide:
            - Write in a confident, visionary, yet approachable tone
            - Focus on one clear message per tweet
            - Use active voice and present tense
            - Include concrete examples or insights when possible
            - Connect topics to democratizing finance whenever relevant
            - Keep it conversational but professional
            - Maximum 300 characters
            
            Format:
            - No hashtags
            - No quotes
            - No random capitalization
            - No emojis
            - Single clear statement or insight
            
            Focus on themes like:
            - Democratizing financial data and tools
            - The intersection of AI and finance
            - Open source innovation
            - Future of financial technology
            - Market insights and trends"""

            # Add research results if available
            if research_results:
                post_prompt += f"\nHere is the context from research:\n{research_results}"
            
            post_prompt += f"\nTopic: {prompt}\n\nRespond with ONLY the tweet text, nothing else."
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": post_prompt, "stream": False},
            ) 
            return {
                "text": response.json()["response"].strip(),
                "tool_used": func_name if func_name else "",
            }
        
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None
