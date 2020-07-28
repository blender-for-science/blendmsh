import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, EnumProperty, BoolProperty

class BlendmshProperties(bpy.types.PropertyGroup):

        initialized : BoolProperty(default=False)

        workspace_path : StringProperty(
                name="",
                description="Path for the results",
                default='/tmp/',
                subtype='DIR_PATH')

        cl_max : FloatProperty(
                name="",
                default=0.1,
                min=0.1,
                max = 5.0,
                precision=3,
                description="Maximum size of the element.")

        n_physicalgroups : IntProperty(
                name="Physical groups",
                default=0,
                min=0,
                description="Number of physical groups.")

        element_order : EnumProperty(
                name='Element order',
                items=[
                        ('1', '1', 'First order elements'),
                        ('2', '2', 'Second order elements'),
                        ('3', '3', 'Third order elements')],
                default='1',
                description='Element order')

        mesh_dimension : EnumProperty(
                name='Mesh dimension',
                items=[
                        ('1', '1D', '1D mesh'),
                        ('2', '2D', '2D mesh'),
                        ('3', '3D', '3D mesh')],
                default='3',
                description='Dimension of output mesh')

        algorithm : EnumProperty(
                name='',
                items=[
                        ('0', 'auto', 'Automatic'),
                        ('1', 'meshadapt', 'Meshadapt'),
                        ('2', 'del2d', 'Delunay2D'),
                        ('3', 'front2d', 'Front2D'),
                        ('4', 'delquad', 'Delquad'),
                        ('5', 'pack', 'Pack'),
                        ('6', 'initial2d', 'Initial2D'),
                        ('7', 'del3d', 'Delunay3D'),
                        ('8', 'front3d', 'Front3D'),
                        ('9', 'mmg3d', 'MMG3D'),
                        ('10', 'hxt', 'HXT'),
                        ('11', 'initial3d', 'Initial3D')],

                default='0',
                description="Algorithm")

        output_file_format : EnumProperty(
                name='Output',
                items=[
                        ('.msh', '.msh', 'Gmsh (.msh)'),
                        ('.inp', '.inp', 'Abaqus (.inp)'),
                        ('.vtk', '.vtk', 'The Visualization Toolkit (.vtk)')],
                default='.msh',
                description='Output file format')

