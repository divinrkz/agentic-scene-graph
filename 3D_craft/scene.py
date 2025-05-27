import bpy
bpy.ops.wm.append(filename="3D_Sofa_Model")
bpy.context.selected_objects[0].location = (-498.50, -500.00, 0.50)
bpy.ops.wm.append(filename="3D_Coffee_Table_Model")
bpy.context.selected_objects[0].location = (-500.00, -498.70, 0.25)
bpy.ops.wm.append(filename="3D_Room_Model")
bpy.context.selected_objects[0].location = (-495.50, -500.00, 1.25)