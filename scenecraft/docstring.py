def import_obj(asset_name: str) -> List[bpy.types.Object]:
    """
    Import an OBJ file into the Blender scene, scale to correct height, rotate to correct angle, move to position and get highest and lowest point.

    Args:
        asset_name (str): Name of the asset to import.

    Returns:
        List[bpy.types.Object]: List of newly imported Blender objects.
        Dict[str, float]: The lowest x, y, and z coordinates.
        Dict[str, float]: The highest x, y, and z coordinates.

    Example:
        asset_dict = {
          "Table": "/Users/ziniu/workspace/assets_all/1019940/table_decor_set.obj"
        }
        height_dict = {
          "Table": 0.8
        }
        location_dict = {
          "Table": [
            10,
            0,
            0
          ]
        }
        rotation_dict = {
          "Table": 180
        }
        imported_objects, lowest_dict, highest_dict = import_obj("Table")
    """
    asset_path = asset_dict[asset_name]
    asset_height = height_dict[asset_name]
    file_path = os.path.join(global_path, asset_path)
    bpy.ops.import_scene.obj(filepath=file_path)
    for obj in bpy.data.objects:
        for k in ['plane_', 'plane.', 'circle', 'floor']:
            if k in obj.name.lower():
                bpy.data.objects.remove(obj, do_unlink=True)
                break
    # Get the new objects
    imported_objects = set(bpy.context.scene.objects) - existing_objects
    existing_objects.update(list(imported_objects))
    # Return the list of new objects
    objs = list(imported_objects)
    
    rotate_objects_z_axis(objs, rotation_dict[asset_name])  
    
    
    lowest_point = find_lowest_vertex_point(objs)
    highest_points = find_highest_vertex_point(objs)
    max_scale = max((highest_points['z'] - lowest_point['z']), (highest_points['x'] - lowest_point['x']) / 10, (highest_points['y'] - lowest_point['y']) / 10)
    normalization_scale = asset_height / max_scale
    for obj in objs:
        obj.matrix_world = obj.matrix_world * normalization_scale
    

    lowest_point = find_lowest_vertex_point(objs)
    highest_points = find_highest_vertex_point(objs)
    
    center_point = {'x': -(lowest_point['x'] + highest_points['x']) / 2, 
                    'y': -(lowest_point['y'] + highest_points['y']) / 2,
                    'z': -lowest_point['z']}
    shift(objs, center_point)
    lowest_point = find_lowest_vertex_point(objs)
    highest_points = find_highest_vertex_point(objs)
    return objs, highest_points, lowest_point

    
def rotate_objects_z_axis(objects: List[bpy.types.Object], angle_degrees: float) -> None:
    """
    Rotate a group of objects around the Z-axis by a given angle.

    Args:
        objects (List[bpy.types.Object]): List of objects to rotate.
        angle_degrees (float): The angle in degrees to rotate.

    Example:
        rotate_objects_z_axis([object1, object2], 45)
    """
   
def shift(objects: List[bpy.types.Object], shift_loc: Dict[str, float]) -> None:
    """
    Shift a group of objects with shift_loc.

    Args:
        objects (List[bpy.types.Object]): List of objects to rotate.
        shift_loc (float): The shift vector.

    Example:
        rotate_objects_z_axis([object1, object2], (5,3,1))
    """
    
def define_proximity_constraint(obj1: bpy.types.Object, obj2: bpy.types.Object, proximity_level: str) -> Tuple[bpy.types.Object, bpy.types.Object, float]:
    """
    Define a proximity constraint between two objects.

    Args:
        obj1 (bpy.types.Object): First object.
        obj2 (bpy.types.Object): Second object.
        proximity_level (str): Level of proximity (e.g., 'close', 'very close', 'on').

    Returns:
        Tuple[bpy.types.Object, bpy.types.Object, float]: A tuple containing both objects and the defined distance.

    Example:
        constraint = define_proximity_constraint(object1, object2, 'close')
    """
   

def apply_constraints(existing_objects: Dict[str, bpy.types.Object], directional_constraints: List[Tuple[str, str, Vector]], proximity_constraints: List[Tuple[str, str, float]], iterations: int = 100, collision_tolerance: float = 1.0) -> None:
    """
    Apply directional and proximity constraints, and resolve collisions iteratively.

    Args:
        existing_objects (Dict[str, bpy.types.Object]): Dictionary of existing objects keyed by their names.
        directional_constraints (List[Tuple[str, str, Vector]]): List of directional constraints.
        proximity_constraints (List[Tuple[str, str, float]]): List of proximity constraints.
        iterations (int, optional): Number of iterations for applying constraints. Defaults to 100.
        collision_tolerance (float, optional): Tolerance for collision detection. Defaults to 1.0.

    Example:
        apply_constraints({'obj1': object1, 'obj2': object2}, 
                          [('obj1', 'obj2', Vector((1,0,0)))], 
                          [('obj1', 'obj2', 2.0)])
    """
    
def adjust_for_mesh_overlap(objs1: list, objs2: list) -> None:
    """
    Adjust the position of a group of objects (objs1) to be just on top of another group (objs2).

    Args:
        objs1 (list): The objects to be placed on top.
        objs2 (list): The objects to be placed under objs1.
    """


def get_all_vertices(objects: List[bpy.types.Object]) -> Set[Vector]:
    """
    Retrieve all vertices from a list of objects, transformed to world coordinates.

    Args:
        objects (List[bpy.types.Object]): List of Blender objects.

    Returns:
        Set[Vector]: A set of vertices in world space.
    """

def check_vertex_overlap(vertices1: Set[Vector], vertices2: Set[Vector], threshold: float = 0.01) -> bool:
    """
    Check if there is any overlap between two sets of vertices within a threshold.

    Args:
        vertices1 (Set[Vector]): First set of vertices.
        vertices2 (Set[Vector]): Second set of vertices.
        threshold (float): Distance threshold to consider as an overlap.

    Returns:
        bool: True if there is an overlap, False otherwise.
    """
   
def calculate_shortest_distance(vertices1: Set[Tuple[float, float, float]], vertices2: Set[Tuple[float, float, float]]) -> float:
    """
    Calculate the shortest distance between two sets of vertices.

    Args:
        vertices1 (Set[Tuple[float, float, float]]): First set of vertices.
        vertices2 (Set[Tuple[float, float, float]]): Second set of vertices.

    Returns:
        float: Shortest distance over the Z-axis.
    """

 

def symmetry_score(assets: List[Layout], axis: str) -> float:
    """
    Calculates a symmetry score for a list of assets along a specified axis.
    
    Args:
    assets (List[Layout]): A list of asset layouts to be evaluated for symmetry.
    axis (str): The axis along which to evaluate symmetry ('x', 'y', or 'z').
    
    Returns:
    float: A score between 0 and 1 indicating the degree of symmetry along the specified axis.
    """


def perpendicularity_score(object1: Layout, object2: Layout) -> float:
    """
    Calculates a score indicating how perpendicular two objects are, based on their forward direction vectors.
    
    Args:
    object1 (Layout): The first object's layout, including its orientation as Euler angles.
    object2 (Layout): The second object's layout, including its orientation as Euler angles.
    
    Returns:
    float: A score between 0 and 1 indicating the degree of perpendicularity.
    """


def calculate_volume(layout: Layout) -> float:
    """Calculate the volume of an object based on its layout dimensions."""


def apply_constraints(existing_objects: Dict[str, bpy.types.Object], directional_constraints: List[Tuple[str, str, Vector]], proximity_constraints: List[Tuple[str, str, float]], iterations: int = 100, collision_tolerance: float = 1.0) -> None:
    """
    Apply directional and proximity constraints, and resolve collisions iteratively.

    Args:
        existing_objects (Dict[str, bpy.types.Object]): Dictionary of existing objects keyed by their names.
        directional_constraints (List[Tuple[str, str, Vector]]): List of directional constraints.
        proximity_constraints (List[Tuple[str, str, float]]): List of proximity constraints.
        iterations (int, optional): Number of iterations for applying constraints. Defaults to 100.
        collision_tolerance (float, optional): Tolerance for collision detection. Defaults to 1.0.

    Example:
        apply_constraints({'obj1': object1, 'obj2': object2}, 
                          [('obj1', 'obj2', Vector((1,0,0)))], 
                          [('obj1', 'obj2', 2.0)])
    """
    
def adjust_for_mesh_overlap(objs1: list, objs2: list) -> None:
    """
    Adjust the position of a group of objects (objs1) to be just on top of another group (objs2).

    Args:
        objs1 (list): The objects to be placed on top.
        objs2 (list): The objects to be placed under objs1.
    """

    
    
def get_all_vertices(objects: List[bpy.types.Object]) -> Set[Vector]:
    """
    Retrieve all vertices from a list of objects, transformed to world coordinates.

    Args:
        objects (List[bpy.types.Object]): List of Blender objects.

    Returns:
        Set[Vector]: A set of vertices in world space.
    """
    
    
def check_vertex_overlap(vertices1: Set[Vector], vertices2: Set[Vector], threshold: float = 0.01) -> float:
    """
    Check if there is any overlap between two sets of vertices within a threshold.

    Args:
        vertices1 (Set[Vector]): First set of vertices.
        vertices2 (Set[Vector]): Second set of vertices.
        threshold (float): Distance threshold to consider as an overlap.

    Returns:
        bool: True if there is an overlap, False otherwise.
    """
    
    
def evaluate_constraints(assets, constraints):
    """Evaluate all constraints and return the overall score."""
    
def adjust_positions(assets, adjustment_step=0.1):
    """Randomly adjust the positions of assets."""
    
    
def constraint_solving(assets, constraints, max_iterations=100):
    """Find an optimal layout of assets to maximize the score defined by constraints."""
    
    
def calculate_shortest_distance(vertices1: Set[Tuple[float, float, float]], vertices2: Set[Tuple[float, float, float]]) -> float:
    """
    Calculate the shortest distance between two sets of vertices.

    Args:
        vertices1 (Set[Tuple[float, float, float]]): First set of vertices.
        vertices2 (Set[Tuple[float, float, float]]): Second set of vertices.

    Returns:
        float: Shortest distance over the Z-axis.
    """
    
def evaluate_hierarchy(assets: List[Layout], expected_order: List[str]) -> float:
    """
    Evaluates how well a list of objects follows a specified hierarchical order based on size.
    
    Args:
    assets (List[Layout]): A list of asset layouts to be evaluated.
    expected_order (List[str]): A list of identifiers (names) for the assets, specifying the expected order of sizes.
    
    Returns:
    float: A metric indicating how well the actual sizes of the objects match the expected hierarchical order.
    """    
    
def calculate_angle_from_center(center: Tuple[float, float, float], object_location: Tuple[float, float, float]) -> float:
    """Calculate the angle of an object relative to a central point."""
    
def rotation_uniformity_score(objects: List[Layout], center: Tuple[float, float, float]) -> float:
    """
    Calculates how uniformly objects are distributed around a central point in terms of rotation.
    
    Args:
    objects (List[Layout]): A list of object layouts to be evaluated.
    center (Tuple[float, float, float]): The central point around which objects are rotating.
    
    Returns:
    float: A score between 0 and 1 indicating the uniformity of object distribution around the center.
    """

def put_ontop(obj_dict, moving_set_name, target_set_name, threshold, step):
    """
    Adjust objects in moving_set_name until the shortest distance to target_set_name is below the threshold.

    Args:
        obj_dict (dict): Dictionary of object sets.
        moving_set_name (str): The key for the set of objects to move.
        target_set_name (str): The key for the set of objects to calculate distance to.
        threshold (float): The distance threshold.
        step (float): The step by which to move objects in the Z direction.
    """
       