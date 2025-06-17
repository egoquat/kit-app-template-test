# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.usd

from pxr import Sdf, Usd
import random

from omni.kit.menu.utils import MenuItemDescription

def scatter_cones(quantity: int):
    usd_context = omni.usd.get_context()
    stage = usd_context.get_stage()

    for _ in range(quantity):
        prim_path = omni.usd.get_stage_next_free_path(
            stage,
            str(stage.GetPseudoRoot().GetPath().AppendPath("Cone")),
            False
        )

        omni.kit.commands.execute(
            "CreatePrimCommand",
            prim_path=prim_path,
            prim_type="Cone",
            attributes={"radius": 50, "height": 100},
            select_new_prim=True,
        )

        bound = 500
        rand_x = random.uniform(-bound, bound)
        rand_z = random.uniform(-bound, bound)

        translation = (rand_x, 0, rand_z)
        omni.kit.commands.execute(
            "TransformPrimSRT",
            path=prim_path,
            new_translation=translation,
        )

def clear_cones():
    usd_context = omni.usd.get_context()
    stage = usd_context.get_stage()

    # Empty list to hold paths of matching primitives
    matched_cones = []

    # Iterate over all prims in the stage
    for prim in stage.TraverseAll():
        # Check if the prim's name starts with the pattern
        if prim.GetName().startswith("Cone"):
            matched_cones.append(prim.GetPath())

    # Delete all the Cone prims
    omni.kit.commands.execute("DeletePrims", paths=matched_cones)

# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.
class MyExtension(omni.ext.IExt):

    def create_window(self):
        self._window = ui.Window("Random Prim UI", width=300, height=150)

        with self._window.frame:
            with ui.VStack():
                label = ui.Label("", height=ui.Percent(15), style={"alignment": ui.Alignment.CENTER})

                def on_click():
                    step = self._step_size_model.as_int
                    self._count += step
                    label.text = f"count: {self._count}"
                    scatter_cones(step)

                def on_reset():
                    self._count = 0
                    label.text = "empty"
                    clear_cones()

                with ui.HStack():
                    ui.Button("Add", clicked_fn=on_click)
                    ui.Button("Reset", clicked_fn=on_reset)

                with ui.HStack(height=0):
                    ui.Label("Step Size", style={"alignment": ui.Alignment.RIGHT_CENTER})
                    ui.Spacer(width=8)
                    self._step_size_model = ui.IntDrag(min=1, max=10).model
                    self._step_size_model.set_value(1)

    def register_actions(self, _ext_name: str):
        action_registry = omni.kit.actions.core.get_action_registry()
        actions_tag = "My Actions"

        action_registry.register_action(
            _ext_name,
            "random_prim_ui",
            lambda: self.create_window(),
            display_name="Register Random Prim UI",
            description="Register the Random Prim UI, which enables the user to randomly generate cones and delete all cones.",
            tag=actions_tag,
        )

    def deregister_actions(self, _ext_name: str):
        action_registry = omni.kit.actions.core.get_action_registry()
        action_registry.deregister_all_actions_for_extension(_ext_name)

    def on_startup(self, _ext_id):
        print("[test01.editor.random_prim_ui] Extension startup")
        # add actions

        self._ext_name = omni.ext.get_extension_name(_ext_id)
        self.register_actions(self._ext_name)

        # add menu item
        self._menu_list = [
            MenuItemDescription(
                name="Random Prim UI",
                onclick_action=(self._ext_name, "random_prim_ui"),
            )
        ]

        omni.kit.menu.utils.add_menu_items(self._menu_list, "Tutorial Menu")

        self._count = 0
        self.create_window();

    def on_click():
        step = self._step_size_model.as_int
        self._count += step
        label.text = f"count: {self._count}"
        scatter_cones(step)

    def on_reset():
        self._count = 0
        label.text = "empty"
        clear_cones()

    def on_shutdown(self):
        print("[test01.editor.random_prim_ui] Extension shutdown")
        self.deregister_actions(self._ext_name)

        if self._window:
            self._window.destroy()
