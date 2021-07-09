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

XML_FILE = "cirrus_sr22.xml"


def _test_compute_shear_stress():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AerostructuralLoad()), __file__, XML_FILE)
    cl_vector_only_prop = [1.53, 1.53, 1.53, 1.52, 1.52, 1.52, 1.52, 1.51, 1.53, 1.55, 1.57,
                           1.58, 1.59, 1.6, 1.61, 1.62, 1.63, 1.64, 1.64, 1.65, 1.65, 1.65,
                           1.65, 1.66, 1.65, 1.65, 1.65, 1.65, 1.63, 1.63, 1.62, 1.61, 1.58,
                           1.55, 1.49, 1.43, 1.31, 1.14, 0.94, 0., 0., 0., 0., 0.,
                           0., 0., 0., 0., 0., 0.]
    y_vector = [0.05, 0.14, 0.23, 0.32, 0.41, 0.5, 0.59, 0.72, 0.88, 1.04, 1.21,
                1.37, 1.54, 1.7, 1.87, 2.04, 2.2, 2.37, 2.54, 2.7, 2.87, 3.04,
                3.2, 3.37, 3.53, 3.7, 3.86, 4.02, 4.18, 4.35, 4.5, 4.66, 4.82,
                4.97, 5.13, 5.28, 5.43, 5.58, 5.73, 0., 0., 0., 0., 0.,
                0., 0., 0., 0., 0., 0.]
    ivc.add_output(
        "data:aerodynamics:slipstream:wing:cruise:only_prop:CL_vector", cl_vector_only_prop
    )
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:Y_vector", y_vector, units="m")
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:velocity", 82.311, units="m/s")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AerostructuralLoad(), ivc)
    shear_max_mass_condition = problem.get_val("data:loads:max_shear:mass", units="kg")
    assert shear_max_mass_condition == pytest.approx(1426.3, abs=1e-1)
    shear_max_lf_condition = problem.get_val("data:loads:max_shear:load_factor")
    assert shear_max_lf_condition == pytest.approx(4.28, abs=1e-2)
    lift_shear_diagram = problem.get_val("data:loads:max_shear:lift_shear", units="N")
    lift_root_shear = lift_shear_diagram[0]
    assert lift_root_shear == pytest.approx(97568, abs=1)
    weight_shear_diagram = problem.get_val("data:loads:max_shear:weight_shear", units="N")
    weight_root_shear = weight_shear_diagram[0]
    assert weight_root_shear == pytest.approx(-6004.87, abs=1)


def test_compute_root_bending_moment():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AerostructuralLoad()), __file__, XML_FILE)
    cl_vector_only_prop = [1.53, 1.53, 1.53, 1.52, 1.52, 1.52, 1.52, 1.51, 1.53, 1.55, 1.57,
                           1.58, 1.59, 1.6, 1.61, 1.62, 1.63, 1.64, 1.64, 1.65, 1.65, 1.65,
                           1.65, 1.66, 1.65, 1.65, 1.65, 1.65, 1.63, 1.63, 1.62, 1.61, 1.58,
                           1.55, 1.49, 1.43, 1.31, 1.14, 0.94, 0., 0., 0., 0., 0.,
                           0., 0., 0., 0., 0., 0.]
    y_vector = [0.05, 0.14, 0.23, 0.32, 0.41, 0.5, 0.59, 0.72, 0.88, 1.04, 1.21,
                1.37, 1.54, 1.7, 1.87, 2.04, 2.2, 2.37, 2.54, 2.7, 2.87, 3.04,
                3.2, 3.37, 3.53, 3.7, 3.86, 4.02, 4.18, 4.35, 4.5, 4.66, 4.82,
                4.97, 5.13, 5.28, 5.43, 5.58, 5.73, 0., 0., 0., 0., 0.,
                0., 0., 0., 0., 0., 0.]
    ivc.add_output(
        "data:aerodynamics:slipstream:wing:cruise:only_prop:CL_vector", cl_vector_only_prop
    )
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:Y_vector", y_vector, units="m")
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:velocity", 82.311, units="m/s")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AerostructuralLoad(), ivc)
    max_rbm_mass_condition = problem.get_val("data:loads:max_rbm:mass", units="kg")
    assert max_rbm_mass_condition == pytest.approx(1426.3, abs=1e-1)
    max_rbm_lf_condition = problem.get_val("data:loads:max_rbm:load_factor")
    assert max_rbm_lf_condition == pytest.approx(4.28, abs=1e-2)
    lift_rbm_diagram = problem.get_val("data:loads:max_rbm:lift_rbm", units="N*m")
    lift_rbm = lift_rbm_diagram[0]
    assert lift_rbm == pytest.approx(246892, abs=1)
    weight_rbm_diagram = problem.get_val("data:loads:max_rbm:weight_rbm", units="N*m")
    weight_rbm = weight_rbm_diagram[0]
    assert weight_rbm == pytest.approx(-13190, abs=1)


def _test_compute_mass_distribution():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(StructuralLoads()), __file__, XML_FILE)
    ivc.add_output("data:loads:max_shear:load_factor", 4.0)
    ivc.add_output("data:loads:max_rbm:load_factor", 4.0)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(StructuralLoads(), ivc)
    point_mass_array = problem.get_val(
        "data:loads:structure:ultimate:force_distribution:point_mass", units="N/m"
    )
    point_mass_result = np.array([-0., -0., -0., -0., -0., -0.,
                                  -0., -0., -0., -16427.4, -16427.4, -16427.4,
                                  -16427.4, -16427.4, -16427.4, -0., -0., -0.,
                                  -0., -0., -0., -0., -0., -0.,
                                  -0., -0., -0., -0., -0., -0.,
                                  -0., -0., -0., -0., -0., -0.,
                                  -0., -0., -0., -0., -0., -0.,
                                  -0., -0., -0., -0., -0., -0.,
                                  0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0.,
                                  0., 0., 0.]
                                 )
    assert np.max(np.abs(point_mass_array - point_mass_result)) <= 1e-1
    wing_mass_array = problem.get_val(
        "data:loads:structure:ultimate:force_distribution:wing", units="N/m"
    )
    wing_mass_result = np.array(
        [-659.1, -652.1, -652.1, -652.1, -652.1, -652.1, -652.1, -652.1,
         -647.9, -647.9, -647.4, -647., -647., -646.3, -645.5, -645.5,
         -636.7, -626.4, -616., -605.6, -595.2, -584.7, -574.2, -563.7,
         -553.1, -542.6, -532.1, -521.5, -511., -500.5, -490., -479.5,
         -469.1, -458.8, -448.5, -438.2, -428., -417.9, -407.8, -397.8,
         -387.9, -378.1, -368.4, -358.8, -349.3, -339.9, -330.6, -329.5,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )
    assert np.max(np.abs(wing_mass_result - wing_mass_array)) <= 1e-1
    fuel_mass_array = problem.get_val(
        "data:loads:structure:ultimate:force_distribution:fuel", units="N/m"
    )
    fuel_mass_result = np.array(
        [-1103.2, -1091.4, -1091.4, -1091.4, -1091.4, -1091.4, -1091.4,
         -1091.4, -1084.5, -1084.5, -1083.7, -1082.9, -1082.9, -1081.7,
         -1080.5, -1080.4, -1065.7, -1048.5, -1031.1, -1013.7, -996.2,
         -978.7, -961.1, -943.5, -925.9, -908.2, -890.6, -872.9,
         -855.3, -837.7, -820.2, -802.7, -785.2, -767.9, -750.6,
         -733.5, -716.4, -699.4, -682.6, -665.9, -649.3, -632.9,
         -616.7, -600.6, -584.7, -569., -553.4, -551.6, 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(fuel_mass_result - fuel_mass_array)) <= 1e-1


def _test_compute_structure_shear():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(StructuralLoads()), __file__, XML_FILE)
    ivc.add_output("data:loads:max_shear:load_factor", 4.0)
    ivc.add_output("data:loads:max_rbm:load_factor", 4.0)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(StructuralLoads(), ivc)
    point_mass_array = problem.get_val("data:loads:structure:ultimate:shear:point_mass", units="N")
    point_mass_result = np.array([-778.7, -778.7, -778.7, -778.7, -778.7, -778.7, -778.7, -778.7,
                                  -778.7, -770.4, -579.9, -389.3, -376.5, -198.8, -8.2, 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0., 0., 0., 0., 0., 0.,
                                  0., 0., 0.]
                                 )
    assert np.max(np.abs(point_mass_array - point_mass_result)) <= 1e-1
    wing_mass_array = problem.get_val("data:loads:structure:ultimate:shear:wing", units="N")
    wing_mass_result = np.array([-2956.2, -2921.8, -2853.5, -2785.2, -2716.9, -2648.5, -2580.2,
                                 -2511.9, -2442.6, -2442., -2434.5, -2427., -2426.4, -2419.4,
                                 -2412., -2411.3, -2324.2, -2223., -2123., -2024.2, -1926.8,
                                 -1830.7, -1736.1, -1643.1, -1551.6, -1461.9, -1373.8, -1287.5,
                                 -1203.1, -1120.5, -1039.8, -961.1, -884.4, -809.6, -736.9,
                                 -666.2, -597.6, -531., -466.5, -404.1, -343.7, -285.4,
                                 -229.1, -174.8, -122.5, -72.2, -23.8, 0., 0.,
                                 0., 0., 0., 0., 0., 0., 0.,
                                 0., 0., 0., 0., 0., 0., 0.,
                                 0., 0., 0., 0., 0., 0., 0.,
                                 0., 0., 0., 0., 0.]
                                )
    assert np.max(np.abs(wing_mass_result - wing_mass_array)) <= 1e-1
    fuel_mass_array = problem.get_val("data:loads:structure:ultimate:shear:fuel", units="N")
    fuel_mass_result = np.array(
        [-4948., -4890.6, -4776.2, -4661.9, -4547.5, -4433.2, -4318.8,
         -4204.5, -4088.5, -4087.4, -4074.8, -4062.3, -4061.4, -4049.7,
         -4037.2, -4036.1, -3890.3, -3720.9, -3553.5, -3388.2, -3225.1,
         -3064.3, -2906., -2750.2, -2597.1, -2446.9, -2299.5, -2155.1,
         -2013.7, -1875.5, -1740.5, -1608.7, -1480.2, -1355.1, -1233.4,
         -1115.1, -1000.2, -888.8, -780.9, -676.4, -575.3, -477.6,
         -383.4, -292.5, -205., -120.8, -39.8, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(fuel_mass_result - fuel_mass_array)) <= 1e-1


def _test_compute_structure_bending():
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
        [-632.1, -591.3, -509.7, -428.2, -346.6, -265., -183.4, -101.9,
         -18.8, -18.1, -10.2, -4.6, -4.3, -1.2, 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0.]
    )
    assert np.max(np.abs(point_mass_array - point_mass_result)) <= 1e-1
    wing_mass_array = problem.get_val(
        "data:loads:structure:ultimate:root_bending:wing", units="N*m"
    )
    wing_mass_result = np.array(
        [-7571.3, -7417.3, -7114.8, -6819.4, -6531.2, -6250.1, -5976.2,
         -5709.5, -5445.4, -5442.9, -5414.6, -5386.5, -5384.6, -5358.3,
         -5330.3, -5327.9, -5006.2, -4642.1, -4292.3, -3957., -3636.5,
         -3330.6, -3039.6, -2763.3, -2501.8, -2254.9, -2022.6, -1804.8,
         -1601.1, -1411.5, -1235.6, -1073.2, -924., -787.6, -663.7,
         -552., -451.9, -363.1, -285.3, -217.9, -160.5, -112.6,
         -73.9, -43.8, -21.9, -7.7, -0.9, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(wing_mass_result - wing_mass_array)) <= 1e-1
    fuel_mass_array = problem.get_val(
        "data:loads:structure:ultimate:root_bending:fuel", units="N*m"
    )
    fuel_mass_result = np.array(
        [-12672.8, -12415.2, -11908.8, -11414.4, -10932., -10461.5,
         -10003.1, -9556.6, -9114.5, -9110.4, -9063.1, -9015.9,
         -9012.7, -8968.9, -8921.9, -8917.9, -8379.5, -7770.,
         -7184.5, -6623.3, -6086.7, -5574.8, -5087.7, -4625.2,
         -4187.5, -3774.3, -3385.5, -3020.8, -2680., -2362.6,
         -2068.2, -1796.4, -1546.6, -1318.3, -1111., -923.9,
         -756.4, -607.8, -477.5, -364.7, -268.6, -188.5,
         -123.6, -73.3, -36.6, -12.9, -1.4, 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0.,
         0., 0., 0.])
    assert np.max(np.abs(fuel_mass_result - fuel_mass_array)) <= 1e-1


def test_compute_lift_distribution():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AerodynamicLoads()), __file__, XML_FILE)
    ivc.add_output("data:loads:max_shear:load_factor", 4.28)
    ivc.add_output("data:loads:max_shear:mass", 1426.3, units="kg")
    ivc.add_output("data:loads:max_rbm:load_factor", 4.28)
    ivc.add_output("data:loads:max_rbm:mass", 1426.3, units="kg")
    cl_vector_only_prop = [1.53, 1.53, 1.53, 1.52, 1.52, 1.52, 1.52, 1.51, 1.53, 1.55, 1.57,
                           1.58, 1.59, 1.6, 1.61, 1.62, 1.63, 1.64, 1.64, 1.65, 1.65, 1.65,
                           1.65, 1.66, 1.65, 1.65, 1.65, 1.65, 1.63, 1.63, 1.62, 1.61, 1.58,
                           1.55, 1.49, 1.43, 1.31, 1.14, 0.94, 0., 0., 0., 0., 0.,
                           0., 0., 0., 0., 0., 0.]
    y_vector = [0.05, 0.14, 0.23, 0.32, 0.41, 0.5, 0.59, 0.72, 0.88, 1.04, 1.21,
                1.37, 1.54, 1.7, 1.87, 2.04, 2.2, 2.37, 2.54, 2.7, 2.87, 3.04,
                3.2, 3.37, 3.53, 3.7, 3.86, 4.02, 4.18, 4.35, 4.5, 4.66, 4.82,
                4.97, 5.13, 5.28, 5.43, 5.58, 5.73, 0., 0., 0., 0., 0.,
                0., 0., 0., 0., 0., 0.]
    ivc.add_output(
        "data:aerodynamics:slipstream:wing:cruise:only_prop:CL_vector", cl_vector_only_prop
    )
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:Y_vector", y_vector, units="m")
    ivc.add_output("data:aerodynamics:slipstream:wing:cruise:prop_on:velocity", 82.311, units="m/s")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AerodynamicLoads(), ivc)
    lift_array = problem.get_val("data:loads:aerodynamic:ultimate:force_distribution", units="N/m")
    lift_result = np.array(
        [14085.6, 13935.7, 13936.8, 13934.5, 13901.7, 13898.9, 13887.,
         13838., 13769.3, 13769.1, 13765.6, 13762.2, 13762., 13755.2,
         13747.9, 13747.2, 13660.2, 13591.1, 13477., 13327.9, 13153.7,
         12990., 12830.3, 12663.4, 12491.7, 12299.9, 12085.6, 11886.,
         11645.6, 11419.1, 11197.3, 10980.4, 10711.3, 10475.8, 10229.3,
         9975.2, 9687.5, 9447.7, 9169., 8888.8, 8558.5, 8194.5,
         7728.1, 7222.4, 6520.7, 5584.2, 4399.8, 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0.]
    )
    assert np.max(np.abs(lift_array - lift_result)) <= 1e-1
