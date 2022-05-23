"""FAST - Copyright (c) 2021 ONERA ISAE."""

#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import openmdao.api as om

from fastoad.module_management.service_registry import RegisterOpenMDAOSystem
from fastoad.module_management.constants import ModelDomain

from .mission_vector import MissionVector
from fastga.models.performances.mission.takeoff import TakeOffPhase


@RegisterOpenMDAOSystem("fastga.performances.mission_vector", domain=ModelDomain.OTHER)
class FullMission(om.Group):
    """Find the conditions necessary for the aircraft equilibrium."""

    def initialize(self):

        self.options.declare("propulsion_id", default=None, types=str, allow_none=True)
        self.options.declare("out_file", default="", types=str)

    def setup(self):

        self.add_subsystem(
            "takeoff", TakeOffPhase(propulsion_id=self.options["propulsion_id"]), promotes=["*"]
        )
        self.add_subsystem(
            "solve_equilibrium",
            MissionVector(
                out_file=self.options["out_file"], propulsion_id=self.options["propulsion_id"]
            ),
            promotes=["*"],
        )