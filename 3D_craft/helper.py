from dataclasses import dataclass, field
from typing import List, Dict, Any
import os, datetime, json

__all__ = ['Node', 'Constraint', 'SceneGraph', 'save_scene_graph']

@dataclass
class Node:
    id: str
    asset: str
    size: tuple[float, float, float]  # (w, d, h) in metres

@dataclass
class Constraint:
    type: str  # 'left_of', 'front_of', etc.
    a: str
    b: str
    gap: float = 0.0

@dataclass
class SceneGraph:
    nodes: List[Node]
    constraints: List[Constraint]
    room_size: tuple[float, float] = (4.0, 3.0)  # default room (w, d)

    def to_json(self) -> Dict[str, Any]:
        return {
            'nodes': [node.__dict__ for node in self.nodes],
            'constraints': [c.__dict__ for c in self.constraints],
            'room': {'size': self.room_size, 'shape': 'rect'}
        }
    

def save_scene_graph(scene_graph: dict) -> str:
    """Save scene graph to a JSON file and return the filename."""
    # Create directory if it doesn't exist
    os.makedirs('assets/scene-graphs', exist_ok=True)
    
    # Generate filename based on timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'assets/scene-graphs/scene_{timestamp}.json'
    
    # Save scene graph to file
    with open(filename, 'w') as f:
        json.dump(scene_graph, f, indent=2)
    print(f'Scene graph saved to {filename}')
    
    return filename
