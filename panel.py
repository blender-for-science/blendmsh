import bpy
from bpy.props import BoolVectorProperty

class BLENDMSH_PT_Panel(bpy.types.Panel):
    bl_idname = 'BLENDMSH_PT_panel'
    bl_label = 'blendmsh'
    bl_category = 'blendmsh'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        rowsub = layout.row(align=True)
        rowsub.prop(scene.blendmsh, 'workspace_path')

        col = layout.column()    
        col.operator('blendmsh.meshinit', text='Initialize')

        row = layout.row()
        row.label(text=" ")

        rowsub = layout.row(align=True)
        rowsub.prop(scene.blendmsh, "n_physicalgroups")  
        rowsub.operator('blendmsh.physicalgroups', icon='ADD')

        row = layout.row()
        row.label(text=" ")

        row = layout.row(align=True)
        row.prop(scene.blendmsh, "element_order", icon='NONE', expand=True, 
                    slider=True, toggle=False, icon_only=False, event=False, 
                    full_event=False, emboss=True)

        row = layout.row()
        rowsub = layout.row(align=True)
        rowsub.prop(scene.blendmsh, 'algorithm')

        rowsub = layout.row(align=True)
        rowsub.prop(scene.blendmsh, "cl_max")

        row = layout.row(align=True)
        row.prop(scene.blendmsh, "mesh_dimension", icon='NONE', expand=True, 
                    slider=True, toggle=False, icon_only=False, event=False, 
                    full_event=False, emboss=True)

        row = layout.row()
        rowsub = layout.row(align=True)
        rowsub.prop(scene.blendmsh, 'output_file_format')

        row = layout.row()
        row.label(text=" ")

        col = layout.column()    
        col.operator('blendmsh.meshproc', text='Mesh')

        row = layout.row()
        row.label(text=" ")

        row = layout.row(align=True)
        row.alignment = 'RIGHT'
        row.label(text="Made with")
        row.label(icon='FUND')

