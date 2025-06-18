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
        print("[test01.test_warp_kernel_ui] Extension startup")

        wp.init()
        self._count = 0
        self._num_points = 1024
        self._outputstring = ""

        self._window = ui.Window("Test01 Warp Kernel UI", width=500, height=800)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("")
                label.text = f"# Runs: 0"

                def on_click():
                    self._count += 1
                    label.text = f"# Runs: {self._count}"
                    # allocate an array of 3d points
                    points = wp.array(np.random.rand(self._num_points, 3), dtype=wp.vec3)
                    lengths = wp.zeros(self._num_points, dtype=float)
                    self._outputstring = ""
                    ps = points.numpy()
                    for i in range(len(ps)):
                        v = ps[i]
                        self._outputstring += f"Index {i}: ({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})\n"

                    # launch kernel
                    wp.launch(kernel=length,
                            dim=len(points),
                            inputs=[points, lengths])

                    l = len(points)

                    print(l)
                    print(points)
                    ##print(lengths)

                with ui.HStack():
                    ui.Button("Run Kernel", clicked_fn=on_click)

                with ui.VStack():
                     ui.Label(f"points: {self._num_points}", style={"alignment": ui.Alignment.RIGHT_CENTER})
                with ui.VStack():
                     ui.Label(" content1", style={"alignment": ui.Alignment.RIGHT_CENTER})
                # with ui.VStack():
                #      ui.Label(self._outputstring, style={"alignment": ui.Alignment.RIGHT_CENTER})
                with ui.VStack():
                     ui.Label(" content2", style={"alignment": ui.Alignment.RIGHT_CENTER})

                print(">>> self._outputstring")
                print(self._outputstring)

    def on_shutdown(self):
        print("[test01.test_warp_kernel_ui] Extension shutdown")
