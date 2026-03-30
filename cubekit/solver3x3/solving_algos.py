from enum import StrEnum
class Algo():
    class OLL:
        # https://jperm.net/algs/2look/oll - refrence used
        class Edges(StrEnum):
            dot_shape = "F R U R' U' F' f R U R' U' f'"
            I_shape = "F R U R' U' F'"
            L_shape = "f R U R' U' f'"
        class Corners(StrEnum):
            Antisune = "R U2 R' U' R U' R'"
            Sune = "R U R' U R U2 R'"
            H = "R U R' U R U' R' U R U2 R'"
            U = "R2 D R' U2 R D' R' U2 R'"
            Pi = "R U2 R2 U' R2 U' R2 U2 R"
            L = "F R' F' r U R U' r'"
            T = "r U R' U' r' F R F'"
    class PLL:
        class Corners(StrEnum):
            none_correct = "F R U' R' U' R U R' F' R U R' U' R' F R F'"
            one_pair_correct = "R' F R' B2 R F' R' B2 R2"
        class Edges(StrEnum):
            one_shiftleft = "R2 U R U R' U' R' U' R' U R'"
            one_shiftright = "R U' R U R U R U' R' U' R2"
            none_shiftback = "M2 U M2 U2 M2 U M2"
            none_shiftleft = one_shiftleft + ' U ' + one_shiftleft + " U'"#"M' U M2 U M2 U M' U2 M2"
