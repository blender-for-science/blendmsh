# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "blendmsh",
    "author" : "Senthur Raj",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Mesh"
}

import bpy

from .properties import BlendmshProperties
from .panel import BLENDMSH_PT_Panel
from .processor import BLENDMSH_OT_Meshinit, BLENDMSH_OT_Meshproc, BLENDMSH_OT_Physicalgroups
from .preferences import BlendmshPreferences, BlendmshInstaller

def register():
    bpy.utils.register_class(BlendmshPreferences)
    bpy.utils.register_class(BlendmshInstaller)
    bpy.utils.register_class(BlendmshProperties)
    bpy.utils.register_class(BLENDMSH_PT_Panel)
    bpy.types.Scene.blendmsh = bpy.props.PointerProperty(type=BlendmshProperties)

    bpy.utils.register_class(BLENDMSH_OT_Meshinit)
    bpy.utils.register_class(BLENDMSH_OT_Meshproc)
    bpy.utils.register_class(BLENDMSH_OT_Physicalgroups)

def unregister():
    bpy.utils.unregister_class(BlendmshPreferences)
    bpy.utils.unregister_class(BlendmshInstaller)
    bpy.utils.unregister_class(BlendmshProperties)
    bpy.utils.unregister_class(BLENDMSH_PT_Panel)
    bpy.utils.unregister_class(BLENDMSH_OT_Meshinit)
    bpy.utils.unregister_class(BLENDMSH_OT_Meshproc)
    bpy.utils.unregister_class(BLENDMSH_OT_Physicalgroups)

if __name__ == "__main__":
    register()