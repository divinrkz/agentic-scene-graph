import json
import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class SceneGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def generate_scene_graph(self, 
                            space_type: str,
                           space_dimensions: Dict[str, float],
                           furniture_catalog: Optional[List[Dict]] = None) -> Dict:
        """
        Generate a scene graph using LLM based on room dimensions and optional furniture catalog.
        
        Args:
            space_dimensions: Dict with room dimensions (width, length, height)
            furniture_catalog: Optional list of furniture items with their dimensions
            
        Returns:
            Dict containing the scene graph in a format suitable for Blender
        """
        prompt = self._create_scene_prompt(space_type, space_dimensions, furniture_catalog)
        print(prompt)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a 3D scene layout expert. You must respond with ONLY a valid JSON object that represents a scene graph for a 3D layout in Blender. The response must be a single JSON object with no additional text, markdown formatting, or code blocks. Do not include any explanations or other text."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print(f"Raw response: {response.choices[0].message.content}")
            raise
    
    def _create_scene_prompt(self, 
                            space_type: str,
                           space_dimensions: Dict[str, float],
                           furniture_catalog: Optional[List[Dict]] = None) -> str:
        prompt = f"Create a 3D scene graph for a {space_type} with dimensions: {space_dimensions}\n"
        
        if furniture_catalog:
            prompt += f"Available furniture:\n{json.dumps(furniture_catalog, indent=2)}\n"
        else:
            prompt += "No specific furniture provided. Suggest appropriate furniture based on room dimensions.\n"
            
        prompt += """
        Return a JSON object with a structure that can be used to create a 3D scene in Blender.
        """
        return prompt 