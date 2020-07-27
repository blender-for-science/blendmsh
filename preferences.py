import bpy

class BlendmshPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):

        import importlib
        from .utils_pip import Pip
        Pip._ensure_user_site_package()

        layout = self.layout       

        if importlib.util.find_spec('gmsh') is not None:
            layout.label(text='Gmsh module loaded.', icon='INFO')
        else:
            layout.label(text='Blendmsh requires Gmsh module!', icon='ERROR')
            row = layout.row()
            row.operator('blendmsh.installer')
            layout.label(text='Installing Gmsh module...', icon='URL')

class BlendmshInstaller(bpy.types.Operator):
    bl_idname = "blendmsh.installer"
    bl_label = "Install Gmsh"
    bl_description = ("Install Gmsh module")

    def execute(self, context):
        try:
            from .utils_pip import Pip
            # Pip.upgrade_pip()
            Pip.install('gmsh')

            import gmsh
            bool_gmsh = True
            self.report({'INFO'}, 'Successfully installed Gmsh module.')
        except:
            self.report({'ERROR'}, 'Could not install Gmsh module, Kindly install it manually.')
        return {'FINISHED'}