import json
from typing import Dict
from openai import OpenAI
import os

class BlenderCodeGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_blender_code(self, scene_graph: Dict) -> str:
        """
        Generate Blender Python code from a scene graph.
        
        Args:
            scene_graph: Dict containing the scene graph
            
        Returns:
            String containing the Blender Python code
        """
        prompt = self._create_blender_prompt(scene_graph)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Blender Python expert. Generate Python code that can be executed in Blender to create a 3D scene based on the provided scene graph."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    def _create_blender_prompt(self, scene_graph: Dict) -> str:
        """Create the prompt for generating Blender code."""
        prompt = f"""
        Generate Blender Python code to create a 3D scene based on this scene graph:
        {json.dumps(scene_graph, indent=2)}
        
        The code should:
        1. Import necessary Blender modules
        2. Clear the existing scene
        4. Add furniture with proper dimensions, positions, and rotations
        5. Set up materials and lighting
        6. Set up a camera for rendering
        7. Include a function to render the scene
        
        The code should be complete and executable in Blender's Python environment.
        """
        return prompt 