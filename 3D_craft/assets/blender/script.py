import bpy
from mathutils import Vector

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Add camera
cam_data = bpy.data.cameras.new(name='Camera')
cam_data.lens = 35
cam_object = bpy.data.objects.new('Camera', cam_data)
bpy.context.collection.objects.link(cam_object)
cam_object.location = (2.0, -3.0, 3.5999999999999996)

# Point camera at room center
direction = Vector((2.0, 1.0, 1.5)) - Vector((2.0, -3.0, 3.5999999999999996))
rot_quat = direction.to_track_quat('-Z', 'Y')
cam_object.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam_object

# Lighting
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
bpy.context.active_object.data.energy = 2.0

# Render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Create floor
bpy.ops.mesh.primitive_cube_add(location=(2.0, 1.0, -0.05))
floor = bpy.context.active_object
floor.name = 'Floor'
floor.scale = (2.0, 1.0, 0.05)

# Create walls
bpy.ops.mesh.primitive_cube_add(location=(0, 0.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_1'
wall.scale = (0.1, 0.0, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(2.0, 0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_2'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(4, 0.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_3'
wall.scale = (0.1, 0.0, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(2.0, 0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_4'
wall.scale = (2.0, 0.1, 1.5)

# Add furniture
# bed_1 - bed
bpy.ops.mesh.primitive_cube_add(location=(1.20, 0.50, 0.40))
obj = bpy.context.active_object
obj.name = 'bed_1'
obj.scale = (0.80, 1.00, 0.40)
obj.rotation_euler = (0, 90, 0)

# desk_1 - desk
bpy.ops.mesh.primitive_cube_add(location=(2.70, 1.70, 0.40))
obj = bpy.context.active_object
obj.name = 'desk_1'
obj.scale = (0.70, 0.40, 0.40)
obj.rotation_euler = (0, 180, 0)

# lamp_1 - lighting
bpy.ops.mesh.primitive_cube_add(location=(1.90, 1.70, 0.25))
obj = bpy.context.active_object
obj.name = 'lamp_1'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# Create materials
# Material: wall_material
mat = bpy.data.materials.new(name='wall_material')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
# Use input names instead of indices for better compatibility
bsdf.inputs['Base Color'].default_value = (1.000, 1.000, 1.000, 1.0)
bsdf.inputs['Roughness'].default_value = 0.5

# Material: floor_material
mat = bpy.data.materials.new(name='floor_material')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
# Use input names instead of indices for better compatibility
bsdf.inputs['Base Color'].default_value = (0.490, 0.490, 0.490, 1.0)
bsdf.inputs['Roughness'].default_value = 0.5

# Apply materials
floor = bpy.data.objects.get('Floor')
if floor and 'floor_material' in bpy.data.materials:
    floor.data.materials.append(bpy.data.materials['floor_material'])

wall = bpy.data.objects.get('wall_1')
if wall and 'wall_material' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wall_material'])

wall = bpy.data.objects.get('wall_2')
if wall and 'wall_material' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wall_material'])

wall = bpy.data.objects.get('wall_3')
if wall and 'wall_material' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wall_material'])

wall = bpy.data.objects.get('wall_4')
if wall and 'wall_material' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wall_material'])


# Save the blend file
import os
os.makedirs('assets/renders', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='assets/renders/scene.blend')

# Render the scene
bpy.context.scene.render.filepath = 'assets/renders/scene.png'
bpy.ops.render.render(write_still=True)