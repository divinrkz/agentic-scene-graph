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
wall.name = 'wall_1'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(4, 1.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_2'
wall.scale = (0.1, 1.0, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(2.0, 2, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_3'
wall.scale = (2.0, 0.1, 1.5)

bpy.ops.mesh.primitive_cube_add(location=(0, 1.0, 1.5))
wall = bpy.context.active_object
wall.name = 'wall_4'
wall.scale = (0.1, 1.0, 1.5)

# -------------------------------------------------- Furniture
# furn_bed  (bed)
bpy.ops.mesh.primitive_cube_add(location=(1.00, 0.60, 0.30))
obj = bpy.context.active_object
obj.name = 'furn_bed'
obj.scale = (1.00, 0.50, 0.30)
obj.rotation_euler = (0, 0, 0)

# furn_desk  (desk)
bpy.ops.mesh.primitive_cube_add(location=(3.00, 0.75, 0.38))
obj = bpy.context.active_object
obj.name = 'furn_desk'
obj.scale = (0.50, 0.30, 0.38)
obj.rotation_euler = (0, 90, 0)

# furn_lamp  (lamp)
bpy.ops.mesh.primitive_cylinder_add(location=(3.20, 0.50, 0.25))
obj = bpy.context.active_object
obj.name = 'furn_lamp'
obj.scale = (0.10, 0.10, 0.25)
obj.rotation_euler = (0, 0, 0)

# -------------------------------------------------- Materials
mat = bpy.data.materials.new(name='wall_mat')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (1.000, 1.000, 1.000, 1.0)
bsdf.inputs['Roughness'].default_value = 0.5

mat = bpy.data.materials.new(name='floor_mat')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.490, 0.490, 0.490, 1.0)
bsdf.inputs['Roughness'].default_value = 0.5

floor = bpy.data.objects.get('Floor')
if floor and 'floor_mat' in bpy.data.materials:
    floor.data.materials.append(bpy.data.materials['floor_mat'])

w = bpy.data.objects.get('wall_1')
if w and 'wall_mat' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_mat'])

w = bpy.data.objects.get('wall_2')
if w and 'wall_mat' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_mat'])

w = bpy.data.objects.get('wall_3')
if w and 'wall_mat' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_mat'])

w = bpy.data.objects.get('wall_4')
if w and 'wall_mat' in bpy.data.materials:
    w.data.materials.append(bpy.data.materials['wall_mat'])

# -------------------------------------------------- Save & Render
import os
os.makedirs('assets/renders', exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='assets/renders/scene.blend')

bpy.context.scene.render.filepath = 'assets/renders/scene.png'
bpy.ops.render.render(write_still=True)