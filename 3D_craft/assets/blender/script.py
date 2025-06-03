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

# -------------------------------------------------- Furniture
# bed  (bed)
bpy.ops.mesh.primitive_cube_add(location=(0.90, 0.50, 0.30))
obj = bpy.context.active_object
obj.name = 'bed'
obj.scale = (0.95, 0.45, 0.30)
obj.rotation_euler = (0, 0, 0)

# desk  (desk)
bpy.ops.mesh.primitive_cube_add(location=(3.00, 1.30, 0.38))
obj = bpy.context.active_object
obj.name = 'desk'
obj.scale = (0.60, 0.30, 0.38)
obj.rotation_euler = (0, 0, 0)

# lamp  (lamp)
bpy.ops.mesh.primitive_cylinder_add(location=(3.60, 1.60, 0.25))
obj = bpy.context.active_object
obj.name = 'lamp'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# -------------------------------------------------- Materials
mat = bpy.data.materials.new(name='mat_wall')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.004, 0.004, 0.004, 1.0)
bsdf.inputs['Roughness'].default_value = 0.8

mat = bpy.data.materials.new(name='mat_floor')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.002, 0.002, 0.002, 1.0)
bsdf.inputs['Roughness'].default_value = 0.8

floor = bpy.data.objects.get('Floor')
if floor and 'mat_floor' in bpy.data.materials:
    floor.data.materials.append(bpy.data.materials['mat_floor'])

w = bpy.data.objects.get('wall1')
if w and 'mat_wall' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['mat_wall'])

w = bpy.data.objects.get('wall2')
if w and 'mat_wall' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['mat_wall'])

w = bpy.data.objects.get('wall3')
if w and 'mat_wall' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['mat_wall'])

w = bpy.data.objects.get('wall4')
if w and 'mat_wall' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['mat_wall'])

# -------------------------------------------------- Save & Render
import os
os.makedirs('assets/renders', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='assets/renders/scene.blend')

bpy.context.scene.render.filepath = 'assets/renders/scene.png'
bpy.ops.render.render(write_still=True)