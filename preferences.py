import bpy

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):

        import importlib
        from .utils_pip import Pip
        Pip._ensure_user_site_package()

        layout = self.layout       

        if importlib.util.find_spec('gmsh-api') is not None:
            layout.label(text='gmsh-api loaded.', icon='INFO')
        else:
            layout.label(text='Blendmsh requires gmsh-api!', icon='ERROR')
            row = layout.row()
            row.operator('blendmsh.installer')

class BlendmshInstaller(bpy.types.Operator):
    bl_idname = "blendmsh.installer"
    bl_label = "Install gmsh-api"
    bl_description = ("Install gmsh-api")

    def execute(self, context):
        try:
            from .utils_pip import Pip
            # Pip.upgrade_pip()
            Pip.install('gmsh-api')

            import gmsh_api
            self.report({'INFO'}, 'Successfully installed gmsh-api.')
        except:
            self.report({'ERROR'}, 'Could not install gmsh-api, Kindly install it manually.')
        return {'FINISHED'}