import bpy
import os
from collections import OrderedDict

class BLENDMSH_OT_Physicalgroups(bpy.types.Operator):
    bl_idname = "blendmsh.physicalgroups"
    bl_label = ""

    diffuse_library = [
                        (255/255, 0/255, 199/255, 1),
                        (255/255, 248/255, 0/255, 1),
                        (83/255, 255/255, 0/255, 1),
                        (13/255, 218/255, 134/255, 1),
                        (115/255, 255/255, 0/255, 1),
                        (0/255, 217/255, 255/255, 1),
                        (235/255, 255/255, 0/255, 1),
                        (255/255, 178/255, 83/255, 1),
                        (148/255, 13/255, 88/255, 1),
                        (255/255, 0/255, 141/255, 1),
                        (255/255, 139/255, 0/255, 1)]

    def execute(self, context):
        scene = context.scene

        if scene.blendmsh.initialized:
            active_object = bpy.context.active_object

            if 'NATIVE' not in bpy.data.materials:
                native_mat = bpy.data.materials.new(name='NATIVE')
                active_object.data.materials.append(native_mat)

            for i in range(scene.blendmsh.n_physicalgroups):
                if str('GROUP_{}'.format(i+1)) not in bpy.data.materials:
                    
                    temp_mat = bpy.data.materials.new(name='GROUP_{}'.format(i+1))
                    temp_mat.diffuse_color = self.diffuse_library[i]
                    active_object.data.materials.append(temp_mat)

            self.report({'INFO'}, 'PHYSICAL GROUPS: {}'.format(scene.blendmsh.n_physicalgroups))
            return{'FINISHED'}
        else:
            self.report({'ERROR'}, 'Kindly initialize geometry before defining physical groups.')
            return {'CANCELLED'}    

class BLENDMSH_OT_Meshinit(bpy.types.Operator):
    bl_idname = 'blendmsh.meshinit'
    bl_label = 'Blendmsh_Meshinit'
    bl_description = 'Triangulates object.'

    def execute(self, context):
        scene = context.scene
        active_object = bpy.context.active_object
        bpy.context.space_data.shading.type = 'MATERIAL'

        filename = active_object.name + '.stl'
        bpy.ops.export_mesh.stl(filepath=os.path.join(scene.blendmsh.workspace_path, filename), ascii=True)
        active_object.select_set(True)
        bpy.ops.object.delete()

        bpy.ops.import_mesh.stl(filepath=os.path.join(scene.blendmsh.workspace_path, filename))
        active_object = bpy.context.active_object

        native_mat = bpy.data.materials.new(name='NATIVE')
        active_object.data.materials.append(native_mat)

        scene.blendmsh.initialized = True
        return {'FINISHED'}


class BLENDMSH_OT_Meshproc(bpy.types.Operator):
    bl_idname = 'blendmsh.meshproc'
    bl_label = 'Blendmsh_Meshproc'
    bl_description = 'Mesh processor.'

    def execute(self, context):
        scene = context.scene

        try:
            import gmsh_api.gmsh as gmsh

            if scene.blendmsh.initialized:
                filename = bpy.context.active_object.name
                active_object = bpy.context.active_object

                physical_group_faces = OrderedDict()
                bpy.ops.object.mode_set(mode='OBJECT')
                for _face in bpy.context.active_object.data.polygons:
                    if 'GROUP' in active_object.data.materials[_face.material_index].name_full:
                        group_id = str(active_object.data.materials[_face.material_index].name_full)

                        # GMSH INDEX STARTS FROM 1, HENCE '_face.index + 1'
                        if group_id not in physical_group_faces.keys():
                            physical_group_faces[group_id] = set([_face.index + 1])
                        else:
                            physical_group_faces[group_id].add(_face.index + 1)

                data = self.get_raw_data(os.path.join(scene.blendmsh.workspace_path, filename+'.stl'))

                points = OrderedDict()
                edges = OrderedDict()
                triangles = OrderedDict()
                curve_loop = OrderedDict()

                geo_points = OrderedDict()
                geo_edges = OrderedDict()

                i = 1
                for _surface in data:
                    for _vertex in _surface:
                        if _vertex not in points.keys():
                            points[_vertex] = i
                            geo_points[i] = _vertex
                            i += 1

                for i in range(len(data)):
                    triangles[i+1] = [points[data[i][0]], points[data[i][1]], points[data[i][2]]]

                i = 1    
                for _triangle in triangles.values():
                    for _edge in self.get_edge_indices(_triangle):
                        if _edge not in edges.keys() and _edge[::-1] not in edges.keys():
                            edges[_edge] = i
                            geo_edges[i] = _edge
                            i += 1

                for _triangle_id in triangles.keys():
                    curve_loop[_triangle_id] = []
                    for connection in self.get_curve_loop(triangles[_triangle_id]):
                        if connection in edges.keys():
                            curve_loop[_triangle_id].append(edges[connection])
                        elif connection[::-1] in edges.keys():
                            curve_loop[_triangle_id].append(-1*edges[connection[::-1]])

                all_physical_group_faces = set()
                for _face_lists in physical_group_faces.values():
                    for _face_id in _face_lists:
                        all_physical_group_faces.add(_face_id)    

                gmsh.initialize()
                gmsh.option.setNumber('General.Terminal', 1)

                lc = scene.blendmsh.cl_max
                geo = gmsh.model.geo

                for _point in points.keys():
                    geo.addPoint(_point[0], _point[1], _point[2], lc, points[_point])

                for _edge in edges.keys():
                    geo.addLine(_edge[0], _edge[1], edges[_edge])
        
                for _curve_id in curve_loop.keys():
                    geo.addCurveLoop([curve_loop[_curve_id][0], curve_loop[_curve_id][1], curve_loop[_curve_id][2]], _curve_id)
                    surf_temp = geo.addPlaneSurface([_curve_id], _curve_id)

                    if _curve_id in all_physical_group_faces:
                        gmsh.model.addPhysicalGroup(2, [surf_temp], _curve_id)

                sl = geo.addSurfaceLoop(list(curve_loop.keys()))
                v = geo.addVolume([sl])

                gmsh.model.geo.synchronize()

                gmsh.option.setNumber("Mesh.Algorithm", int(scene.blendmsh.algorithm))
                gmsh.option.setNumber("Mesh.ElementOrder", int(scene.blendmsh.element_order))
                gmsh.option.setNumber("Mesh.Optimize", 1)
                gmsh.option.setNumber("Mesh.QualityType", 2)
                gmsh.option.setNumber("Mesh.SaveAll", 1)
                gmsh.model.mesh.generate(int(scene.blendmsh.mesh_dimension))

                gmsh.write(os.path.join(scene.blendmsh.workspace_path, filename+scene.blendmsh.output_file_format))
                gmsh.finalize()

                self.report({'INFO'}, '{} file written to {}'.format(filename+scene.blendmsh.output_file_format, scene.blendmsh.workspace_path))
                return {'FINISHED'}

            else:
                self.report({'ERROR'}, 'Kindly initialize geometry before defining physical groups.')
                return {'CANCELLED'}            

        except:
            self.report({'ERROR'}, 'Couldnot import Gmsh module, Kindly re-install it manually.')
            return {'CANCELLED'}


    def get_raw_data(self, path):
        data = [[]]
        with open(path, 'r') as f:
            line = f.readline()
            while(line):
                if 'endfacet' in line:
                    data.append([])
                else:
                    if 'vertex' in line:
                        #IGNORING NORMALS FOR NOW
                        data[-1].append(tuple(map(float, line[:-1].split(' ')[1:])))

                line = f.readline()

        return data[:-1]

    def get_curve_loop(self, surf):
        return [(surf[0], surf[1]), (surf[1], surf[2]), (surf[2], surf[0])]

    def get_edge_indices(self, surf):
        return [(surf[0], surf[2]), (surf[0], surf[1]), (surf[1], surf[2])]
