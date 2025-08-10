! compat_legacy.f90 : legacy intrinsics shims
double precision function dfloat(i)
  implicit none
  integer, intent(in) :: i
  dfloat = dble(i)
end function dfloat