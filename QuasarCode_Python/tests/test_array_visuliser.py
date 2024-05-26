import numpy as np

from QuasarCode.Tools import ArrayVisuliser

class Test_ArrayVisuliser(object):
    def test_standard(self):
        assert ArrayVisuliser(np.array([1, 2, 3, 4, 5])).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#
|    N    :         : 5 |
|    ∞    :   0.00% : 0 |
|   +ve   : 100.00% : 5 |
|    0    :   0.00% : 0 |
|   -ve   :   0.00% : 0 |
|   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 |
|         :         :   |
|max   ≠ ∞:       5.000 |
|small ≠ 0:       1.000 |
|min   ≠-∞:       1.000 |
|         :         :   |
#-----------------------#"""

        assert ArrayVisuliser([np.array([1, 2, 3, 4, 5]), np.array([-1, -2, -3, -4, -5])]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#-------- (#1) ---------#
|    N    :         : 5 ¦    N    :         : 5 |
|    ∞    :   0.00% : 0 ¦    ∞    :   0.00% : 0 |
|   +ve   : 100.00% : 5 ¦   +ve   :   0.00% : 0 |
|    0    :   0.00% : 0 ¦    0    :   0.00% : 0 |
|   -ve   :   0.00% : 0 ¦   -ve   : 100.00% : 5 |
|   -∞    :   0.00% : 0 ¦   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 ¦   nan   :   0.00% : 0 |
|         :         :   ¦         :         :   |
|max   ≠ ∞:       5.000 ¦max   ≠ ∞:      -1.000 |
|small ≠ 0:       1.000 ¦small ≠ 0:      -1.000 |
|min   ≠-∞:       1.000 ¦min   ≠-∞:      -5.000 |
|         :         :   ¦         :         :   |
#-----------------------#-----------------------#"""

        assert ArrayVisuliser([np.array([1, 2, 3, 4, 5]), np.array([-1, -2, -3, -4, -5])]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = True, show_plus_minus_e = True, show_min_max = False
        ) == """\
#-------- (#0) ---------#-------- (#1) ---------#
|    N    :         : 5 ¦    N    :         : 5 |
|    ∞    :   0.00% : 0 ¦    ∞    :   0.00% : 0 |
|   +ve   : 100.00% : 5 ¦   +ve   :   0.00% : 0 |
|    0    :   0.00% : 0 ¦    0    :   0.00% : 0 |
|   -ve   :   0.00% : 0 ¦   -ve   : 100.00% : 5 |
|   -∞    :   0.00% : 0 ¦   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 ¦   nan   :   0.00% : 0 |
|         :         :   ¦         :         :   |
| +1≥x> 0 :  20.00% : 1 ¦ +1≥x> 0 :   0.00% : 0 |
|  0>x≥-1 :   0.00% : 0 ¦  0>x≥-1 :  20.00% : 1 |
|         :         :   ¦         :         :   |
| +e≥x> 0 :  40.00% : 2 ¦ +e≥x> 0 :   0.00% : 0 |
|  0>x≥-e :   0.00% : 0 ¦  0>x≥-e :  40.00% : 2 |
|         :         :   ¦         :         :   |
#-----------------------#-----------------------#"""

        assert ArrayVisuliser.column(np.array([1, 2, 3, 4, 5]), np.array([-1, -2, -3, -4, -5])).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#
|    N    :         : 5 |
|    ∞    :   0.00% : 0 |
|   +ve   : 100.00% : 5 |
|    0    :   0.00% : 0 |
|   -ve   :   0.00% : 0 |
|   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 |
|         :         :   |
|max   ≠ ∞:       5.000 |
|small ≠ 0:       1.000 |
|min   ≠-∞:       1.000 |
|         :         :   |
#,,,,,,,, (#1) ,,,,,,,,,#
|    N    :         : 5 |
|    ∞    :   0.00% : 0 |
|   +ve   :   0.00% : 0 |
|    0    :   0.00% : 0 |
|   -ve   : 100.00% : 5 |
|   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 |
|         :         :   |
|max   ≠ ∞:      -1.000 |
|small ≠ 0:      -1.000 |
|min   ≠-∞:      -5.000 |
|         :         :   |
#-----------------------#"""

        assert ArrayVisuliser.arrange(2, [np.array([1, 2, 3, 4, 5]), np.array([-1, -2, -3, -4, -5])]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#-------- (#1) ---------#
|    N    :         : 5 ¦    N    :         : 5 |
|    ∞    :   0.00% : 0 ¦    ∞    :   0.00% : 0 |
|   +ve   : 100.00% : 5 ¦   +ve   :   0.00% : 0 |
|    0    :   0.00% : 0 ¦    0    :   0.00% : 0 |
|   -ve   :   0.00% : 0 ¦   -ve   : 100.00% : 5 |
|   -∞    :   0.00% : 0 ¦   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 ¦   nan   :   0.00% : 0 |
|         :         :   ¦         :         :   |
|max   ≠ ∞:       5.000 ¦max   ≠ ∞:      -1.000 |
|small ≠ 0:       1.000 ¦small ≠ 0:      -1.000 |
|min   ≠-∞:       1.000 ¦min   ≠-∞:      -5.000 |
|         :         :   ¦         :         :   |
#-----------------------#-----------------------#"""

        assert ArrayVisuliser.arrange(1, [np.array([1, 2, 3, 4, 5]), np.array([-1, -2, -3, -4, -5])]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#
|    N    :         : 5 |
|    ∞    :   0.00% : 0 |
|   +ve   : 100.00% : 5 |
|    0    :   0.00% : 0 |
|   -ve   :   0.00% : 0 |
|   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 |
|         :         :   |
|max   ≠ ∞:       5.000 |
|small ≠ 0:       1.000 |
|min   ≠-∞:       1.000 |
|         :         :   |
#,,,,,,,, (#1) ,,,,,,,,,#
|    N    :         : 5 |
|    ∞    :   0.00% : 0 |
|   +ve   :   0.00% : 0 |
|    0    :   0.00% : 0 |
|   -ve   : 100.00% : 5 |
|   -∞    :   0.00% : 0 |
|   nan   :   0.00% : 0 |
|         :         :   |
|max   ≠ ∞:      -1.000 |
|small ≠ 0:      -1.000 |
|min   ≠-∞:      -5.000 |
|         :         :   |
#-----------------------#"""

        assert ArrayVisuliser.arrange(3, [np.array([1, 2, 3, 4, 5]), np.array([-1, -2, -3, -4, -5])]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#-------- (#1) ---------#                        
|    N    :         : 5 ¦    N    :         : 5 |                        
|    ∞    :   0.00% : 0 ¦    ∞    :   0.00% : 0 |                        
|   +ve   : 100.00% : 5 ¦   +ve   :   0.00% : 0 |                        
|    0    :   0.00% : 0 ¦    0    :   0.00% : 0 |                        
|   -ve   :   0.00% : 0 ¦   -ve   : 100.00% : 5 |                        
|   -∞    :   0.00% : 0 ¦   -∞    :   0.00% : 0 |                        
|   nan   :   0.00% : 0 ¦   nan   :   0.00% : 0 |                        
|         :         :   ¦         :         :   |                        
|max   ≠ ∞:       5.000 ¦max   ≠ ∞:      -1.000 |                        
|small ≠ 0:       1.000 ¦small ≠ 0:      -1.000 |                        
|min   ≠-∞:       1.000 ¦min   ≠-∞:      -5.000 |                        
|         :         :   ¦         :         :   |                        
#-----------------------#-----------------------#                        """

        assert ArrayVisuliser([[np.array([1, 2, 3, 4, 5]), None], [None, np.array([-1, -2, -3, -4, -5])]]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#                        
|    N    :         : 5 |                        
|    ∞    :   0.00% : 0 |                        
|   +ve   : 100.00% : 5 |                        
|    0    :   0.00% : 0 |                        
|   -ve   :   0.00% : 0 |                        
|   -∞    :   0.00% : 0 |                        
|   nan   :   0.00% : 0 |                        
|         :         :   |                        
|max   ≠ ∞:       5.000 |                        
|small ≠ 0:       1.000 |                        
|min   ≠-∞:       1.000 |                        
|         :         :   |                        
#-----------------------#-------- (#3) ---------#
                        |    N    :         : 5 |
                        |    ∞    :   0.00% : 0 |
                        |   +ve   :   0.00% : 0 |
                        |    0    :   0.00% : 0 |
                        |   -ve   : 100.00% : 5 |
                        |   -∞    :   0.00% : 0 |
                        |   nan   :   0.00% : 0 |
                        |         :         :   |
                        |max   ≠ ∞:      -1.000 |
                        |small ≠ 0:      -1.000 |
                        |min   ≠-∞:      -5.000 |
                        |         :         :   |
                        #-----------------------#"""

        assert ArrayVisuliser([[np.array([1, 2, 3, 4, 5]), None, None], [None, None, None], [None, None, np.array([-1, -2, -3, -4, -5])]]).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#-------- (#0) ---------#                                                
|    N    :         : 5 |                                                
|    ∞    :   0.00% : 0 |                                                
|   +ve   : 100.00% : 5 |                                                
|    0    :   0.00% : 0 |                                                
|   -ve   :   0.00% : 0 |                                                
|   -∞    :   0.00% : 0 |                                                
|   nan   :   0.00% : 0 |                                                
|         :         :   |                                                
|max   ≠ ∞:       5.000 |                                                
|small ≠ 0:       1.000 |                                                
|min   ≠-∞:       1.000 |                                                
|         :         :   |                                                
#-----------------------#                                                
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                                         
                                                #-------- (#8) ---------#
                                                |    N    :         : 5 |
                                                |    ∞    :   0.00% : 0 |
                                                |   +ve   :   0.00% : 0 |
                                                |    0    :   0.00% : 0 |
                                                |   -ve   : 100.00% : 5 |
                                                |   -∞    :   0.00% : 0 |
                                                |   nan   :   0.00% : 0 |
                                                |         :         :   |
                                                |max   ≠ ∞:      -1.000 |
                                                |small ≠ 0:      -1.000 |
                                                |min   ≠-∞:      -5.000 |
                                                |         :         :   |
                                                #-----------------------#"""

        assert ArrayVisuliser(np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])).render(
            all_columns_same_width = False, min_count_allowence = 0, show_plus_minus_1 = False, show_plus_minus_e = False, show_min_max = True
        ) == """\
#------------ (#0) -------------#
|    N    :         : 10 (2, 5) |
|    ∞    :   0.00% :  0 (0, 0) |
|   +ve   : 100.00% : 10 (2, 5) |
|    0    :   0.00% :  0 (0, 0) |
|   -ve   :   0.00% :  0 (0, 0) |
|   -∞    :   0.00% :  0 (0, 0) |
|   nan   :   0.00% :  0 (0, 0) |
|         :         :           |
|max   ≠ ∞:              10.000 |
|small ≠ 0:               1.000 |
|min   ≠-∞:               1.000 |
|         :         :           |
#-------------------------------#"""

        assert str(ArrayVisuliser(np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))) == "(#0) | 10 (2, 5)"
