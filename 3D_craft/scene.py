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
bpy.ops.mesh.primitive_cube_add(location=(2.0, 0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall1'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(4, 1.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall2'
wall.scale = (0.1, 1.0, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(2.0, 2, 1.5))
wall = bpy.context.active_object
wall.name = 'wall3'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(0, 1.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall4'
wall.scale = (0.1, 1.0, 1.5)

# Add furniture
# bed1 - bed
bpy.ops.mesh.primitive_cube_add(location=(1.00, 0.60, 0.30))
obj = bpy.context.active_object
obj.name = 'bed1'
obj.scale = (0.95, 0.45, 0.30)
obj.rotation_euler = (0, 0, 0)

# desk1 - desk
bpy.ops.mesh.primitive_cube_add(location=(3.00, 0.75, 0.38))
obj = bpy.context.active_object
obj.name = 'desk1'
obj.scale = (0.50, 0.25, 0.38)
obj.rotation_euler = (0, 0, 0)

# lamp1 - lamp
bpy.ops.mesh.primitive_cylinder_add(location=(2.80, 1.25, 0.25))
obj = bpy.context.active_object
obj.name = 'lamp1'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# Create materials
# Material: wallMat
mat = bpy.data.materials.new(name='wallMat')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
# Use input names instead of indices for better compatibility
bsdf.inputs['Base Color'].default_value = (0.003, 0.003, 0.003, 1.0)
bsdf.inputs['Roughness'].default_value = None

# Material: floorMat
mat = bpy.data.materials.new(name='floorMat')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
# Use input names instead of indices for better compatibility
bsdf.inputs['Base Color'].default_value = (0.002, 0.002, 0.002, 1.0)
bsdf.inputs['Roughness'].default_value = None

# Apply materials
floor = bpy.data.objects.get('Floor')
if floor and 'floorMat' in bpy.data.materials:
    floor.data.materials.append(bpy.data.materials['floorMat'])

wall = bpy.data.objects.get('wall1')
if wall and 'wallMat' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wallMat'])

wall = bpy.data.objects.get('wall2')
if wall and 'wallMat' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wallMat'])

wall = bpy.data.objects.get('wall3')
if wall and 'wallMat' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wallMat'])

wall = bpy.data.objects.get('wall4')
if wall and 'wallMat' in bpy.data.materials:
    wall.data.materials.append(bpy.data.materials['wallMat'])


# Save the blend file
import os
os.makedirs('assets/renders', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='assets/renders/scene.blend')

# Render the scene
bpy.context.scene.render.filepath = 'assets/renders/scene.png'
bpy.ops.render.render(write_still=True)