# https://blenderartists.org/t/editing-bone-groups-with-python/1489930
# This is one of the major issues with the Blender API docs, it is not inherently clear how to actually access the data you want, or where it is stored.
# In this case, the data you are looking for is stored in Pose Bones inside the active object.
# The script below will create a new Bone Group on an existing armature, rename it, and reassign the color set.
# I have added comments to explain how it all works, feel free to ask if anything is unclear.

def test():
        
        import bpy

        context = bpy.context
        object = context.object

        # Bone Groups can only be created in Pose mode, so if we're not already in
        # Pose mode, then switch to it
        if not context.mode == 'POSE':
            bpy.ops.object.posemode_toggle()

        # Create a new Bone Group
        bpy.ops.pose.group_add()

        # Creating a variable called bone_group for convenience
        # Setting it to the first Bone Group available on the object (ie bone_groups[0])
        bone_group = object.pose.bone_groups[0]

        # Now we can set the name and color theme
        # If you're not sure what the name of a theme is, 
        # assign it manually and check the INFO window for the exact name
        bone_group.name = 'Boney M'
        bone_group.color_set = 'THEME01'

        # It appears that type=0 will create a new empty bone group
        # So you'll have to make the assignment number one higher that
        # the bone_group number, eg - bone_group[0] and type=1, 
        # bone_group[1] and type=2 etc
        bpy.ops.pose.group_assign(type=1)

# EDIT:
# Meant to add that the last line where you assign bones to groups depends on which bones are currently selected, so you may want to add some logic in there to deselect any bones you don’t want, and select any that you do want to add to the group before you call the group_assign operator!