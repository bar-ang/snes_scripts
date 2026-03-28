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
SRC := $(TARGET).asm
OBJ := $(BUILDDIR)/$(TARGET).o
OUT := $(BUILDDIR)/$(TARGET).smc

# Default rule
all: $(OUT)

# Ensure build directory exists
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# Assemble
$(OBJ): $(SRC) | $(BUILDDIR)
	$(AS) $(ASFLAGS) -o $@ $<

# Link
$(OUT): $(OBJ)
	$(LD) $(LDFLAGS) $< -o $@

# Clean
clean:
	rm -rf $(BUILDDIR)
