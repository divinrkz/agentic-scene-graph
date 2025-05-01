import bpy
import bmesh
from mathutils import Vector, Matrix
import os
import math
import mathutils
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

global_path = "/Users/ziniu/workspace/assets/"
# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete the selected objects
bpy.ops.object.delete()


@dataclass
class Layout:
    location: Tuple[float, float, float]
    min: Tuple[float, float, float]
    max: Tuple[float, float, float]
    orientation: Tuple[float, float, float]  # Assuming Euler angles (pitch, yaw, roll)

def import_obj(asset_name: str) -> List[bpy.types.Object]:
    """
    Import an OBJ file into the Blender scene.

    Args:
        asset_name (str): Name of the asset to import.

    Returns:
        List[bpy.types.Object]: List of newly imported Blender objects.
        Dict[str, float]: The lowest x, y, and z coordinates.
        Dict[str, float]: The highest x, y, and z coordinates.

    Example:
        imported_objects = import_obj("example.obj")
    """
    asset_path = asset_dict[asset_name]
    asset_height = layout_dict[asset_name]['height']
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
    
    rotate_objects_z_axis(objs, layout_dict[asset_name]['rotation'])  
    
    
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


def add_camera(location: Tuple[float, float, float], target_point: Tuple[float, float, float], lens: float = 35) -> bpy.types.Object:
    """
    Add a camera to the Blender scene.

    Args:
        location (Vector): The location to place the camera.
        target_point (Vector): The point the camera should be aimed at.
        lens (float, optional): The lens size. Defaults to 35.

    Returns:
        bpy.types.Object: The created camera object.

    Example:
        camera = add_camera((10, 10, 10), (0, 0, 0))
    """
    # Create a new camera data object
    cam_data = bpy.data.cameras.new(name="Camera")
    cam_data.lens = lens  # Set the lens property

    # Create a new camera object and link it to the scene
    cam_object = bpy.data.objects.new('Camera', cam_data)
    bpy.context.collection.objects.link(cam_object)

    # Set the camera location
    cam_object.location = location

    # Calculate the direction vector from the camera to the target point
    direction = Vector(target_point) - Vector(location)
    # Orient the camera to look at the target point
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam_object.rotation_euler = rot_quat.to_euler()

    # Set the created camera as the active camera in the scene
    bpy.context.scene.camera = cam_object

    return cam_object



def scale_group(objects: List[bpy.types.Object], scale_factor: float) -> None:
    """
    Scale a group of objects by a given factor.

    Args:
        objects (List[bpy.types.Object]): List of Blender objects to scale.
        scale_factor (float): The scale factor to apply.

    Example:
        scale_group([object1, object2], 1.5)
    """
    for obj in objects:
        obj.scale = (obj.scale.x * scale_factor, 
                     obj.scale.y * scale_factor, 
                     obj.scale.z * scale_factor)
        obj.matrix_world = obj.matrix_world * scale_factor


def render_scene(output_path: str) -> None:
    """
    Render the current Blender scene.

    Args:
        output_path (str): File path where the rendered image will be saved.

    Example:
        render_scene("/path/to/save/render.png")
    """
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_path
    r = bpy.context.scene.render
    r.resolution_x = 224
    r.resolution_y = 224
    # Render the scene
    bpy.ops.render.render(write_still=True)


def add_light(location: Vector, energy: float = 500, light_type: str = 'SUN') -> bpy.types.Object:
    """
    Add a light to the Blender scene.

    Args:
        location (Vector): The location to place the light.
        energy (float, optional): The energy of the light. Defaults to 10000.
        light_type (str, optional): Type of the light ('POINT', 'SUN', etc.). Defaults to 'POINT'.

    Returns:
        bpy.types.Object: The created light object.

    Example:
        light = add_light(Vector((5, 5, 5)), 5000, 'SUN')
    """
    light_data = bpy.data.lights.new(name="Light", type=light_type)
    light_data.energy = energy  # Set the energy of the light

    # Create a new light object
    light_object = bpy.data.objects.new(name="Light", object_data=light_data)
    bpy.context.collection.objects.link(light_object)

    # Set the location of the light
    light_object.location = location

    return light_object

def find_lowest_vertex_point(objs: List[bpy.types.Object]) -> Dict[str, float]:
    """
    Find the lowest vertex point among a list of objects.

    Args:
        objs (List[bpy.types.Object]): List of Blender objects to evaluate.

    Returns:
        Dict[str, float]: The lowest x, y, and z coordinates.

    Example:
        lowest_point = find_lowest_vertex_point([object1, object2])
    """
    bpy.context.view_layer.update()
    lowest_points = {'x': float('inf'), 'y': float('inf'), 'z': float('inf')}

    for obj in objs:
        # Apply the object's current transformation to its vertices
        obj_matrix_world = obj.matrix_world

        if obj.type == 'MESH':
            # Update mesh to the latest data
            obj.data.update()
            for vertex in obj.data.vertices:
                world_vertex = obj_matrix_world @ vertex.co
                lowest_points['x'] = min(lowest_points['x'], world_vertex.x)
                lowest_points['y'] = min(lowest_points['y'], world_vertex.y)
                lowest_points['z'] = min(lowest_points['z'], world_vertex.z)
        
    return lowest_points


def find_highest_vertex_point(objs: List[bpy.types.Object]) -> Dict[str, float]:
    """
    Find the highest vertex point among a list of objects.

    Args:
        objs (List[bpy.types.Object]): List of Blender objects to evaluate.

    Returns:
        Dict[str, float]: The lowest x, y, and z coordinates.

    Example:
        lowest_point = find_lowest_vertex_point([object1, object2])
    """
    bpy.context.view_layer.update()
    highest_points = {'x': -float('inf'), 'y': -float('inf'), 'z': -float('inf')}

    for obj in objs:
        # Apply the object's current transformation to its vertices
        obj_matrix_world = obj.matrix_world

        if obj.type == 'MESH':
            # Update mesh to the latest data
            obj.data.update()
            for vertex in obj.data.vertices:
                world_vertex = obj_matrix_world @ vertex.co
                highest_points['x'] = max(highest_points['x'], world_vertex.x)
                highest_points['y'] = max(highest_points['y'], world_vertex.y)
                highest_points['z'] = max(highest_points['z'], world_vertex.z)
        
    return highest_points



def rotate_objects_z_axis(objects: List[bpy.types.Object], angle_degrees: float) -> None:
    """
    Rotate a group of objects around the Z-axis by a given angle.

    Args:
        objects (List[bpy.types.Object]): List of objects to rotate.
        angle_degrees (float): The angle in degrees to rotate.

    Example:
        rotate_objects_z_axis([object1, object2], 45)
    """
    bpy.context.view_layer.update()
    angle_radians = math.radians(angle_degrees)  # Convert angle to radians
    rotation_matrix = mathutils.Matrix.Rotation(angle_radians, 4, 'Y')
    lowest_point = find_lowest_vertex_point(objects)
    highest_points = find_highest_vertex_point(objects)
    center_point = {'x': (lowest_point['x'] + highest_points['x']) / 2, 
                    'y': (lowest_point['y'] + highest_points['y']) / 2,
                    'z': 0}
    for obj in objects:
        if obj.type == 'MESH':
            obj.data.update()
            obj.matrix_world = obj.matrix_world @ rotation_matrix
            
    lowest_point = find_lowest_vertex_point(objects)
    highest_points = find_highest_vertex_point(objects)
    center_point['x'] -= (lowest_point['x'] + highest_points['x']) / 2 
    center_point['y'] -= (lowest_point['y'] + highest_points['y']) / 2 
    shift(objects, center_point)
    
def shift(objects: List[bpy.types.Object], shift_loc: Dict[str, float]) -> None:
    """
    Shift a group of objects with shift_loc.

    Args:
        objects (List[bpy.types.Object]): List of objects to rotate.
        shift_loc (float): The shift vector.

    Example:
        rotate_objects_z_axis([object1, object2], (5,3,1))
    """
    for obj in objects:
        # Shift object so the lowest point is at (0,0,0)
        obj.location.x += shift_loc['x']
        obj.location.y += shift_loc['y']
        obj.location.z += shift_loc['z']
    bpy.context.view_layer.update()

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
    proximity_map = {
        'close': 3.0,             # Example distance for 'close'
        'very close': 1.0,        # Example distance for 'very close'
        'on': 0.0,                # Overlapping or touching
        'moderate': 5.0,          # Moderate distance
        'distant': 10.0,          # Distant but in the same scene
        # Add more options as needed
    }

    distance = proximity_map.get(proximity_level, 3.0)  # Default to 'close' if level is undefined

    return (obj1, obj2, distance)


def euler_to_forward_vector(orientation: Tuple[float, float, float]) -> np.ndarray:
    """Convert Euler angles to a forward direction vector."""
    pitch, yaw, _ = orientation
    # Assuming the angles are in radians
    x = np.cos(yaw) * np.cos(pitch)
    y = np.sin(yaw) * np.cos(pitch)
    z = np.sin(pitch)
    return np.array([x, y, z])

def calculate_vector(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> np.ndarray:
    """Calculate the directional vector from point a to b."""
    return np.array(b) - np.array(a)

def direction_score(object1: Layout, object2: Layout) -> float:
    """
    Calculates a score indicating how directly object1 is targeting object2.
    
    Args:
    object1 (Layout): The first object's layout, assumed to be the one doing the targeting.
    object2 (Layout): The second object's layout, assumed to be the target.
    
    Returns:
    float: A score between 0 and 1 indicating the directionality of object1 towards object2.
    """
    forward_vector = euler_to_forward_vector(object1.orientation)
    target_vector = calculate_vector(object1.location, object2.location)
    # Normalize vectors to ensure the dot product calculation is based only on direction
    forward_vector_normalized = normalize_vector(forward_vector)
    target_vector_normalized = normalize_vector(target_vector)
    # Calculate the cosine of the angle between the two vectors
    cos_angle = np.dot(forward_vector_normalized, target_vector_normalized)
    # Map the cosine range [-1, 1] to a score range [0, 1]
    score = (cos_angle + 1) / 2
    return score

def alignment_score(assets: List[Layout], axis: str) -> float:
    """
    Calculates an alignment score for a list of assets along a specified axis.
    
    Args:
    assets (List[Layout]): A list of asset layouts to be evaluated for alignment.
    axis (str): The axis along which to evaluate alignment ('x', 'y', or 'z').
    
    Returns:
    float: A score between 0 and 1 indicating the degree of alignment along the specified axis.
    """
    if not assets or axis not in ['x', 'y', 'z']:
        return 0.0  # Return a score of 0 for invalid input
    
    # Axis index mapping to the location tuple
    axis_index = {'x': 0, 'y': 1, 'z': 2}[axis]
    
    # Extract the relevant coordinate for each asset based on the chosen axis
    coordinates = [asset.location[axis_index] for asset in assets]
    # Calculate the variance of these coordinates
    variance = np.var(coordinates)
    # Inverse the variance to calculate the score, assuming a lower variance indicates better alignment
    # Normalize the score to be between 0 and 1, considering a reasonable threshold for "perfect" alignment
    threshold_variance = 1.0  # Define a threshold variance for "perfect" alignment
    score = 1 / (1 + variance / threshold_variance)
    # Clamp the score between 0 and 1
    score = max(0, min(score, 1))
    return score
    
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
    for v1_tuple in vertices1:
        v1 = Vector(v1_tuple)
        for v2_tuple in vertices2:
            v2 = Vector(v2_tuple)
            if (v1 - v2).length <= threshold:
                return 0.0
    return 1.0



def normalize_vector(v: np.ndarray) -> np.ndarray:
    """Normalize a vector."""
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else np.zeros_like(v)

def orientation_similarity(orientation1: Tuple[float, float, float], orientation2: Tuple[float, float, float]) -> float:
    """Calculate the similarity between two orientations, represented as Euler angles."""
    # Convert Euler angles to vectors for simplicity in comparison
    vector1 = np.array(orientation1)
    vector2 = np.array(orientation2)
    # Calculate the cosine similarity between the two orientation vectors
    cos_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    return cos_similarity

def parallelism_score(assets: List[Layout]) -> float:
    """
    Evaluates and returns a score indicating the degree of parallelism in a list of assets' layouts, considering both position and orientation.
    
    Args:
    assets (List[Layout]): A list of asset layouts.
    
    Returns:
    float: A score between 0 and 1 indicating the parallelism of the assets.
    """
    if len(assets) < 2:
        return 1.0  # Single asset or no asset is arbitrarily considered perfectly parallel
    
    # Positional parallelism
    vectors = [calculate_vector(assets[i].location, assets[i+1].location) for i in range(len(assets)-1)]
    normalized_vectors = [normalize_vector(v) for v in vectors]
    dot_products_position = [np.dot(normalized_vectors[i], normalized_vectors[i+1]) for i in range(len(normalized_vectors)-1)]
    
    # Rotational similarity
    orientation_similarities = [orientation_similarity(assets[i].orientation, assets[i+1].orientation) for i in range(len(assets)-1)]
    
    # Combine scores
    position_score = np.mean([0.5 * (dot + 1) for dot in dot_products_position])
    orientation_score = np.mean([(similarity + 1) / 2 for similarity in orientation_similarities])
    
    # Average the position and orientation scores for the final score
    final_score = (position_score + orientation_score) / 2
    
    return final_score


def calculate_distance(location1: Tuple[float, float, float], location2: Tuple[float, float, float]) -> float:
    """Calculate the Euclidean distance between two points."""
    return np.linalg.norm(np.array(location1) - np.array(location2))



def symmetry_score(assets: List[Layout], axis: str) -> float:
    """
    Calculates a symmetry score for a list of assets along a specified axis.
    
    Args:
    assets (List[Layout]): A list of asset layouts to be evaluated for symmetry.
    axis (str): The axis along which to evaluate symmetry ('x', 'y', or 'z').
    
    Returns:
    float: A score between 0 and 1 indicating the degree of symmetry along the specified axis.
    """
    if not assets or axis not in ['x', 'y', 'z']:
        return 0.0  # Return a score of 0 for invalid input
    
    # Axis index mapping to the location tuple
    axis_index = {'x': 0, 'y': 1, 'z': 2}[axis]
    
    # Find the median coordinate along the specified axis to define the symmetry axis
    coordinates = [asset.location[axis_index] for asset in assets]
    symmetry_axis = np.median(coordinates)
    
    # Calculate the deviation from symmetry for each asset
    deviations = []
    for asset in assets:
        # Find the mirrored coordinate across the symmetry axis
        mirrored_coordinate = 2 * symmetry_axis - asset.location[axis_index]
        # Find the closest asset to this mirrored coordinate
        closest_distance = min(abs(mirrored_coordinate - other.location[axis_index]) for other in assets)
        deviations.append(closest_distance)
    
    # Calculate the average deviation from perfect symmetry
    avg_deviation = np.mean(deviations)
    
    # Convert the average deviation to a score, assuming smaller deviations indicate better symmetry
    # The scoring formula can be adjusted based on the specific requirements for symmetry in the application
    max_deviation = 10.0  # Define a maximum deviation for which the score would be 0
    score = max(0, 1 - avg_deviation / max_deviation)
    
    return score

def perpendicularity_score(object1: Layout, object2: Layout) -> float:
    """
    Calculates a score indicating how perpendicular two objects are, based on their forward direction vectors.
    
    Args:
    object1 (Layout): The first object's layout, including its orientation as Euler angles.
    object2 (Layout): The second object's layout, including its orientation as Euler angles.
    
    Returns:
    float: A score between 0 and 1 indicating the degree of perpendicularity.
    """
    vector1 = euler_to_forward_vector(object1.orientation)
    vector2 = euler_to_forward_vector(object2.orientation)
    cos_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
    score = 1 - np.abs(cos_angle)
    return score

def calculate_volume(layout: Layout) -> float:
    """Calculate the volume of an object based on its layout dimensions."""
    length = abs(layout.max[0] - layout.min[0])
    width = abs(layout.max[1] - layout.min[1])
    height = abs(layout.max[2] - layout.min[2])
    return length * width * height

        

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
    for iteration in range(iterations):
        # Apply directional constraints
        for obj1_name, obj2_name, direction in directional_constraints:
            obj1 = existing_objects.get(obj1_name)
            obj2 = existing_objects.get(obj2_name)
            if obj1 and obj2:
                obj2.location = obj1.location + mathutils.Vector(direction)

        # Apply proximity constraints
        for obj1_name, obj2_name, desired_distance in proximity_constraints:
            obj1 = existing_objects.get(obj1_name)
            obj2 = existing_objects.get(obj2_name)
            if obj1 and obj2:
                direction = (obj2.location - obj1.location).normalized()
                obj2.location = obj1.location + direction * desired_distance

        # Collision detection and resolution
        for obj1 in existing_objects.values():
            for obj2 in existing_objects.values():
                if obj1 != obj2:
                    distance = (obj2.location - obj1.location).length
                    if distance < collision_tolerance:
                        # Adjust position to resolve collision
                        collision_direction = (obj2.location - obj1.location).normalized()
                        adjustment_distance = collision_tolerance - distance
                        obj2.location += collision_direction * adjustment_distance


def adjust_for_mesh_overlap(objs1: list, objs2: list) -> None:
    """
    Adjust the position of a group of objects (objs1) to be just on top of another group (objs2).

    Args:
        objs1 (list): The objects to be placed on top.
        objs2 (list): The objects to be placed under objs1.
    """

    def get_combined_world_bound_box(objs):
        """ Get the combined bounding box of a list of objects in world coordinates. """
        world_bbox_points = []
        for obj in objs:
            local_bbox = [mathutils.Vector(corner) for corner in obj.bound_box]
            world_bbox = [obj.matrix_world @ corner for corner in local_bbox]
            world_bbox_points.extend(world_bbox)
        return world_bbox_points

    def get_box_extents(bbox):
        """ Get the min and max Z extents of a bounding box. """
        z_coords = [v.z for v in bbox]
        return min(z_coords), max(z_coords)

    bbox_obj1 = get_combined_world_bound_box(objs1)
    bbox_obj2 = get_combined_world_bound_box(objs2)

    min_z_obj1, _ = get_box_extents(bbox_obj1)
    _, max_z_obj2 = get_box_extents(bbox_obj2)

    distance_to_move = max_z_obj2 - min_z_obj1
    for obj in objs1:
        obj.location.z += distance_to_move



def get_all_vertices(objects: List[bpy.types.Object]) -> Set[Vector]:
    """
    Retrieve all vertices from a list of objects, transformed to world coordinates.

    Args:
        objects (List[bpy.types.Object]): List of Blender objects.

    Returns:
        Set[Vector]: A set of vertices in world space.
    """
    vertices = set()
    for obj in objects:
        obj.update_from_editmode()  # Update the object's data
        world_matrix = obj.matrix_world
        for vertex in obj.data.vertices:
            world_vertex = world_matrix @ vertex.co
            vertices.add(tuple(world_vertex))  # Convert Vector to tuple
    return vertices


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
    for v1_tuple in vertices1:
        v1 = Vector(v1_tuple)
        for v2_tuple in vertices2:
            v2 = Vector(v2_tuple)
            if (v1 - v2).length <= threshold:
                return 1.0
    return 0.0
    
def evaluate_constraints(assets, constraints):
    """Evaluate all constraints and return the overall score."""
    total_score = 0
    for constraint_func, involved_assets in constraints:
        # Assuming each constraint function takes involved assets and returns a score
        scores = constraint_func([assets[name] for name in involved_assets])
        total_score += sum(scores)  # Summing scores assuming each constraint can contribute multiple scores
    return total_score

def adjust_positions(assets, adjustment_step=0.1):
    """Randomly adjust the positions of assets."""
    for asset in assets.values():
        # Randomly adjust position within a small range to explore the space
        asset.location = (
            asset.location[0] + random.uniform(-adjustment_step, adjustment_step),
            asset.location[1] + random.uniform(-adjustment_step, adjustment_step),
            asset.location[2]  # Z position kept constant for simplicity
        )

def constraint_solving(assets, constraints, max_iterations=100):
    """Find an optimal layout of assets to maximize the score defined by constraints."""
    best_score = evaluate_constraints(assets, constraints)
    best_layout = {name: asset.copy() for name, asset in assets.items()}  # Assuming a copy method exists

    for _ in range(max_iterations):
        adjust_positions(assets)
        current_score = evaluate_constraints(assets, constraints)
        
        if current_score > best_score:
            best_score = current_score
            best_layout = {name: asset.copy() for name, asset in assets.items()}
        else:
            # Revert to best layout if no improvement
            assets = {name: layout.copy() for name, layout in best_layout.items()}

    return best_layout, best_score

def calculate_shortest_distance(vertices1: Set[Tuple[float, float, float]], vertices2: Set[Tuple[float, float, float]]) -> float:
    """
    Calculate the shortest distance between two sets of vertices.

    Args:
        vertices1 (Set[Tuple[float, float, float]]): First set of vertices.
        vertices2 (Set[Tuple[float, float, float]]): Second set of vertices.

    Returns:
        float: Shortest distance over the Z-axis.
    """
    min_distance = float('inf')
    for v1_tuple in vertices1:
        v1 = Vector(v1_tuple)
        for v2_tuple in vertices2:
            v2 = Vector(v2_tuple)
            distance = (v1 - v2).length
            min_distance = min(min_distance, distance)
    return min_distance





def evaluate_hierarchy(assets: List[Layout], expected_order: List[str]) -> float:
    """
    Evaluates how well a list of objects follows a specified hierarchical order based on size.
    
    Args:
    assets (List[Layout]): A list of asset layouts to be evaluated.
    expected_order (List[str]): A list of identifiers (names) for the assets, specifying the expected order of sizes.
    
    Returns:
    float: A metric indicating how well the actual sizes of the objects match the expected hierarchical order.
    """
    # Map identifiers to volumes
    id_to_volume = {asset_id: calculate_volume(asset) for asset_id, asset in zip(expected_order, assets)}
    
    # Calculate the actual order based on sizes
    actual_order = sorted(id_to_volume.keys(), key=lambda x: id_to_volume[x], reverse=True)
    
    # Evaluate the match between the expected and actual orders
    correct_positions = sum(1 for actual, expected in zip(actual_order, expected_order) if actual == expected)
    total_positions = len(expected_order)
    
    # Calculate the match percentage as a measure of hierarchy adherence
    match_percentage = correct_positions / total_positions
    
    return match_percentage


def calculate_angle_from_center(center: Tuple[float, float, float], object_location: Tuple[float, float, float]) -> float:
    """Calculate the angle of an object relative to a central point."""
    vector = np.array(object_location) - np.array(center)
    angle = np.arctan2(vector[1], vector[0])
    return angle

def rotation_uniformity_score(objects: List[Layout], center: Tuple[float, float, float]) -> float:
    """
    Calculates how uniformly objects are distributed around a central point in terms of rotation.
    
    Args:
    objects (List[Layout]): A list of object layouts to be evaluated.
    center (Tuple[float, float, float]): The central point around which objects are rotating.
    
    Returns:
    float: A score between 0 and 1 indicating the uniformity of object distribution around the center.
    """
    angles = [calculate_angle_from_center(center, obj.location) for obj in objects]
    angles = np.sort(np.mod(angles, 2*np.pi))  # Normalize angles to [0, 2\pi] and sort
    
    # Calculate differences between consecutive angles, including wrap-around difference
    angle_diffs = np.diff(np.append(angles, angles[0] + 2*np.pi))
    
    # Evaluate uniformity as the variance of these differences
    variance = np.var(angle_diffs)
    uniformity_score = 1 / (1 + variance)  # Inverse variance, higher score for lower variance
    
    return uniformity_score

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
    while True:
        vertices_set1 = get_all_vertices(obj_dict[moving_set_name])
        vertices_set2 = get_all_vertices(obj_dict[target_set_name])
        shortest_distance = calculate_shortest_distance(vertices_set1, vertices_set2)
        print(shortest_distance)

        if shortest_distance < threshold:
            break

        for obj in obj_dict[moving_set_name]:
            obj.location.z -= max(step, shortest_distance)

        bpy.context.view_layer.update()
    

def add_sandland(): 
    
    # Load the texture image
    texture_image_path = '/Users/ziniu/workspace/assets_all/600852/Sand_t.jpg'
    image_texture = bpy.data.images.load(texture_image_path)

    # Create a new material with the texture
    material = bpy.data.materials.new(name="SandMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')

    # Add texture image node
    tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = image_texture

    # Add texture coordinate and mapping nodes
    tex_coord = material.node_tree.nodes.new('ShaderNodeTexCoord')
    mapping = material.node_tree.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (10, 10, 10)  # Adjust the scale as needed

    # Link nodes
    material.node_tree.links.new(mapping.inputs['Vector'], tex_coord.outputs['Object'])
    material.node_tree.links.new(tex_image.inputs['Vector'], mapping.outputs['Vector'])
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

    # Create a plane and scale it
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.scale.x = 500
    plane.scale.y = 500

    # Apply the material to the plane
    plane.data.materials.append(material)

    # Update scene
    bpy.context.view_layer.update()
            
      