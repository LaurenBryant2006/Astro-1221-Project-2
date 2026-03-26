"""
AstroLLMTools
-------------
Bridges AI queries and the analytics engine, providing LLM-powered function tools.

Classes:
    AstroLLMTools

Methods:
    get_observing_story(object_name):
        # Retrieve object data and generate a story using LLM
        pass
    generate_observing_plan(user_profile):
        # Generate a custom observing plan for the user
        pass
    # Additional LLM function tools as required

Data Structures:
    - List[dict]: JSON schemas for LLM function tools
"""
import litellm
import os
from dotenv import load_dotenv

load_dotenv()

class AstroLLMTools:
    """Class to provide LLM-powered tools for observing plans and stories."""
    def __init__(self):
        # Attach these to 'self' so all methods can see them
        self.api_base = "https://litellmproxy.osu-ai.org"
        self.api_key = os.getenv("ASTRO1221_API_KEY")
        self.default_model = "openai/GPT-4.1-mini"
        if not self.api_key:
            print("Warning: ASTRO1221_API_KEY not found in environment!")

    def prompt_llm(self, messages, temperature=0.3, max_tokens=2000):
        # Use the variables attached to self
        response = litellm.completion(
            model=self.default_model,
            messages=messages,
            api_base=self.api_base,
            api_key=self.api_key,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def get_observing_story(self, object_data):
        """Generate a story about a Messier object using LLM."""

        # Pull data for object being described
        messier_id = object_data.get('Name', 'this object')
        obj_type = object_data.get('Class', 'celestial object')
        constellation = object_data.get('Constellation', 'deep sky')
        mag = object_data.get('Magnitude', 'unknown brightness')
        remarks = object_data.get('Remarks', '')
        #actual prompt for llm 
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an astronomy expert helping an astronomer learn more about "
                    "astronomical objects through stories and facts."
                    "Use the provided data to tell an engaging and accurate story"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Tell me the discovery story and lore of {messier_id}."
                    f"Data: it is a {obj_type} in {constellation} with a magnitude of {mag}. "
                    f"additional contect from records {remarks}. "
                    f"please identify it's common name if mentioned in the context"
                )
            },
        ]
        return self.prompt_llm(messages)
    def generate_observing_plan(self, user_profile):
        """generate a custom observing plan for the user profile."""
        # get user specifics 
        profile_details = (
            f"experience level: {user_profile.get('experience_level', 'beginner')}, "
            f"Telescope Aperture: {user_profile.get('aperture_mm', 'unknown')}mm, "
            f"Location: {user_profile.get('location', 'unknown')}, "
            f"Current Season: {user_profile.get('preferred_season', 'Spring')}. "
        )
            #actual prompt for llm 
        messages = [
            {"role": "system", "content": "You are a professional astronomer creating custom viewing guides based on user preferences."},
            {"role": "user", "content": f"create a plan for {profile_details}, include 3 recomended objects as well as tips for their specific viewing gear"}
        ]
        return self.prompt_llm(messages)
     # Additional function tools for LLM as needed
    
if __name__ == "__main__":
    # Test the class
    astro_test = AstroLLMTools()
    
    print("Fetching story for M31...")
    print(astro_test.get_observing_story("Andromeda Galaxy (M31)"))