import bpy
from mathutils import Vector
import math

# -------------------------------------------------- Reset scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# -------------------------------------------------- Camera
cam_data  = bpy.data.cameras.new(name='Camera')
cam_data.lens = 35
cam_obj   = bpy.data.objects.new('Camera', cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (6.8, -4.8, 6.6)

# Aim camera at centre of room (65° elevation, 45° azimuth iso-view)
direction = Vector((2.0, 1.0, 1.5)) - cam_obj.location
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam_obj

# -------------------------------------------------- Lighting
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
bpy.context.active_object.data.energy = 2.0

# -------------------------------------------------- Render settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# -------------------------------------------------- Floor
bpy.ops.mesh.primitive_cube_add(location=(2.0, 1.0, -0.05))
floor = bpy.context.active_object
floor.name = 'Floor'
floor.scale = (2.0, 1.0, 0.05)

# -------------------------------------------------- Walls
bpy.ops.mesh.primitive_cube_add(location=(2.0, 0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall1'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(4, 0.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall2'
wall.scale = (0.1, 0.0, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(2.0, 0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall3'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(0, 0.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall4'
wall.scale = (0.1, 0.0, 1.5)

# -------------------------------------------------- Furniture
# desk1  (desk)
bpy.ops.mesh.primitive_cube_add(location=(1.00, 0.00, 0.38))
obj = bpy.context.active_object
obj.name = 'desk1'
obj.scale = (0.40, 0.30, 0.38)
obj.rotation_euler = (0, 0, 0)

# chair1  (seat)
bpy.ops.mesh.primitive_cube_add(location=(1.00, 0.00, 0.40))
obj = bpy.context.active_object
obj.name = 'chair1'
obj.scale = (0.25, 0.25, 0.40)
obj.rotation_euler = (0, 180, 0)

# lamp1  (lamp)
bpy.ops.mesh.primitive_cylinder_add(location=(1.35, 0.75, 0.25))
obj = bpy.context.active_object
obj.name = 'lamp1'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# bookshelf1  (storage)
bpy.ops.mesh.primitive_cube_add(location=(2.40, 0.00, 0.90))
obj = bpy.context.active_object
obj.name = 'bookshelf1'
obj.scale = (0.40, 0.20, 0.90)
obj.rotation_euler = (0, 0, 0)

# sofa1  (seat)
bpy.ops.mesh.primitive_cube_add(location=(3.00, 0.00, 0.42))
obj = bpy.context.active_object
obj.name = 'sofa1'
obj.scale = (0.90, 0.38, 0.42)
obj.rotation_euler = (0, 270, 0)

# desk2  (desk)
bpy.ops.mesh.primitive_cube_add(location=(0.50, 0.00, 0.38))
obj = bpy.context.active_object
obj.name = 'desk2'
obj.scale = (0.40, 0.30, 0.38)
obj.rotation_euler = (0, 0, 0)

# chair2  (seat)
bpy.ops.mesh.primitive_cube_add(location=(0.50, 0.00, 0.40))
obj = bpy.context.active_object
obj.name = 'chair2'
obj.scale = (0.25, 0.25, 0.40)
obj.rotation_euler = (0, 180, 0)

# lamp2  (lamp)
bpy.ops.mesh.primitive_cylinder_add(location=(0.35, 0.75, 0.25))
obj = bpy.context.active_object
obj.name = 'lamp2'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# bookshelf2  (storage)
bpy.ops.mesh.primitive_cube_add(location=(0.50, 0.00, 0.90))
obj = bpy.context.active_object
obj.name = 'bookshelf2'
obj.scale = (0.40, 0.20, 0.90)
obj.rotation_euler = (0, 0, 0)

# desk3  (desk)
bpy.ops.mesh.primitive_cube_add(location=(3.50, 0.00, 0.38))
obj = bpy.context.active_object
obj.name = 'desk3'
obj.scale = (0.40, 0.30, 0.38)
obj.rotation_euler = (0, 0, 0)

# chair3  (seat)
bpy.ops.mesh.primitive_cube_add(location=(3.50, 0.00, 0.40))
obj = bpy.context.active_object
obj.name = 'chair3'
obj.scale = (0.25, 0.25, 0.40)
obj.rotation_euler = (0, 180, 0)

# lamp3  (lamp)
bpy.ops.mesh.primitive_cylinder_add(location=(3.35, 0.75, 0.25))
obj = bpy.context.active_object
obj.name = 'lamp3'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# bookshelf3  (storage)
bpy.ops.mesh.primitive_cube_add(location=(3.50, 0.00, 0.90))
obj = bpy.context.active_object
obj.name = 'bookshelf3'
obj.scale = (0.40, 0.20, 0.90)
obj.rotation_euler = (0, 0, 0)

# -------------------------------------------------- Materials
mat = bpy.data.materials.new(name='floor_material')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.471, 0.471, 0.471, 1.0)
bsdf.inputs['Roughness'].default_value = 0.8

mat = bpy.data.materials.new(name='wall_material')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.902, 0.902, 0.902, 1.0)
bsdf.inputs['Roughness'].default_value = 0.3

floor = bpy.data.objects.get('Floor')
if floor and 'floor_material' in bpy.data.materials:
    floor.data.materials.append(bpy.data.materials['floor_material'])

w = bpy.data.objects.get('wall1')
if w and 'wall_material' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_material'])

w = bpy.data.objects.get('wall2')
if w and 'wall_material' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_material'])

w = bpy.data.objects.get('wall3')
if w and 'wall_material' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_material'])

w = bpy.data.objects.get('wall4')
if w and 'wall_material' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_material'])

# -------------------------------------------------- Save & Render
import os
os.makedirs('assets/renders', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='assets/renders/scene.blend')

bpy.context.scene.render.filepath = 'assets/renders/scene.png'
bpy.ops.render.render(write_still=True)