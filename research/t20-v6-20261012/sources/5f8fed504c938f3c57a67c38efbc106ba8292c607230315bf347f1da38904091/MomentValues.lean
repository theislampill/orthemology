import Certificate

namespace TruncatedMoment

theorem moment_000 : Lambda (term 0 0 0 1) = 1 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_001 : Lambda (term 0 0 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_010 : Lambda (term 0 1 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_100 : Lambda (term 1 0 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_002 : Lambda (term 0 0 2 1) = 4 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_011 : Lambda (term 0 1 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_020 : Lambda (term 0 2 0 1) = 4 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_101 : Lambda (term 1 0 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_110 : Lambda (term 1 1 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_200 : Lambda (term 2 0 0 1) = 4 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_003 : Lambda (term 0 0 3 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_012 : Lambda (term 0 1 2 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_021 : Lambda (term 0 2 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_030 : Lambda (term 0 3 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_102 : Lambda (term 1 0 2 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_111 : Lambda (term 1 1 1 1) = (3/2 : ℝ) := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_120 : Lambda (term 1 2 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_201 : Lambda (term 2 0 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_210 : Lambda (term 2 1 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_300 : Lambda (term 3 0 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_004 : Lambda (term 0 0 4 1) = 50 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_013 : Lambda (term 0 1 3 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_022 : Lambda (term 0 2 2 1) = 1 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_031 : Lambda (term 0 3 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_040 : Lambda (term 0 4 0 1) = 50 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_103 : Lambda (term 1 0 3 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_112 : Lambda (term 1 1 2 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_121 : Lambda (term 1 2 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_130 : Lambda (term 1 3 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_202 : Lambda (term 2 0 2 1) = 1 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_211 : Lambda (term 2 1 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_220 : Lambda (term 2 2 0 1) = 1 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_301 : Lambda (term 3 0 1 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_310 : Lambda (term 3 1 0 1) = 0 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

theorem moment_400 : Lambda (term 4 0 0 1) = 50 := by
  norm_num [Lambda, term, MvPolynomial.coeff_monomial, exponent_eq_iff]

end TruncatedMoment
