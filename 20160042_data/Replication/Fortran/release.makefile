# ===== release.makefile (Windows + gfortran) =====
# 사용 예시:
#   make -f release.makefile clean
#   make -f release.makefile
#   make -f release.makefile OUT=kmv FC="C:/Strawberry/c/bin/gfortran.exe"

# 0) 출력 실행파일명 (기본값)
OUT      ?= kmv
PROG     := $(OUT)

# 1) 컴파일러/플래그 (원하면 make 호출 시 FC/FFLAGS 덮어쓰기 가능)
# 1) 컴파일러/플래그
FC       = C:/msys64/mingw64/bin/gfortran.exe
# 디버그용으로 최적화 낮추고 더 관대한 설정 (탭 경고 억제)
FFLAGS   = -m64 -O0 -g -fopenmp -fbacktrace -Wall -ffree-line-length-none -Wno-line-truncation -Wno-tabs -std=legacy -fcheck=bounds -fcheck=mem

# 2) SuiteSparse / OpenBLAS 경로 (MSYS2 기본 경로 기준)
INCDIRS  ?= -IC:/msys64/mingw64/include -IC:/msys64/mingw64/include/suitesparse
LIBDIRS  ?= -LC:/msys64/mingw64/lib

# 3) 링크 옵션
#   UMFPACK는 AMD/CCOLAMD/COLAMD/CAMD 및 SuiteSparse_config, BLAS 필요
#   OpenBLAS 사용. 필요 시 -lstdc++ (C++ 심볼) 또는 -lmingwex(system_) 활성화
LIBS     ?= -lumfpack -lcholmod -lamd -lcolamd -lccolamd -lcamd -lsuitesparseconfig -lopenblas -lm -lmingwex
#LIBS    += -lstdc++
#LIBS    += -lmingwex

LDFLAGS  ?= $(LIBDIRS)

# 4) 오브젝트 목록
MOD = Parameters.o Globals.o umfpack.o Procedures.o compat_legacy.o

SUBR = AllocateArrays.o SetParameters.o Grids.o IterateBellman.o HJBUpdate.o \
       cumnor.o rtsec.o StationaryDistribution.o SaveSteadyStateOutput.o \
       DistributionStatistics.o rtbis.o rtflsp.o InitialSteadyState.o \
       FinalSteadyState.o SolveSteadyStateEqum.o Calibration.o \
       MomentConditions.o dfovec.o newuoa-h.o newuob-h.o update.o trsapp-h.o \
       biglag.o bigden.o mnbrak.o golden.o sort2.o CumulativeConsumption.o \
       FnDiscountRate.o OptimalConsumption.o FnHoursBC.o ImpulseResponses.o \
       IRFSequence.o Transition.o SaveIRFOutput.o IterateTransitionStickyRb.o \
       IterateTransOneAssetStickyRb.o FnCapitalEquity.o \
       CumulativeConsTransition.o DiscountedMPC.o DiscountedMPCTransition.o

OBJ = $(MOD) $(SUBR)

# 5) 빌드 규칙
all: $(PROG).exe

$(PROG).exe: $(OBJ) Main.o
	$(FC) $(FFLAGS) -o $@ $(OBJ) Main.o $(LDFLAGS) $(LIBS)

# 모듈 의존: Main은 모듈들 이후
Main.o: $(MOD)

$(PROG).out: $(OBJ) Main.o
	$(FC) $(FCFLAGS) -o $@ $^ $(LDFLAGS)

# 6) 컴파일 규칙 (이 부분이 누락되어 있었음!)
%.o: %.f90
	@echo "Compiling $<..."
	$(FC) $(FFLAGS) $(INCDIRS) -c $< -o $@

%.o: %.f95
	@echo "Compiling $<..."
	$(FC) $(FFLAGS) $(INCDIRS) -c $< -o $@

%.o: %.f
	@echo "Compiling $<..."
	$(FC) $(FFLAGS) $(INCDIRS) -c $< -o $@

%.o: %.for
	@echo "Compiling $<..."
	$(FC) $(FFLAGS) $(INCDIRS) -c $< -o $@

# 7) Windows clean
.PHONY: all clean
clean:
	- del /Q *.o *.obj *.mod *.MOD *genmod* *~ 2>nul
	- del /Q $(PROG).exe 2>nul