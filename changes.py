# Perform the mirroring operation
bpy.context.view_layer.objects.active = target_armature
bpy.ops.object.mode_set(mode='EDIT')

- # Check if the bone group already exists and clear it
- if bone_group_name in target_armature.pose.bone_groups:
-     target_armature.pose.bone_groups.remove(target_armature.pose.bone_groups[bone_group_name])

- # Create a new bone group
- bone_group = target_armature.pose.bone_groups.new(name=bone_group_name)

+ # Check if the bone collection already exists and clear it
+ bone_collection = target_armature.pose.bone_groups.get(bone_group_name)
+ if bone_collection:
+     target_armature.pose.bone_groups.remove(bone_collection)

+ # Create a new bone collection
+ bone_collection = target_armature.pose.bone_groups.new(name=bone_group_name)

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
-       # Add the new bone to the bone group
-       bone_group.bones.append(new_bone.name)
+       # Add the new bone to the bone collection
+       bone_collection.bones.append(new_bone.name)
    else:
        # If the bone exists, update its head, tail, and roll to match the source armature
        target_bone = target_armature.data.edit_bones[bone_name]
        source_bone = source_armature.data.edit_bones[bone_name]
        target_bone.head = source_bone.head
        target_bone.tail = source_bone.tail
        target_bone.roll = source_bone.roll
-       # Add the existing bone to the bone group
-       bone_group.bones.append(target_bone.name)
+       # Add the existing bone to the bone collection
+       bone_collection.bones.append(target_bone.name)

bpy.ops.object.mode_set(mode='OBJECT')
