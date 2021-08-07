bl_info = {
    "name": "NGon Finder",
    "author": "Yonaoshi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar",
    "description": "Find the N-Gon in edit mode.",
    "warning": "",
    "doc_url": "https://github.com/yonaoshi/NGonFinder",
    "category": "Mesh",
}


import bmesh
import bpy


class NGFPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "NGon Finder"
    bl_idname = "OBJECT_PT_NGF"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "NGon Finder"

    def draw(self, context):
        self.layout.row().operator("object.ngf_operator")


class NGFOperator(bpy.types.Operator):
    """Find NGon Operator"""
    bl_idname = "object.ngf_operator"
    bl_label = "Find"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')

        # Get the active mesh
        obj = bpy.context.edit_object
        me = obj.data

        # Get a BMesh representation
        bm = bmesh.from_edit_mesh(me)

        # deselct square / select NGon
        for face in bm.faces:
            if len(face.verts) == 4:
                face.select_set(False)
            else:
                face.select_set(True)

        # Show the updates in the viewport
        # and recalculate n-gon tessellation.
        bmesh.update_edit_mesh(me, True)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(NGFPanel)
    bpy.utils.register_class(NGFOperator)


def unregister():
    bpy.utils.unregister_class(NGFPanel)
    bpy.utils.unregister_class(NGFOperator)


if __name__ == "__main__":
    register()
