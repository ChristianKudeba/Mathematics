# Build with MSVC (requires a VS 2022 Developer Command Prompt)
# Or with MinGW/GCC if available on PATH.
#
# MSVC (from VS Developer Command Prompt):
#   nmake
#
# GCC / MinGW:
#   make CC=gcc

# ---- MSVC target (nmake) ----------------------------------------
CC     = cl
CFLAGS = /O2 /W3 /D_CRT_SECURE_NO_WARNINGS
LFLAGS = /link /SUBSYSTEM:WINDOWS user32.lib gdi32.lib comdlg32.lib
TARGET = proof_viz.exe

$(TARGET): main.c
	$(CC) $(CFLAGS) main.c $(LFLAGS) /OUT:$(TARGET)

clean:
	del /Q $(TARGET) main.obj 2>nul

# ---- GCC / MinGW target (make) ----------------------------------
.PHONY: gcc clean
gcc:
	gcc -Wall -O2 -mwindows -o $(TARGET) main.c -lcomdlg32 -lgdi32 -luser32 -lm
