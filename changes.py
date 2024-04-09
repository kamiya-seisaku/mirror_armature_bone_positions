class MirrorRigify(bpy.types.Operator):
    bl_idname = "object.mirror_rigify"
    bl_label = "Mirror Rigify"
    bl_options = {'REGISTER', 'UNDO'}

+   # Add a class property to track the running state
+   is_running_modal = False

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and not bpy.types.WindowManager.running_modal_operator

    def execute(self, context):
        # ... existing execute code ...

    def invoke(self, context, event):
-       if context.window_manager.running_modal_operator:
+       if MirrorRigify.is_running_modal:
            self.report({'WARNING'}, "Mirror Rigify is already running")
            return {'CANCELLED'}
        else:
-           context.window_manager.running_modal_operator = True
+           MirrorRigify.is_running_modal = True
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

    def modal(self, event, context):
        # ... existing modal code ...

        # When finishing the modal operation, reset the running state
+       if finished:  # Replace 'finished' with your condition to end the modal operation
+           MirrorRigify.is_running_modal = False

        return {'PASS_THROUGH'}

# ... rest of your code ...
