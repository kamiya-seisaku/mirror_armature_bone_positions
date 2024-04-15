# This is a Blender addon to copy all bone transformations from a source armature to a target armature.  Intended for rigify armature but should be good for any two armatures with same bone names.
# Written in 2024 By kkey, made public as is in MIT license.
# 2024/4/9: Switched to modal execution, for ease in debugging.

import bpy

# Add-on information
bl_info = {
    "name": "Mirror Rigify",
    "author": "kkey",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > My Tab",
    "description": "Copies bone transformations from one Rigify armature to another.",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}

# Property group to hold the armature references
class MirrorRigifyProperties(bpy.types.PropertyGroup):
    # Source armature property with an eyedropper selector
    source_armature: bpy.props.PointerProperty(
        name="Source Rigify Armature",
        type=bpy.types.Object,
        description="Select the source Rigify armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    ) # type: ignore
    # Target armature property with an eyedropper selector
    target_armature: bpy.props.PointerProperty(
        # name="Target Rigify Armature",
        type=bpy.types.Object,
        description="Select the target Rigify armature",
        poll=lambda self, obj: obj.type == 'ARMATURE'
    ) # type: ignore

# UI Panel in the 3D View
class MirrorRigifyPanel(bpy.types.Panel):
    bl_label = "Mirror Rigify"
    bl_idname = "OBJECT_PT_mirror_rigify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        props = context.scene.mirror_rigify_props

        # UI elements for selecting armatures
        layout.prop(props, "source_armature")
        layout.prop(props, "target_armature")
        # Button to execute the mirroring operation
        layout.operator("object.mirror_rigify")

# Operator to perform the mirroring action
class MirrorRigify(bpy.types.Operator):
    bl_idname = "object.mirror_rigify"
    bl_label = "Mirror Rigify"
    bl_options = {'REGISTER', 'UNDO'}

    # Add a class property to track the running state
    is_running_modal = False
    is_operation_finished = False

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'
        # return context.area.type == 'VIEW_3D' and not bpy.types.WindowManager.running_modal_operator

    def execute(self, context):
        is_operation_finished = False
        props = context.scene.mirror_rigify_props
        source_armature = props.source_armature
        target_armature = props.target_armature

        source_bones_list = [bone.name for bone in source_armature.data.bones]
        target_bones_list = [bone.name for bone in target_armature.data.bones]

        # Check if both armatures are selected
        if not source_armature or not target_armature:
            self.report({'ERROR'}, "Armatures not found")
            return {'CANCELLED'}

        # if bpy.ops.armature.collections("TobeMoved"):
        #     bpy.ops.armature.collection_delete(collection="TobeMoved")
        bone_collection = bpy.ops.armature.collection_add()

        # Ensure both armatures are in object mode before changes
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = source_armature
        bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.armature.collection_rename(name="TobeMoved")
        # send armature collection to the top
        for i in range(0, bpy.ops.armature.collections_count()-1):
            bpy.ops.armature.collection_move(direction='UP')

        # Perform the mirroring operation
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode='EDIT')

        for bone_name in source_bones_list:
            # Check if the bone exists in the target armature
            # target_bone_name = "ORG-"+bone_name
            target_bone_name = bone_name
            if target_bone_name not in target_armature.data.edit_bones:
                # If not, do nothing
                pass
            else:
                # If the bone exists, update its head, tail, and roll to match the source armature
                target_bone = target_armature.data.edit_bones[target_bone_name]
                source_bone = source_armature.data.edit_bones[bone_name]
                # todo: 2024/4/15 bone coords are relative to object origin.  compensattion added. test this. 
                target_bone.head = source_bone.head + target_armature.location - source_armature.location
                target_bone.tail = source_bone.tail + target_armature.location - source_armature.location
                target_bone.roll = source_bone.roll + target_armature.rotation_euler - source_armature.rotation_euler

                # Assign the selected bone collection to the armature
                target_bone.select
                bpy.ops.armature.collection_assign()
                # rename bone collection
                
                # force redraw ui and 3d view
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


        bpy.ops.object.mode_set(mode='OBJECT')
        is_operation_finished = True
        return {'FINISHED'}

    def invoke(self, context, event):
        # if MirrorRigify.is_running_modal:
        #     self.report({'WARNING'}, "Mirror Rigify is already running")
        #     return {'CANCELLED'}
        # else:
        #     MirrorRigify.is_running_modal = True
        #     context.window_manager.modal_handler_add(self)
        #     self.execute(context)
        #     return {'RUNNING_MODAL'}
        self.execute(context)
        return {'RUNNING_MODAL'}

    def modal(self, event, context):
        # if event.type in {'RIGHTMOUSE', 'ESC'}:
        #     context.window_manager.running_modal_operator = False
        #     return {'CANCELLED'}
        if self.is_operation_finished:
            MirrorRigify.is_running_modal = False
            return {'FINISHED'}

        return {'PASS_THROUGH'}

# Register and unregister functions for Blender to hook up the addon
def register():
    bpy.utils.register_class(MirrorRigifyProperties)
    bpy.utils.register_class(MirrorRigifyPanel)
    bpy.utils.register_class(MirrorRigify)
    bpy.types.Scene.mirror_rigify_props = bpy.props.PointerProperty(type=MirrorRigifyProperties)

def unregister():
    bpy.utils.unregister_class(MirrorRigifyProperties)
    bpy.utils.unregister_class(MirrorRigifyPanel)
    bpy.utils.unregister_class(MirrorRigify)
    del bpy.types.Scene.mirror_rigify_props

if __name__ == "__main__":
    register()
