# code from https://stackoverflow.com/questions/52910187/how-to-make-a-polygon-radar-spider-chart-in-python

import numpy as np
import csv

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
    
    class RadarTransform(PolarAxes.PolarTransform):
        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        
        PolarTransform = RadarTransform

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

def generatePlot(data, colors):
    name = data[1][0]
    filename = "img/" + name + ".png"
    N = len(data[0])
    theta = radar_factory(N, frame='polygon')

    spoke_labels = data.pop(0)
    title, case_data = data[0]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    plt.ylim([0,1])
    ax.set_rgrids([0.25, 0.5, 0.75])
    ax.set_title(title,  position=(0.5, 1.1), ha='center')

    for d in case_data:
        line = ax.plot(theta, d, color=colors[name]) # add label here for legend
        ax.fill(theta, d,  alpha=0.4, color=colors[name])
    ax.set_varlabels(spoke_labels)
    
    plt.savefig(filename)

def openCSV(file):
    """ read csv file to a list """
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def main():
    data = openCSV("result.csv")
    parties = data.pop(0)
    
    # different colors for each party
    colorcodes = ["#878784", "#E30613", "#E53136", "#84B414", "#F9B200", "#0060AD", "#9AC31C", "#F5AE40", "#0E52A0", "#FFD200", "#E6222D", "#329F4F", "#878784"]
    colors = {parties [i] : colorcodes[i] for i in range(len(parties))}
    #print(colors)
    
    
    #convert entries from string to float
    for i in range(0, len(data)):
        data[i] = list(map(float, data[i]))
    # print(parties)
    # print(data)

    # generate plots for all parties
    for i in range(len(data)):
        print("Generating for", parties[i])
        arg = [parties[0:i]+parties[i+1:], (parties[i], [data[i][0:i]+data[i][i+1:]])]
        generatePlot(arg, colors)


    """
    # structure for multiple graphs on a plot:
    data = [['SP', 'GLP', 'Mitte', 'FDP', 'SVP', 'LP', 'Piraten', 'Grüne'],
            ('TITLE $\int_{-\infty}^{\infty}\sin^2(3x)dx$', [
                [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00],
                [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00],
                [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00],
                [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00],
                [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00]])]
    """

if __name__ == '__main__':
    main()