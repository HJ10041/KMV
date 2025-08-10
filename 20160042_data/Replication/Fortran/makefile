release:
    make -f release.makefile

debug:
    make -f debug.makefile
    dsymutil $(OUT).out

hpcrelease:
    make -f hpcrelease.makefile

pbs:
    make -f pbs.makefile

compilesubmit:
    make -f hpcrelease.makefile
    make -f pbs.makefile
    qsub $(OUT).pbs

.PHONY: clean

clean:
    del *.o, *.mod, *.MOD, *genmod*, *~ -ErrorAction SilentlyContinue
    del /s /q *.dSYM 2>nul