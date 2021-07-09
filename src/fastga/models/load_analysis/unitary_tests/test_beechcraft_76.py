"""
Test load_analysis module
"""
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

import numpy as np
import pytest

from fastoad.module_management.service_registry import RegisterPropulsion

from ..aerostructural_loads import AerostructuralLoad
from ..structural_loads import StructuralLoads
from ..aerodynamic_loads import AerodynamicLoads

from tests.testing_utilities import run_system, get_indep_var_comp, list_inputs


XML_FILE = "beechcraft_76.xml"


def test_compute_shear_stress():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AerostructuralLoad()), __file__, XML_FILE)
    cl_vector_only_prop = [0.04, 0.13, 0.21, 0.3, 0.39, 0.47, 0.56, 0.68, 0.84, 1.01, 1.17,
                           1.34, 1.51, 1.67, 1.84, 2.01, 2.18, 2.35, 2.51, 2.68, 2.85, 3.02,
                           3.19, 3.35, 3.52, 3.68, 3.85, 4.01, 4.18, 4.34, 4.5, 4.66, 4.81,
                           4.97, 5.13, 5.28, 5.43, 5.58, 5.73, 0., 0., 0., 0., 0.,
                           0., 0., 0., 0., 0., 0.]
    y_vector = [1.43, 1.42, 1.42, 1.42, 1.42, 1.41, 1.42, 1.41, 1.4, 1.4, 1.41,
                1.4, 1.4, 1.46, 1.5, 1.38, 1.35, 1.36, 1.35, 1.34, 1.33, 1.32,
                1.31, 1.3, 1.28, 1.26, 1.24, 1.21, 1.19, 1.16, 1.13, 1.09, 1.05,
                1.01, 0.95, 0.88, 0.79, 0.67, 0.63, 0., 0., 0., 0., 0.,
                0., 0., 0., 0., 0., 0.]
    ivc.add_output(
        "data:aerodynamics:slipstream:wing:cruise:only_prop:CL_vector", cl_vector_only_prop
    )
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:Y_vector", y_vector, units="m")
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:velocity", 82.3111, units="m/s")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AerostructuralLoad(), ivc)
    shear_max_mass_condition = problem.get_val("data:loads:max_shear:mass", units="kg")
    assert shear_max_mass_condition == pytest.approx(1747.3, abs=1e-1)
    shear_max_lf_condition = problem.get_val("data:loads:max_shear:load_factor")
    assert shear_max_lf_condition == pytest.approx(3.8, abs=1e-2)
    lift_shear_diagram = problem.get_val("data:loads:max_shear:lift_shear", units="N")
    lift_root_shear = lift_shear_diagram[0]
    assert lift_root_shear == pytest.approx(147551.45, abs=1)
    weight_shear_diagram = problem.get_val("data:loads:max_shear:weight_shear", units="N")
    weight_root_shear = weight_shear_diagram[0]
    assert weight_root_shear == pytest.approx(-21398.3, abs=1)


def test_compute_root_bending_moment():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AerostructuralLoad()), __file__, XML_FILE)
    cl_vector_only_prop = [0.04, 0.13, 0.21, 0.3, 0.39, 0.47, 0.56, 0.68, 0.84, 1.01, 1.17,
                           1.34, 1.51, 1.67, 1.84, 2.01, 2.18, 2.35, 2.51, 2.68, 2.85, 3.02,
                           3.19, 3.35, 3.52, 3.68, 3.85, 4.01, 4.18, 4.34, 4.5, 4.66, 4.81,
                           4.97, 5.13, 5.28, 5.43, 5.58, 5.73, 0., 0., 0., 0., 0.,
                           0., 0., 0., 0., 0., 0.]
    y_vector = [1.43, 1.42, 1.42, 1.42, 1.42, 1.41, 1.42, 1.41, 1.4, 1.4, 1.41,
                1.4, 1.4, 1.46, 1.5, 1.38, 1.35, 1.36, 1.35, 1.34, 1.33, 1.32,
                1.31, 1.3, 1.28, 1.26, 1.24, 1.21, 1.19, 1.16, 1.13, 1.09, 1.05,
                1.01, 0.95, 0.88, 0.79, 0.67, 0.63, 0., 0., 0., 0., 0.,
                0., 0., 0., 0., 0., 0.]
    ivc.add_output(
        "data:aerodynamics:slipstream:wing:cruise:only_prop:CL_vector", cl_vector_only_prop
    )
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:Y_vector", y_vector, units="m")
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:velocity", 82.3111, units="m/s")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AerostructuralLoad(), ivc)
    max_rbm_mass_condition = problem.get_val("data:loads:max_rbm:mass", units="kg")
    assert max_rbm_mass_condition == pytest.approx(1568.4, abs=1e-1)
    max_rbm_lf_condition = problem.get_val("data:loads:max_rbm:load_factor")
    assert max_rbm_lf_condition == pytest.approx(3.8, abs=1e-2)
    lift_rbm_diagram = problem.get_val("data:loads:max_rbm:lift_rbm", units="N*m")
    lift_rbm = lift_rbm_diagram[0]
    assert lift_rbm == pytest.approx(391838, abs=1)
    weight_rbm_diagram = problem.get_val("data:loads:max_rbm:weight_rbm", units="N*m")
    weight_rbm = weight_rbm_diagram[0]
    assert weight_rbm == pytest.approx(-34939, abs=1)


def test_compute_mass_distribution():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(StructuralLoads()), __file__, XML_FILE)
    load_factor_shear = 4.0
    ivc.add_output("data:loads:max_shear:load_factor", load_factor_shear)
    load_factor_rbm = 4.0
    ivc.add_output("data:loads:max_rbm:load_factor", load_factor_rbm)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(StructuralLoads(), ivc)
    point_mass_array = problem.get_val(
        "data:loads:structure:ultimate:force_distribution:point_mass", units="N/m"
    )
    point_mass_result = np.array(
        [-0., -0., -0., -0., -0., -0.,
         -0., -0., -0., -24551.9, -24551.9, -24551.9,
         -24551.9, -24551.9, -0., -0., -0., -0.,
         -0., -0., -0., -0., -0., -145568.2,
         -145568.2, -145568.2, -145568.2, -145568.2, -145568.2, -0.,
         -0., -0., -0., -0., -0., -0.,
         -0., -0., -0., -0., -0., -0.,
         -0., -0., -0., -0., -0., -0.,
         -0., -0., -0., -0., -0., -0.,
         -0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )
    assert np.max(np.abs(point_mass_array - point_mass_result)) <= 1e-1
    wing_mass_array = problem.get_val(
        "data:loads:structure:ultimate:force_distribution:wing", units="N/m"
    )
    wing_mass_result = np.array(
        [-592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6,
         -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6,
         -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6,
         -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6,
         -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6,
         -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6,
         -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, -592.6, 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )

    assert np.max(np.abs(wing_mass_result - wing_mass_array)) <= 1e-1
    fuel_mass_array = problem.get_val(
        "data:loads:structure:ultimate:force_distribution:fuel", units="N/m"
    )
    fuel_mass_result = np.array(
        [-196.5, -196.5, -196.5, -196.5, -196.5, -196.5, -196.5, -196.5,
         -196.5, -196.5, -196.5, -982.6, -982.6, -982.6, -982.6, -982.6,
         -982.6, -982.6, -982.6, -982.6, -491.3, -491.3, -491.3, -491.3,
         -491.3, -491.3, -491.3, -491.3, -491.3, -491.3, -491.3, -491.3,
         -982.6, -982.6, -982.6, -982.6, -982.6, -982.6, -982.6, -982.6,
         -982.6, -982.6, -982.6, -982.6, -982.6, -982.6, -982.6, -982.6,
         -982.6, -982.6, -982.6, -982.6, -982.6, -982.6, -982.7, 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )
    assert np.max(np.abs(fuel_mass_result - fuel_mass_array)) <= 1e-1


def test_compute_structure_shear():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(StructuralLoads()), __file__, XML_FILE)
    ivc.add_output("data:loads:max_shear:load_factor", 4.0)
    ivc.add_output("data:loads:max_rbm:load_factor", 4.0)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(StructuralLoads(), ivc)
    point_mass_array = problem.get_val("data:loads:structure:ultimate:shear:point_mass", units="N")
    point_mass_result = np.array(
        [-8067.5, -8067.5, -8067.5, -8067.5, -8067.5, -8067.5, -8067.5,
         -8067.5, -8067.5, -8055.3, -7770.3, -7485.4, -7200.4, -6915.5,
         -6903.2, -6903.2, -6903.2, -6903.2, -6903.2, -6903.2, -6903.2,
         -6903.2, -6903.2, -6830.4, -5141., -3451.6, -2708.3, -1762.2,
         -72.8, 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(point_mass_array - point_mass_result)) <= 1e-1
    wing_mass_array = problem.get_val("data:loads:structure:ultimate:shear:wing", units="N")
    wing_mass_result = np.array(
        [-3438.9, -3406., -3340.1, -3274.3, -3208.4, -3142.5, -3076.6,
         -3010.8, -2984.3, -2983.7, -2976.9, -2970., -2963.1, -2956.2,
         -2955.6, -2931.2, -2837.5, -2743.4, -2648.8, -2553.7, -2458.3,
         -2362.6, -2284., -2283.4, -2276.6, -2269.7, -2266.7, -2262.8,
         -2255.9, -2255.3, -2170.5, -2074.3, -1978., -1881.6, -1785.4,
         -1689.2, -1593.3, -1497.5, -1402.1, -1307., -1212.3, -1118.1,
         -1024.4, -931.2, -838.7, -746.9, -655.8, -565.5, -476.,
         -387.3, -299.6, -212.8, -126.9, -42.1, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(wing_mass_result - wing_mass_array)) <= 1e-1
    fuel_mass_array = problem.get_val("data:loads:structure:ultimate:shear:fuel", units="N")
    fuel_mass_result = np.array(
        [-4686.8, -4675.9, -4654., -4632.2, -4610.3, -4588.5, -4566.6,
         -4544.8, -4536., -4535.8, -4533.5, -4526.7, -4515.3, -4503.9,
         -4502.9, -4462.3, -4307.1, -4151., -3994.1, -3836.5, -3717.8,
         -3638.5, -3573.4, -3572.9, -3567.2, -3561.5, -3559., -3555.8,
         -3550.1, -3549.6, -3479.3, -3399.5, -3279.7, -3120., -2960.4,
         -2800.9, -2641.8, -2483., -2324.8, -2167.1, -2010.1, -1853.9,
         -1698.5, -1544.1, -1390.7, -1238.4, -1087.4, -937.6, -789.2,
         -642.2, -496.7, -352.8, -210.5, -69.9, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(fuel_mass_result - fuel_mass_array)) <= 1e-1


def test_compute_structure_bending():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(StructuralLoads()), __file__, XML_FILE)
    ivc.add_output("data:loads:max_shear:load_factor", 4.0)
    ivc.add_output("data:loads:max_rbm:load_factor", 4.0)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(StructuralLoads(), ivc)
    point_mass_array = problem.get_val(
        "data:loads:structure:ultimate:root_bending:point_mass", units="N*m"
    )
    point_mass_result = np.array(
        [-14541.1, -14092.7, -13196., -12299.4, -11402.7, -10506.,
         -9609.4, -8712.7, -8352.6, -8344.5, -8252.7, -8164.2,
         -8078.9, -7997., -7990.1, -7705.2, -6614.6, -5517.8,
         -4415.5, -3308.4, -2197.1, -1082.3, -167.1, -160.2,
         -90.8, -40.9, -25.2, -10.6, 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )
    assert np.max(np.abs(point_mass_array - point_mass_result)) <= 1e-1
    wing_mass_array = problem.get_val(
        "data:loads:structure:ultimate:root_bending:wing", units="N*m"
    )
    wing_mass_result = np.array(
        [-9977.7, -9787.5, -9412.6, -9045.1, -8684.8, -8331.8, -7986.2,
         -7647.9, -7514.1, -7511.1, -7476.6, -7442.1, -7407.6, -7373.3,
         -7370.3, -7248.8, -6793.1, -6349.8, -5919.3, -5502.1, -5098.7,
         -4709.4, -4401.4, -4399.1, -4372.7, -4346.3, -4334.7, -4320.,
         -4293.8, -4291.5, -3974.9, -3630.1, -3300.8, -2987.2, -2689.4,
         -2407.5, -2141.7, -1892., -1658.5, -1441.2, -1239.9, -1054.7,
         -885.3, -731.7, -593.5, -470.7, -362.8, -269.8, -191.1,
         -126.6, -75.7, -38.2, -13.6, -1.5, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(wing_mass_result - wing_mass_array)) <= 1e-1
    fuel_mass_array = problem.get_val(
        "data:loads:structure:ultimate:root_bending:fuel", units="N*m"
    )
    fuel_mass_result = np.array(
        [-15514.4, -15254.2, -14735.7, -14219.7, -13706., -13194.8,
         -12686., -12179.7, -11977., -11972.5, -11919.8, -11867.2,
         -11814.8, -11762.4, -11757.9, -11572.9, -10880.2, -10208.3,
         -9558., -8930.1, -8325.2, -7731.2, -7253.2, -7249.6,
         -7208.2, -7166.8, -7148.6, -7125.5, -7084.3, -7080.7,
         -6577.8, -6019.1, -5473.2, -4953.1, -4459.3, -3991.9,
         -3551.2, -3137.2, -2750.1, -2389.7, -2055.9, -1748.8,
         -1468., -1213.2, -984.1, -780.4, -601.6, -447.3,
         -316.9, -209.9, -125.5, -63.3, -22.5, -2.5,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )
    assert np.max(np.abs(fuel_mass_result - fuel_mass_array)) <= 1e-1


def test_compute_lift_distribution():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AerodynamicLoads()), __file__, XML_FILE)
    ivc.add_output("data:loads:max_shear:load_factor", 4.0)
    ivc.add_output("data:loads:max_shear:mass", 1747., units="kg")
    ivc.add_output("data:loads:max_rbm:load_factor", 4.0)
    ivc.add_output("data:loads:max_rbm:mass", 1568., units="kg")
    cl_vector_only_prop = [0.04, 0.13, 0.21, 0.3, 0.39, 0.47, 0.56, 0.68, 0.84, 1.01, 1.17,
                           1.34, 1.51, 1.67, 1.84, 2.01, 2.18, 2.35, 2.51, 2.68, 2.85, 3.02,
                           3.19, 3.35, 3.52, 3.68, 3.85, 4.01, 4.18, 4.34, 4.5, 4.66, 4.81,
                           4.97, 5.13, 5.28, 5.43, 5.58, 5.73, 0., 0., 0., 0., 0.,
                           0., 0., 0., 0., 0., 0.]
    y_vector = [1.43, 1.42, 1.42, 1.42, 1.42, 1.41, 1.42, 1.41, 1.4, 1.4, 1.41,
                1.4, 1.4, 1.46, 1.5, 1.38, 1.35, 1.36, 1.35, 1.34, 1.33, 1.32,
                1.31, 1.3, 1.28, 1.26, 1.24, 1.21, 1.19, 1.16, 1.13, 1.09, 1.05,
                1.01, 0.95, 0.88, 0.79, 0.67, 0.63, 0., 0., 0., 0., 0.,
                0., 0., 0., 0., 0., 0.]
    ivc.add_output(
        "data:aerodynamics:slipstream:wing:cruise:only_prop:CL_vector", cl_vector_only_prop
    )
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:Y_vector", y_vector, units="m")
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:velocity", 82.3111, units="m/s")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AerodynamicLoads(), ivc)
    lift_array = problem.get_val("data:loads:aerodynamic:ultimate:force_distribution", units="N/m")
    lift_result = np.array(
        [6257.1, 6257.1, 6256.9, 6258.7, 6256., 6250.9, 6248.4,
         6837.1, 6968.4, 6971.4, 7005.5, 7041.7, 7094.2, 7146.7,
         7151.2, 7337.9, 8279.8, 11151.1, 18189.2, 33070.4, 32166.4,
         31129.4, 30287.1, 30280.7, 30207., 30133.3, 30100.8, 30059.1,
         29984.6, 29978.2, 29059.8, 27990.8, 26938.2, 25884.6, 24835.9,
         23773.9, 22716.8, 21654., 20592.6, 19519.5, 18456.4, 17379.7,
         16312.5, 15240.5, 14170.7, 13083.4, 11998.2, 10898.7, 9783.9,
         8601.8, 7382.8, 6067.2, 4595.8, 2814.8, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(lift_array - lift_result)) <= 1e-1
