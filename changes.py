# Assuming 'target_armature' is a valid armature object
# and 'bone_group_name' is the name of the bone collection you want to access

# Check if the bone collection already exists
bone_collection = next((col for col in target_armature.pose.bone_groups if col.name == bone_group_name), None)

# If the bone collection doesn't exist, create it
if bone_collection is None:
    bone_collection = target_armature.pose.bone_groups.new(name=bone_group_name)

# Now you can use 'bone_collection' as needed
