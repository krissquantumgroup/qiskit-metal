# Jaseung Ku
# 2025. 08
# Based on transmon_pocket_cl.py, just inherit TransmonPocket6 from transmon_pockt_6.py
# Transmon with 6 connection pads with a flux line

"""Transmon Pocket 6 with Flux line

Pocket "axis"
        _________________
        |               |
        |_______________|       ^
        ________x________       |  N
        |               |       |
        |_______________|

Child of 'standard' transmon pocket.
"""
# pylint: disable=invalid-name
# Modification of Transmon Pocket Object to include a flux line (would be better to just make as a child)

import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.qubits.transmon_pocket_6 import TransmonPocket6


class TransmonPocket6FL(TransmonPocket6):  # pylint: disable=invalid-name
    """The base `TransmonPocket6` class.

    Inherits `TransmonPocket` class.

    Create a standard pocket transmon qubit for a ground plane,
    with two pads connected by a junction (see drawing below).

    Connector lines can be added using the `connection_pads`
    dictionary. Each connector line has a name and a list of default
    properties.

    This is a child of TransmonPocket, see TransmonPocket for the variables and
    description of that class.

    ::

        _________________
        |               |
        |_______________|       ^
        ________x________       |  N
        |               |       |
        |_______________|


    .. image::
        transmon_pocket_cl.png

    .. meta::
        Transmon Pocket flux Line

    BaseQubit Default Options:
        * connection_pads: empty Dict -- The dictionary which contains all active connection lines for the qubit.
        * _default_connection_pads: empty Dict -- The default values for the (if any) connection lines of the qubit.

    TransmonPocket Default Options:
        * pad_gap: '30um' -- The distance between the two flux islands, which is also the resulting 'length' of the pseudo junction
        * inductor_width: '20um' -- Width of the pseudo junction between the two charge islands (if in doubt, make the same as pad_gap). Really just for simulating in HFSS / other EM software
        * pad_width: '455um' -- The width (x-axis) of the charge island pads
        * pad_height: '90um' -- The size (y-axis) of the charge island pads
        * pocket_width: '650um' -- Size of the pocket (cut out in ground) along x-axis
        * pocket_height: '650um' -- Size of the pocket (cut out in ground) along y-axis
        * _default_connection_pads: Dict
            * pad_gap: '15um' -- Space between the connector pad and the charge island it is nearest to
            * pad_width: '125um' -- Width (x-axis) of the connector pad
            * pad_height: '30um' -- Height (y-axis) of the connector pad
            * pad_cpw_shift: '5um' -- Shift the connector pad cpw line by this much away from qubit
            * pad_cpw_extent: '25um' -- Shift the connector pad cpw line by this much away from qubit
            * cpw_width: 'cpw_width' -- Center trace width of the CPW line
            * cpw_gap: 'cpw_gap' -- Dielectric gap width of the CPW line
            * cpw_extend: '100um' -- Depth the connector line extends into ground (past the pocket edge)
            * pocket_extent: '5um' -- How deep into the pocket should we penetrate with the cpw connector (into the fround plane)
            * pocket_rise: '65um' -- How far up or downrelative to the center of the transmon should we elevate the cpw connection point on the ground plane
            * loc_W: '+1' -- Width location  only +-1
            * loc_H: '+1' -- Height location only +-1

    Default Options:
        make_FL=True,
        fl_gap='6um',  # the cpw dielectric gap of the flux line
        fl_width='10um',  # the cpw trace width of the flux line
        fl_taper_width='5um', # the tapered cpw trace width of the flux line
        fl_hline_length='100um',
        fl_length='100um', 
        fl_taper_length='60um', # length of the tapered cpw
        fl_ground_gap='5um',  # how much ground between the flux line and the qubit pocket. 
        fl_off_center= '10um',  # distance from the center axis the qubit pocket is built on
        fl_loc = 'left' # 'left' or 'right' 
    """
    component_metadata = Dict(short_name='Q', _qgeometry_table_poly='True')
    """Component metadata"""

    default_options = Dict(
        make_FL=True,
        fl_gap='6um',  # the cpw dielectric gap of the flux line
        fl_width='10um',  # the cpw trace width of the flux line
        fl_taper_width='5um', # the tapered cpw trace width of the flux line
        fl_hline_length='100um',
        fl_length='100um', 
        fl_taper_length='60um', # length of the tapered cpw
        fl_ground_gap='5um',  # how much ground between the flux line and the qubit pocket. 
        fl_off_center= '10um',  # distance from the center axis the qubit pocket is built on
        fl_loc = 'left' # 'left' or 'right' 
    )
    """Default drawing options"""

    TOOLTIP = """Create a standard pocket transmon qubit for a ground plane,
    with two pads connected by a junction"""

    def make(self):
        """Define the way the options are turned into QGeometry."""
        super().make()

        if self.options.make_FL == True:
            self.make_flux_line()


#####################################################################

    def make_flux_line(self):
        """Creates the flux line if the user has flux line option to TRUE."""

        # Grab option values
        name = 'Flux_Line'

        p = self.p

        fl_line = draw.LineString([(0, 0), (0, -p.fl_length)])

        # fl_cpw = draw.buffer(fl_line, p.fl_width/2)
        fl_cpw = draw.Polygon([
            (-p.fl_taper_width/2, 0),
            (p.fl_taper_width/2, 0),
            (p.fl_width/2, -p.fl_taper_length),
            (p.fl_width/2, -p.fl_length),
            (-p.fl_width/2, -p.fl_length),
            (-p.fl_width/2, -p.fl_taper_length)
        ])            

        fl_etcher = draw.buffer(fl_line, p.fl_width/2 + p.fl_gap)
        fl_etcher_tmp = draw.Polygon([
            (-p.fl_hline_length/2,0), (p.fl_hline_length/2, 0), (0, -p.fl_taper_length)
        ])
        fl_etcher = draw.unary_union([fl_etcher, fl_etcher_tmp])

        polys = [fl_cpw, fl_etcher, fl_line]

        # Move to the final position
        polys = draw.translate(
                polys, 
                p.fl_off_center, 
                -p.pocket_width/2-p.fl_ground_gap
                )
        if p.fl_loc == 'left':            
            polys = draw.rotate(polys, p.orientation - 90, (0,0))
        elif p.fl_loc=='right':
            polys = draw.rotate(polys, p.orientation + 90, (0,0))                
        polys = draw.translate(polys, p.pos_x, p.pos_y)

        [fl_cpw, fl_etcher, fl_line] = polys

        # Generating pins
        points = list(draw.shapely.geometry.shape(fl_line).coords)
        self.add_pin(name, points, p.fl_width, input_as_norm=True)

        # Adding to qgeometry table
        self.add_qgeometry('poly', dict(fl_cpw=fl_cpw))
        self.add_qgeometry('path', dict(fl_line=fl_line), width=p.fl_width)
        self.add_qgeometry('poly', dict(fl_etcher=fl_etcher), subtract=True)
