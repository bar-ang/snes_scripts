# Default target
TARGET := test

# Tools
AS := ca65
LD := ld65

# Flags
ASFLAGS := --cpu 65816
LDFLAGS := -C memmap.cfg

# Directories
BUILDDIR := build

# Files
SRCS := $(wildcard *.asm)
OBJ := $(BUILDDIR)/$(TARGET).o
OUT := $(BUILDDIR)/$(TARGET).smc

# Default rule
all: $(OUT)

# Ensure build directory exists
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# Assemble (main file only, but depend on ALL asm files)
$(OBJ): $(SRCS) | $(BUILDDIR)
	$(AS) $(ASFLAGS) -o $@ $(TARGET).asm

# Link
$(OUT): $(OBJ)
	$(LD) $(LDFLAGS) $< -o $@

# Clean
clean:
	rm -rf $(BUILDDIR)
