import omni.ext
import omni.ui as ui
import warp as wp
import numpy as np


# Warp kernel to computes the lengths of 3D vectors
@wp.kernel
def length(points: wp.array(dtype=wp.vec3),
           lengths: wp.array(dtype=float)):

    # thread index
    tid = wp.tid()

    # compute distance of each point from origin
    lengths[tid] = wp.length(points[tid])


# Any class derived from `omni.ext.IExt` in the top level module (defined in `python.modules` of `extension.toml`) will
# be instantiated when the extension gets enabled, and `on_startup(ext_id)` will be called.
# Later when the extension gets disabled on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is the current extension id. It can be used with the extension manager to query additional information,
    # like where this extension is located on the filesystem.
    def on_startup(self, ext_id):
        print("[{{ extension_name }}] Extension startup")

        wp.init()
        self._count = 0
        self._num_points = 1024

        self._window = ui.Window("{{ extension_display_name }}", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("")

                def on_click():
                    self._count += 1
                    label.text = f"# Runs: {self._count}"
                    # allocate an array of 3d points
                    points = wp.array(np.random.rand(self._num_points, 3), dtype=wp.vec3)
                    lengths = wp.zeros(self._num_points, dtype=float)

                    # launch kernel
                    wp.launch(kernel=length,
                            dim=len(points),
                            inputs=[points, lengths])

                    print(lengths)



                with ui.HStack():
                    ui.Button("Run Kernel", clicked_fn=on_click)

    def on_shutdown(self):
        print("[{{ extension_name }}] Extension shutdown")