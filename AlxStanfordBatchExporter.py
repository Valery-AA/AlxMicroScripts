bl_info = {
    "name" : "Batch PLY",
    "author" : "Valeria Bosco[Valy Arhal]",
    "description" : "Exports the entire mesh selection as singular Stanford .ply files, file name based on object name, batch export folder is where the .blend file is located",
    "version" : (1, 0, 0),
    "warning" : "",
    "category" : "3D View",
    "location" : "",
    "blender" : (3, 6, 0)
}

import bpy
import os

class Alx_PT_PLYExport(bpy.types.Panel):
    """"""

    bl_label = "Batch Export Selection"
    bl_idname = "alx_panel_ply_export"

    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "Alx Export"

    

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        AlxLayout = self.layout
        AxlOPS_PLY_Export = AlxLayout.row().operator(Alx_OT_BatchPLYExport.bl_idname, text="Export Stanford (.ply)")

class Alx_OT_BatchPLYExport(bpy.types.Operator):
    """"""

    bl_label = "Batch Export Selection"
    bl_idname = "alx.operator_ply_export"

    UseAsciiFormat : bpy.props.BoolProperty(name="Export as ASCII", default=False)
    UseMeshModifiers : bpy.props.BoolProperty(name="Export with Mesh Modifiers", default=False)
    UseVertexNormals : bpy.props.BoolProperty(name="Export Vertex Normals", default=False)
    UseUVCoordinates : bpy.props.BoolProperty(name="Export UV Coordinates", default=False)
    UseVertexColors : bpy.props.BoolProperty(name="Export Vertex Colors", default=False)
    ExportGlobalScale : bpy.props.FloatProperty(name="Export Scale", default=1.0, min=-100000, max=100000)

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"
    
    def execute(self, context):
        try:
            ObjectListToExport = []
            context.selected_objects[0]
            for Object in context.selected_objects:
                if (Object is not None) and (Object.type == "MESH"):
                    ObjectListToExport.append(Object)

            for ExportObject in ObjectListToExport:
                blend_file_path = bpy.data.filepath
                if (blend_file_path != ""):
                    directory = os.path.dirname(blend_file_path)

                    export_directory_name = "Stanford Batch Export"
                    export_directory = os.path.join(directory, export_directory_name)

                    target_file = os.path.join(export_directory, "%s.ply" % ExportObject.name)

                    if (os.path.exists(export_directory) == False):
                        os.mkdir(export_directory)

                    for DataObject in bpy.data.objects:
                        DataObject.select_set(False)


                    ExportObject.select_set(True)
                    bpy.context.view_layer.objects.active = ExportObject

                    bpy.ops.export_mesh.ply(
                        filepath=target_file, 
                        use_selection=True, 
                        use_ascii=self.UseAsciiFormat, 
                        use_mesh_modifiers=self.UseMeshModifiers, 
                        use_normals=self.UseVertexNormals, 
                        use_uv_coords=self.UseUVCoordinates, 
                        use_colors=self.UseVertexColors,
                        global_scale=self.ExportGlobalScale
                        )

        except Exception as e:
            print(e)

        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


AlxClassQueue = [Alx_OT_BatchPLYExport, Alx_PT_PLYExport]

def register():
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    bpy.context.preferences.use_preferences_save = True

def unregister():
    for AlxQCls in AlxClassQueue:
        bpy.utils.unregister_class(AlxQCls)

if __name__ == "__main__":
    register()