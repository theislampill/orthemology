"""Exact-real Gaussian W→FR formulas evaluated in NumPy floating point.

This is the classical split attributed in RESULT.md, applied to one conditional
fibre. It does not sample an exact Gaussian, represent a general conditional
kernel, or certify floating-point errors. Strict input checks may reject a
mathematically semidefinite matrix whose computed eigenvalue rounds negative.
"""
from numbers import Real
import numpy as np


def gaussian_step(mean, covariance, target_mean, target_covariance, h):
    """Return Gaussian parameters after OU then centred reaction, each time h.

    Shapes: mean and target_mean (d,); covariances (d,d). Inputs must be finite,
    exactly symmetric in their array representation, target covariance positive
    definite, input covariance positive semidefinite, and 0<h<infinity.
    Floating-point failures at ill-conditioned/extreme inputs raise rather than
    supply a falsely certified law. No input array is changed.
    """
    if any(np.iscomplexobj(x) for x in
           (mean, covariance, target_mean, target_covariance)):
        raise ValueError('Gaussian parameters must be real, not complex arrays')
    if not isinstance(h, Real) or not np.isfinite(h) or h <= 0:
        raise ValueError('h must be a finite positive real scalar')
    mean = np.asarray(mean, dtype=float)
    target_mean = np.asarray(target_mean, dtype=float)
    covariance = np.asarray(covariance, dtype=float)
    target_covariance = np.asarray(target_covariance, dtype=float)
    if mean.ndim != 1 or mean.size == 0 or target_mean.shape != mean.shape:
        raise ValueError('mean vectors must have the same nonempty shape')
    d = mean.size
    if covariance.shape != (d, d) or target_covariance.shape != (d, d):
        raise ValueError('covariance shapes must match the mean dimension')
    if not all(np.all(np.isfinite(x)) for x in
               (mean, target_mean, covariance, target_covariance)):
        raise ValueError('parameters must be finite')
    for name, mat in [('covariance', covariance), ('target_covariance', target_covariance)]:
        if not np.array_equal(mat, mat.T):
            raise ValueError(name + ' must be symmetric in its supplied array representation')
    eig_t, vec_t = np.linalg.eigh(target_covariance)
    if np.min(eig_t) <= 0:
        raise ValueError('target covariance must be positive definite')
    if np.min(np.linalg.eigvalsh(covariance)) < 0:
        raise ValueError('input covariance must be positive semidefinite')
    a_eigs = np.exp(-h / eig_t)
    # expm1 avoids cancellation of I-exp(-2h T^-1) for small positive h.
    q_eigs = eig_t * (-np.expm1(-2*h / eig_t))
    A = (vec_t * a_eigs) @ vec_t.T
    Q = (vec_t * q_eigs) @ vec_t.T
    diffusion_mean = target_mean + A @ (mean-target_mean)
    diffusion_covariance = A @ covariance @ A + Q
    diffusion_covariance = (diffusion_covariance + diffusion_covariance.T)/2
    np.linalg.cholesky(diffusion_covariance)
    a = np.exp(-h)
    identity = np.eye(d)
    inv_s = np.linalg.solve(diffusion_covariance, identity)
    inv_t = np.linalg.solve(target_covariance, identity)
    precision = a*inv_s + (-np.expm1(-h))*inv_t
    precision = (precision+precision.T)/2
    np.linalg.cholesky(precision)
    output_covariance = np.linalg.solve(precision, identity)
    output_covariance = (output_covariance+output_covariance.T)/2
    output_mean = target_mean + np.linalg.solve(
        precision, a*np.linalg.solve(diffusion_covariance,
                                    diffusion_mean-target_mean))
    if not np.all(np.isfinite(output_covariance)) or not np.all(np.isfinite(output_mean)):
        raise ArithmeticError('nonfinite floating-point output')
    np.linalg.cholesky(output_covariance)
    return dict(mean=output_mean, covariance=output_covariance,
                diffusion_mean=diffusion_mean,
                diffusion_covariance=diffusion_covariance,
                reaction_exponent=float(a), diffusion_matrix=A,
                diffusion_noise_covariance=Q)
