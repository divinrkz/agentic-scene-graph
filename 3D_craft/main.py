import os
import tempfile
import subprocess
from typing import Dict, List, Optional
from scene.generator import SceneGenerator
from blender.generator import BlenderCodeGenerator
from blender.utils import run_blender_script, create_blender_script

class SceneCraft:
    def __init__(self):
        self.scene_generator = SceneGenerator()
        self.blender_generator = BlenderCodeGenerator()
    
    def generate_scene(self,
                      space_type: str,
                      space_dimensions: Dict[str, float],
                      furniture_catalog: Optional[List[Dict]] = None,
                      output_path: str = "rendered_scene.blend") -> str:
        """
        Generate a 3D scene and render it.
        
        Args:
            space_type: Type of space (e.g., "Bed Room", "Living Room")
            space_dimensions: Dict with room dimensions (width, length, height)
            furniture_catalog: Optional list of furniture items with their dimensions
            output_path: Path where the rendered image should be saved
            
        Returns:
            Path to the rendered image
        """
        # Generate scene graph
        scene_graph = self.scene_generator.generate_scene_graph(
            space_type,
            space_dimensions,
            furniture_catalog
        )
        print("Generated scene graph:", scene_graph)
        
        # Create Blender script
        blender_script = create_blender_script({
            'width': space_dimensions['width'],
            'length': space_dimensions['length'],
            'height': space_dimensions['height'],
            'furniture': scene_graph.get('furniture', []),
            'output_path': output_path
        })
        
        print("Running Blender Script ... ")
        result = run_blender_script(blender_script, output_path)
        
        if not result['success']:
            print("Error running Blender script:")
            print(result['stderr'])
            raise RuntimeError("Failed to render scene")
            
        return output_path

def main():
    scene_craft = SceneCraft()
    
    room_dimensions = {
        "width": 4.0,  # meters
        "length": 5.0,  # meters
        "height": 2.7  # meters
    }
    
    furniture_catalog = [
        {
            "type": "bed",
            "dimensions": {
                "width": 1.6,
                "length": 2.0,
                "height": 0.5
            }
        },
        {
            "type": "desk",
            "dimensions": {
                "width": 1.2,
                "length": 0.6,
                "height": 0.75
            }
        }
    ]
    
    # Generate and render scene
    output_path = scene_craft.generate_scene(
        space_type="Bed Room",
        space_dimensions=room_dimensions,
        furniture_catalog=furniture_catalog,
        output_path="rendered_scene.blend"
    )
    print(f"Scene rendered to: {output_path}")

if __name__ == "__main__":
    main() 