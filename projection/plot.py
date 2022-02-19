# code from https://stackoverflow.com/questions/52910187/how-to-make-a-polygon-radar-spider-chart-in-python
# user: ImportanceOfBeingErnest

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)


        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)


                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def generatePlot(data):

    N = len(data[0])
    theta = radar_factory(N, frame='polygon')

    spoke_labels = data.pop(0)
    title, case_data = data[0]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
    #ax.set_rgrids([0.25, 0.5, 0.75])
    ax.set_title(title,  position=(0.5, 1.1), ha='center')

    for d in case_data:
        line = ax.plot(theta, d) # add label here for legend
        ax.fill(theta, d,  alpha=0.25)
    ax.set_varlabels(spoke_labels)

    #plt.show()
    #plt.legend()
    plt.savefig("plot.png")


def main():
    parties = ["Result", "SP", "Gruene", "EVP", "GLP", "Mitte", "FDP", "SVP", "EDU", "Piraten", "PdA", "LP"]
    
    data = [parties, (parties[4], [[0.6957, 0.7826, 0.7826, 0.6739, 1.0000, 0.7174, 0.5652, 0.3696, 0.4565, 0.7391, 0.6957, 0.4783]])]

    """
    data = [['SP', 'GLP', 'Mitte', 'FDP', 'SVP', 'LP', 'Piraten', 'Grüne'],
            ('TITLE $\int_{-\infty}^{\infty}\sin^2(3x)dx$', [
                [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00],
                [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00],
                [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00],
                [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00],
                [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00]])]
    """

    generatePlot(data)

if __name__ == '__main__':
    main()