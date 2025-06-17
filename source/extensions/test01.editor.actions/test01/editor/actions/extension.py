# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES.
# All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import omni.ext

import omni.kit.actions.core
import omni.kit.hotkeys.core as hotkeys

def register_actions(extension_id: str):
    import test01.editor.random_prim_ui  # Change to the name of your extension
    action_registry = omni.kit.actions.core.get_action_registry()
    actions_tag = "My Actions"

    action_registry.register_action(
        extension_id,  # extension_id: The id of the source extension registering the action.
        "scatter_8_cones",  # action_id: Id of the action, unique to the extension registering it.
        lambda: test01.editor.random_prim_ui.scatter_cones(8),
        # The Python object called when the action is executed. (Change to use the name of your extension)
        display_name="Scatter 8 Cones",  # The name of the action for display purposes.
        description="Scatter 8 Cones in random positions",  # A brief description of what the action does.
        tag=actions_tag,  # Arbitrary tag used to group sets of related actions.
    )

def deregister_actions(extension_id: str):
    action_registry = omni.kit.actions.core.get_action_registry()
    action_registry.deregister_all_actions_for_extension(extension_id)

def register_hotkeys(extension_id: str):
    hotkey_registry = hotkeys.get_hotkey_registry()
    action_registry = omni.kit.actions.core.get_action_registry()
    ext_actions = action_registry.get_all_actions_for_extension(extension_id)

    hotkey_registry.register_hotkey(
        hotkey_ext_id=extension_id,
        key="CTRL+8",
        action_ext_id=ext_actions[0].extension_id,
        action_id=ext_actions[0].id,
    )

def deregister_hotkeys(extension_id: str):
    hotkey_registry = hotkeys.get_hotkey_registry()
    hotkey_registry.deregister_all_hotkeys_for_extension(extension_id)


class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        # add actions
        self._ext_name = omni.ext.get_extension_name(ext_id)
        register_actions(self._ext_name)

        # add hotkeys
        register_hotkeys(self._ext_name)

        print("[test01.editor.actions] MyExtension startup.  Registered Actions and Hotkeys")

    def on_shutdown(self):
        deregister_hotkeys(self._ext_name)
        deregister_actions(self._ext_name)
        print("[test01.editor.actions] MyExtension shutdown.  Deregistered Actions and Hotkeys")

