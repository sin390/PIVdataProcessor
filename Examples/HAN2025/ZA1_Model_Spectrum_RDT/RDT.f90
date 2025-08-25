! rdt_axsym.f90    Fortran 90 translation of G01_modelspectrumRDT.py
MODULE rdt_kinds
  IMPLICIT NONE
  INTEGER, PARAMETER :: dp = SELECTED_REAL_KIND(15, 300)
  REAL(dp), PARAMETER :: pi = 3.1415926535897932384626433832795_dp
END MODULE rdt_kinds

MODULE util_arrays
  USE rdt_kinds
  IMPLICIT NONE
CONTAINS
  SUBROUTINE linspace(a, b, n, x)
    REAL(dp), INTENT(IN)  :: a, b
    INTEGER, INTENT(IN)   :: n
    REAL(dp), INTENT(OUT) :: x(n)
    INTEGER :: i
    IF (n == 1) THEN
      x(1) = a
    ELSE
      DO i = 1, n
        x(i) = a + (b - a) * REAL(i - 1, dp) / REAL(n - 1, dp)
      END DO
    END IF
  END SUBROUTINE linspace
END MODULE util_arrays

MODULE rdt_types
  USE rdt_kinds
  IMPLICIT NONE
  TYPE :: k_range
    REAL(dp) :: kmin = 0.0_dp
    REAL(dp) :: kmax = 0.0_dp
    INTEGER  :: points = 0
    REAL(dp) :: dk = 0.0_dp
    REAL(dp) :: L = 0.0_dp
    REAL(dp) :: Re_lambda = 0.0_dp
  CONTAINS
    PROCEDURE :: recommend_value
  END TYPE k_range
CONTAINS
  SUBROUTINE recommend_value(this, L_in, Re_lam_in)
    CLASS(k_range), INTENT(INOUT) :: this
    REAL(dp), INTENT(IN)          :: L_in, Re_lam_in
    REAL(dp) :: domain, eta
    this%L = L_in
    this%Re_lambda = Re_lam_in
    domain = 10.0_dp * L_in
    this%kmin = 2.0_dp * pi / domain
    eta = (15.0_dp**(3.0_dp/4.0_dp)) * (Re_lam_in**(-1.5_dp)) * L_in
    this%kmax = 2.0_dp * pi / eta
    this%points = MAX(2, INT(domain / eta))
    this%dk = (this%kmax - this%kmin) / REAL(this%points - 1, dp)
  END SUBROUTINE recommend_value
END MODULE rdt_types

MODULE spectra_models
  USE rdt_kinds
  IMPLICIT NONE
  TYPE :: PopeParams
    REAL(dp) :: L, eta, epsilon, C, CL, p0, Ceta, beta
  END TYPE PopeParams
  TYPE :: PaoParams
    REAL(dp) :: L, eta, epsilon, m, alpha
  END TYPE PaoParams
CONTAINS
  PURE FUNCTION pope_spectrum(k, p) RESULT(Ek)
    REAL(dp), INTENT(IN) :: k
    TYPE(PopeParams), INTENT(IN) :: p
    REAL(dp) :: Ek, fL, feta
    fL  = ((k*p%L) / SQRT((k*p%L)**2 + p%CL))**(5.0_dp/3.0_dp + p%p0)
    feta = EXP(-p%beta * ((k*p%eta)**4 + p%Ceta**4)**0.25_dp - p%Ceta)
    Ek = p%C * (p%epsilon**(2.0_dp/3.0_dp)) * k**(-5.0_dp/3.0_dp) * fL * feta
  END FUNCTION pope_spectrum

  PURE FUNCTION pao_spectrum(k, p) RESULT(Ek)
    REAL(dp), INTENT(IN) :: k
    TYPE(PaoParams), INTENT(IN) :: p
    REAL(dp) :: Ek, fL, feta
    fL  = (1.0_dp + (3.0_dp*p%alpha/2.0_dp) * (k*p%L)**(-2.0_dp/3.0_dp))**(p%m)
    feta = EXP(-(3.0_dp*p%alpha/2.0_dp) * (p%eta*k)**(4.0_dp/3.0_dp))
    Ek = p%alpha * (p%epsilon**(2.0_dp/3.0_dp)) * k**(-5.0_dp/3.0_dp) / fL * feta
  END FUNCTION pao_spectrum
END MODULE spectra_models

MODULE rdt_ops
  USE rdt_kinds
  USE rdt_types
  USE util_arrays
  USE spectra_models
  IMPLICIT NONE
CONTAINS
  FUNCTION cal_energy(k_long, E) RESULT(energy)
    REAL(dp), INTENT(IN) :: k_long(:), E(:)
    REAL(dp) :: energy, dk
    dk = k_long(2) - k_long(1)
    energy = SUM(E) * dk
  END FUNCTION cal_energy

  FUNCTION cal_integral_scale(k_long, E) RESULT(Lint)
    REAL(dp), INTENT(IN) :: k_long(:), E(:)
    REAL(dp) :: Lint, dk
    REAL(dp), ALLOCATABLE :: tmp(:)
    dk = k_long(2) - k_long(1)
    ALLOCATE(tmp(SIZE(E)))
    tmp = (E / k_long) * dk
    Lint = (pi/2.0_dp) * SUM(tmp) / cal_energy(k_long, E)
    DEALLOCATE(tmp)
  END FUNCTION cal_integral_scale

SUBROUTINE cal_origin(E11k1, k_long_r, k_trans_r, use_pope, pope, pao)
  REAL(dp), INTENT(OUT) :: E11k1(:)
  TYPE(k_range), INTENT(IN) :: k_long_r, k_trans_r
  LOGICAL, INTENT(IN) :: use_pope
  TYPE(PopeParams), INTENT(IN) :: pope
  TYPE(PaoParams),  INTENT(IN) :: pao
  INTEGER :: i, j, l
  REAL(dp), ALLOCATABLE :: k1(:), k2(:), k3(:)
  REAL(dp) :: sumv, ksq, kimg, term

  ALLOCATE(k1(k_long_r%points))
  ALLOCATE(k2(k_trans_r%points))
  ALLOCATE(k3(k_trans_r%points))

  CALL linspace(k_long_r%kmin,  k_long_r%kmax,  k_long_r%points,  k1)
  CALL linspace(k_trans_r%kmin, k_trans_r%kmax, k_trans_r%points, k2)
  k3 = k2

  DO i = 1, k_long_r%points
    sumv = 0.0_dp
    DO j = 1, k_trans_r%points
      DO l = 1, k_trans_r%points
        ksq = k1(i)**2 + k2(j)**2 + k3(l)**2
        IF (ksq <= 0.0_dp) CYCLE
        kimg = SQRT(ksq)
        IF (use_pope) THEN
          term = pope_spectrum(kimg, pope)
        ELSE
          term = pao_spectrum(kimg, pao)
        END IF
        term = term * ((k2(j)**2 + k3(l)**2) / (pi * ksq**2)) * (k_trans_r%dk**2)
        sumv = sumv + term
      END DO
    END DO
    E11k1(i) = sumv
  END DO

  DEALLOCATE(k1, k2, k3)
END SUBROUTINE cal_origin

SUBROUTINE cal_origin_polar(E11k1, k_long_r, k_trans_r, use_pope, pope, pao)
  USE rdt_kinds; USE spectra_models; USE rdt_types
  IMPLICIT NONE
  REAL(dp), INTENT(OUT) :: E11k1(:)
  TYPE(k_range), INTENT(IN) :: k_long_r, k_trans_r
  LOGICAL, INTENT(IN) :: use_pope
  TYPE(PopeParams), INTENT(IN) :: pope
  TYPE(PaoParams),  INTENT(IN) :: pao
  INTEGER :: i, m, nlong, nrad
  REAL(dp) :: dk, dr, k1, r, r2, ksq, kimg, term
  REAL(dp) :: sumv
  REAL(dp), ALLOCATABLE :: k1g(:)

  ! 长度方向点数
  nlong = k_long_r%points
  dk = k_long_r%dk
  dr = k_trans_r%dk
  nrad = k_trans_r%points          ! 极径方向点数
  ALLOCATE(k1g(nlong))
  CALL linspace(k_long_r%kmin, k_long_r%kmax, nlong, k1g)

  DO i = 1, nlong
    k1   = k1g(i)
    sumv = 0.0_dp

!$omp parallel do reduction(+:sumv) schedule(static)
    DO m = 1, nrad
      r  = dr * REAL(m, dp)
      r2 = r*r
      ksq = k1*k1 + r2
      kimg = SQRT(ksq)

      IF (use_pope) THEN
        term = pope_spectrum(kimg, pope)
      ELSE
        term = pao_spectrum(kimg, pao)
      END IF

      ! E11 integrand in polar coordinates: (r^2 / (pi * ksq^2)) * (2*pi*r*dr) = 2*r^3*dr / ksq^2
      term = term / 2.0_dp/ pi /ksq**2.0_dp
      term = term *r*r
      term = term * 2.0_dp * pi * r *dr
      sumv = sumv + term
    END DO
!$omp end parallel do

    E11k1(i) = sumv
  END DO

  DEALLOCATE(k1g)
END SUBROUTINE cal_origin_polar

SUBROUTINE cal_RDT_E11k1_polar(E11k1, k_long_r, k_trans_r, c, use_pope, pope, pao)
  USE rdt_kinds; USE spectra_models; USE rdt_types
  IMPLICIT NONE
  REAL(dp), INTENT(OUT) :: E11k1(:)
  TYPE(k_range), INTENT(IN) :: k_long_r, k_trans_r
  REAL(dp), INTENT(IN) :: c
  LOGICAL, INTENT(IN) :: use_pope
  TYPE(PopeParams), INTENT(IN) :: pope
  TYPE(PaoParams),  INTENT(IN) :: pao
  INTEGER :: i, m, nlong, nrad
  REAL(dp) :: dk, dr, k1, k1i, r, r2, ksq, ksq_img, kimg, term, coeff
  REAL(dp) :: sumv
  REAL(dp), ALLOCATABLE :: k1g(:)

  nlong = k_long_r%points
  dk = k_long_r%dk
  dr = k_trans_r%dk
  nrad = k_trans_r%points         ! r �̍ő�͌��� k2/k3 �͈͂ɍ��킹��
  ALLOCATE(k1g(nlong))
  CALL linspace(k_long_r%kmin, k_long_r%kmax, nlong, k1g)

  coeff = 2.0_dp*pi               ! �p�x�ϕ�

  DO i = 1, nlong
    k1   = k1g(i)
    k1i  = c*k1                    ! �摜��Ԃ� k1
    sumv = 0.0_dp

!$omp parallel do reduction(+:sumv) schedule(static)
    DO m = 1, nrad
      r  = dr*REAL(m,dp)
      r2 = r*r
      ksq     = k1*k1 + r2
      ksq_img = k1i*k1i + (r*r)/c   ! img_k2^2+img_k3^2 = (r^2)/c
      kimg    = SQRT(ksq_img)

      IF (use_pope) THEN
        term = pope_spectrum(kimg, pope)
      ELSE
        term = pao_spectrum(kimg, pao)
      END IF

      ! E11 integrand: ((img_k2^2+img_k3^2)/(��*ksq^2)) * (2�� r dr)
      ! = ( (r^2/c) / (��*ksq^2) ) * (2�� r dr) = (2*r^3/(c*ksq^2)) * dr
      term = term / 2.0_dp/ pi /ksq**2.0_dp
      term = term *(r*r)/c
      term = term * 2.0_dp * pi * r *dr
      sumv = sumv + term
    END DO
!$omp end parallel do

    E11k1(i) = sumv
  END DO

  DEALLOCATE(k1g)
END SUBROUTINE cal_RDT_E11k1_polar


SUBROUTINE cal_RDT_E11k1(E11k1, k_long_r, k_trans_r, c, use_pope, pope, pao)
  REAL(dp), INTENT(OUT) :: E11k1(:)
  TYPE(k_range), INTENT(IN) :: k_long_r, k_trans_r
  REAL(dp), INTENT(IN) :: c
  LOGICAL, INTENT(IN) :: use_pope
  TYPE(PopeParams), INTENT(IN) :: pope
  TYPE(PaoParams),  INTENT(IN) :: pao
  INTEGER :: i, j, l
  REAL(dp), ALLOCATABLE :: k1(:), k2(:), k3(:)
  REAL(dp), ALLOCATABLE :: img_k1(:), img_k2(:), img_k3(:)
  REAL(dp) :: sumv, ksq, ksq_img, kimg, term

  ALLOCATE(k1(k_long_r%points))
  ALLOCATE(k2(k_trans_r%points))
  ALLOCATE(k3(k_trans_r%points))
  CALL linspace(k_long_r%kmin,  k_long_r%kmax,  k_long_r%points,  k1)
  CALL linspace(k_trans_r%kmin, k_trans_r%kmax, k_trans_r%points, k2)
  k3 = k2

  ALLOCATE(img_k1(k_long_r%points), img_k2(k_trans_r%points), img_k3(k_trans_r%points))
  img_k1 = c * k1
  img_k2 = k2 / SQRT(c)
  img_k3 = k3 / SQRT(c)

  DO i = 1, k_long_r%points
    sumv = 0.0_dp
    DO j = 1, k_trans_r%points
      DO l = 1, k_trans_r%points
        ksq     = k1(i)**2 + k2(j)**2 + k3(l)**2
        ksq_img = img_k1(i)**2 + img_k2(j)**2 + img_k3(l)**2
        IF (ksq <= 0.0_dp) CYCLE
        kimg = SQRT(ksq_img)
        IF (use_pope) THEN
          term = pope_spectrum(kimg, pope)
        ELSE
          term = pao_spectrum(kimg, pao)
        END IF
        term = term * ((img_k2(j)**2 + img_k3(l)**2) / (pi * ksq**2)) * (k_trans_r%dk**2)
        sumv = sumv + term
      END DO
    END DO
    E11k1(i) = sumv
  END DO

  DEALLOCATE(k1, k2, k3, img_k1, img_k2, img_k3)
END SUBROUTINE cal_RDT_E11k1


SUBROUTINE cal_RDT_E22k2(E22k2, k_long_r, k_trans_r, c, use_pope, pope, pao)
  REAL(dp), INTENT(OUT) :: E22k2(:)
  TYPE(k_range), INTENT(IN) :: k_long_r, k_trans_r
  REAL(dp), INTENT(IN) :: c
  LOGICAL, INTENT(IN) :: use_pope
  TYPE(PopeParams), INTENT(IN) :: pope
  TYPE(PaoParams),  INTENT(IN) :: pao
  INTEGER :: i, j, l
  REAL(dp), ALLOCATABLE :: k1(:), k2(:), k3(:)
  REAL(dp), ALLOCATABLE :: img_k1(:), img_k2(:), img_k3(:)
  REAL(dp) :: sumv, ksq, ksq_img, kimg, term, t1

  ALLOCATE(k2(k_long_r%points))          ! longitudinal axis for E22(k2)
  ALLOCATE(k1(k_trans_r%points))
  ALLOCATE(k3(k_trans_r%points))

  CALL linspace(k_long_r%kmin,  k_long_r%kmax,  k_long_r%points,  k2)
  CALL linspace(k_trans_r%kmin, k_trans_r%kmax, k_trans_r%points,  k1)
  k3 = k1

  ALLOCATE(img_k1(k_trans_r%points), img_k2(k_long_r%points), img_k3(k_trans_r%points))
  img_k1 = c * k1
  img_k2 = k2 / SQRT(c)
  img_k3 = k3 / SQRT(c)

  DO i = 1, k_long_r%points
    sumv = 0.0_dp
    DO j = 1, k_trans_r%points
      DO l = 1, k_trans_r%points
        ksq     = k1(j)**2 + k2(i)**2 + k3(l)**2
        ksq_img = img_k1(j)**2 + img_k2(i)**2 + img_k3(l)**2
        IF (ksq <= 0.0_dp .OR. ksq_img <= 0.0_dp) CYCLE
        kimg = SQRT(ksq_img)
        IF (use_pope) THEN
          term = pope_spectrum(kimg, pope)
        ELSE
          term = pao_spectrum(kimg, pao)
        END IF
        t1 = c**(-3.0_dp)*img_k1(j)**2*(img_k1(j)**2 + img_k2(i)**2) + &
             c**( 3.0_dp)*img_k3(l)**2*(img_k2(i)**2 + img_k3(l)**2) + &
             2.0_dp*img_k1(j)**2*img_k3(l)**2
        term = term * ( t1 / (pi * ksq**2 * ksq_img) ) * (k_trans_r%dk**2)
        sumv = sumv + term
      END DO
    END DO
    E22k2(i) = sumv
  END DO

  DEALLOCATE(k1, k2, k3, img_k1, img_k2, img_k3)
END SUBROUTINE cal_RDT_E22k2
END MODULE rdt_ops

PROGRAM main
  USE rdt_kinds
  USE rdt_types
  USE spectra_models
  USE rdt_ops
  USE util_arrays
  IMPLICIT NONE

  TYPE(k_range) :: kr_long, kr_trans
  TYPE(PopeParams) :: pope
  TYPE(PaoParams)  :: pao
  REAL(dp), ALLOCATABLE :: k_long(:), E11(:), E22(:)
  REAL(dp) :: integral_L, Re_lambda, epsilon, c
  LOGICAL :: use_pope
  INTEGER :: i
  CHARACTER(LEN=*), PARAMETER :: f_ori = 'E11_origin.txt', f11 = 'E11k1_RDT.txt', f22 = 'E22k2_025.txt'

!!! ------- Calculation parameters -------
  c          = 0.25_dp

  integral_L = 2e-2_dp
  epsilon    = 4.5e4_dp
  Re_lambda  = 600.0_dp
!!! ------- Calculation parameters -------

  use_pope   = .TRUE.

  CALL kr_long%recommend_value(integral_L, Re_lambda)
  CALL kr_trans%recommend_value(integral_L, Re_lambda)
  ALLOCATE(k_long(kr_long%points), E11(kr_long%points), E22(kr_long%points))
  CALL linspace(kr_long%kmin, kr_long%kmax, kr_long%points, k_long)

  ! ------- set spectrum params -------
  pope%L = integral_L
  pope%eta = (15.0_dp**(3.0_dp/4.0_dp)) * (Re_lambda**(-1.5_dp)) * pope%L
  pope%epsilon = epsilon
  pope%C = 1.5_dp
  pope%CL = 6.78_dp
  pope%p0 = 2.0_dp
  pope%Ceta = 0.4_dp
  pope%beta = 5.2_dp


  pao%L = integral_L
  pao%eta = (15.0_dp**(3.0_dp/4.0_dp)) * (Re_lambda**(-1.5_dp)) * pao%L
  pao%epsilon = epsilon
  pao%m = 11.0_dp/2.0_dp
  pao%alpha = 1.52_dp

  ! ------- compute -------
  cALL cal_origin_polar(E11, kr_long, kr_trans, use_pope, pope, pao)
  OPEN(10, FILE=f_ori, STATUS='REPLACE', ACTION='WRITE', FORM='FORMATTED')
  DO i = 1, SIZE(E11)
    WRITE(10, '(ES22.12,1X,ES22.12)') k_long(i), E11(i)
  END DO
  CLOSE(10)
  
  CALL cal_RDT_E11k1_polar(E11, kr_long, kr_trans, c, use_pope, pope, pao)
!  CALL cal_RDT_E22k2(E22, kr_long, kr_trans, c, use_pope, pope, pao)

  ! ------- save to text -------
  OPEN(10, FILE=f11, STATUS='REPLACE', ACTION='WRITE', FORM='FORMATTED')
  DO i = 1, SIZE(E11)
    WRITE(10, '(ES22.12,1X,ES22.12)') k_long(i), E11(i)
  END DO
  CLOSE(10)

 ! OPEN(20, FILE=f22, STATUS='REPLACE', ACTION='WRITE', FORM='FORMATTED')
 ! DO i = 1, SIZE(E22)
 !   WRITE(20, '(ES22.12,1X,ES22.12)') k_long(i), E22(i)
 ! END DO
 ! CLOSE(20)

  ! (�C��) �G�l���M�[�E�ϕ��X�P�[����W���o�͂�
  WRITE(*,'(A,ES14.6)') 'Energy(E11): ', cal_energy(k_long, E11)
  WRITE(*,'(A,ES14.6)') 'Integral scale from E11: ', cal_integral_scale(k_long, E11)

END PROGRAM main
