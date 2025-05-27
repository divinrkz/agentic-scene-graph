import os
import subprocess
import tempfile
from typing import Optional, List, Dict

def run_blender_script(script_content: str, 
                      output_path: Optional[str] = None,
                      blender_path: Optional[str] = None) -> Dict:
    """
    Run a Python script in Blender.
    
    Args:
        script_content: The Python script to run in Blender
        output_path: Optional path to save the rendered image
        blender_path: Optional path to Blender executable. If None, will try to find it.
        
    Returns:
        Dict containing the execution result
    """
    # Try to find Blender if path not provided
    if blender_path is None:
        # Common Blender paths
        blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
                
        if blender_path is None:
            raise FileNotFoundError("Could not find Blender executable. Please install Blender and try again.")

    # Create a temporary file for the script
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
        temp_file.write(script_content.encode())
        temp_file_path = temp_file.name

    try:
        cmd = [
            blender_path,
            '--background', 
            '--python', temp_file_path
        ]
        
        if output_path:
            cmd.extend(['--', '--output', output_path])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'stdout': e.stdout,
            'stderr': e.stderr,
            'error': str(e)
        }
        
    finally:
        os.unlink(temp_file_path)


def generate_furniture_code(furniture_list: List[Dict]) -> str:
    """
    Generate Blender Python code for creating furniture.
    Args:
        furniture_list: List of furniture items with their properties 
    Returns:
        String containing the Blender Python code for creating furniture
    """
    code = []
    for item in furniture_list:
        code.append(f"""
    # Create {item['type']}
    bpy.ops.mesh.primitive_cube_add()
    {item['type']} = bpy.context.active_object
    {item['type']}.scale = ({item['dimensions']['width']}, {item['dimensions']['length']}, {item['dimensions']['height']})
    {item['type']}.location = ({item['position']['x']}, {item['position']['y']}, {item['position']['z']})
    {item['type']}.rotation_euler = (0, 0, {item.get('rotation', 0)})
""")
    return "\n".join(code) 