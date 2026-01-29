# jk_library.py
# Jaseung Ku
# 2025.Aug

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

from ... import config
if not config.is_building_docs():
    from qiskit_metal import is_true


class ChipCorner(QComponent):
    """
    This class is a template
	Use this class as a blueprint to put together for your components - have fun
    
    .. meta::
        My QComponent

    """

    # Edit these to define your own template options for creation
    # Default drawing options
    default_options = Dict(
        pos_x='0um',
        pos_y='0um',
        width='10um', 
        height='300um',
        orientation='0',
        layer='1'
        )
    """Default drawing options"""

    # Name prefix of component, if user doesn't provide name
    component_metadata = Dict(short_name='component')
    """Component metadata"""

    def make(self):
        """Convert self.options into QGeometry."""

        p = self.parse_options()  # Parse the string options into numbers

        # EDIT HERE - Replace the following with your code
        # Create some raw geometry
        # Use autocompletion for the `draw.` module (use tab key)
        rec1 = draw.rectangle(p.width, p.height, p.pos_x, p.pos_y)
        rec1 = draw.translate(rec1, p.width/2, p.height/2)
        rec2 = draw.rectangle(p.height, p.width, p.pos_x, p.pos_y)
        rec2 = draw.translate(rec2, p.height/2, p.width/2)
        rec_union = draw.union(rec1, rec2)
        rec_union = draw.rotate(rec_union, p.orientation, (p.pos_x, p.pos_y))

        geom = {'my_polygon': rec_union}
        self.add_qgeometry('poly', geom, layer=p.layer, subtract=False)
        

class TestStructure(QComponent):
    """
 	Test structure for Josephson junctions.
    Just two pads    
    .. meta::
        My QComponent

    """

    # Edit these to define your own template options for creation
    # Default drawing options
    default_options = Dict(
        pos_x='0um',
        pos_y='0um',
        pad_width='400um',
        pad_height='300um',
        pad_gap='60um',
        bridge_width='40um',
        bridge_gap='20um',
        pocket_gap='50um',
        orientation='0',
        layer='1'
        )
    """Default drawing options"""

    # Name prefix of component, if user doesn't provide name
    component_metadata = Dict(short_name='component')
    """Component metadata"""

    def make(self):
        """Convert self.options into QGeometry."""

        p = self.parse_options()  # Parse the string options into numbers

        rec1 = draw.rectangle(p.pad_width, p.pad_height)
        rec1 = draw.translate(rec1, 0, p.pad_height/2+p.pad_gap/2)
        rec2 = draw.rectangle(p.pad_width, p.pad_height)
        rec2 = draw.translate(rec2, 0, -p.pad_height/2-p.pad_gap/2)
        bridge_height = (p.pad_gap-p.bridge_gap)/2
        bridge1 = draw.rectangle(p.bridge_width, bridge_height)
        bridge1 = draw.translate(bridge1, 0, bridge_height/2+p.bridge_gap/2)
        bridge2 = draw.rectangle(p.bridge_width, bridge_height)
        bridge2 = draw.translate(bridge2, 0, -bridge_height/2-p.bridge_gap/2)
        rec_union = draw.union(rec1, rec2, bridge1, bridge2)
      
        rec_pocket = draw.rectangle(p.pad_width, p.pad_height*2+p.pad_gap)
        rec_pocket = draw.buffer(rec_pocket, p.pocket_gap)

        polys = [rec_union, rec_pocket]
        
        polys = draw.rotate(polys, p.orientation, (0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)

        [rec_union, rec_pocket] = polys

        self.add_qgeometry('poly', dict(rec_union=rec_union))
        self.add_qgeometry('poly', dict(rec_pocket=rec_pocket),  subtract=True)
        
      
