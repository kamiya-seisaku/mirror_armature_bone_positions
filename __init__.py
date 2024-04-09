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

        # Check if both armatures are selected
        if not source_armature or not target_armature:
            self.report({'ERROR'}, "Armatures not found")
            return {'CANCELLED'}

        # Ensure both armatures are in object mode before changes
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = source_armature
        bpy.ops.object.mode_set(mode='EDIT')

        # Perform the mirroring operation
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode='EDIT')

        # Define the bone group name
        bone_group_name = "BonesToMove"

        # Check if the bone collection already exists and clear it
        bone_collection = target_armature.pose.bone_groups.get(bone_group_name)
        if bone_collection:
            target_armature.pose.bone_groups.remove(bone_collection)

        # Create a new bone collection
        bone_collection = target_armature.pose.bone_groups.new(name=bone_group_name)

        # Define a list of source bones to be mirrored
        source_bones_list = [bone.name for bone in source_armature.data.edit_bones]

        for bone_name in source_bones_list:
            # Check if the bone exists in the target armature
            if bone_name not in target_armature.data.edit_bones:
                # If not, create a new bone in the target armature
                new_bone = target_armature.data.edit_bones.new(name=bone_name)
                # Set the head, tail, and roll to match the source armature
                source_bone = source_armature.data.edit_bones[bone_name]
                new_bone.head = source_bone.head
                new_bone.tail = source_bone.tail
                new_bone.roll = source_bone.roll
                # Add the new bone to the bone collection
                bone_collection.bones.append(new_bone.name)
            else:
                # If the bone exists, update its head, tail, and roll to match the source armature
                target_bone = target_armature.data.edit_bones[bone_name]
                source_bone = source_armature.data.edit_bones[bone_name]
                target_bone.head = source_bone.head
                target_bone.tail = source_bone.tail
                target_bone.roll = source_bone.roll
                # Add the existing bone to the bone collection
                bone_collection.bones.append(target_bone.name)

        bpy.ops.object.mode_set(mode='OBJECT')
        is_operation_finished = True
        return {'FINISHED'}

    def invoke(self, context, event):
        if MirrorRigify.is_running_modal:
            self.report({'WARNING'}, "Mirror Rigify is already running")
            return {'CANCELLED'}
        else:
            MirrorRigify.is_running_modal = True
            context.window_manager.modal_handler_add(self)
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
