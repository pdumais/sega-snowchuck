SECTIONS
{
    . = 0x000000;

    .text :
    {
        *(.text)
    }

    . = ALIGN(2);
    .sound 0x3000: AT(0x3000)
    {
        *(.sound)
    }

    . = ALIGN(2);
    .rodata :
    {
        *(.rodata)
    }

    . = ALIGN(2);
    __rom_end = .;
    
    .data 0x00FF3000: AT(__rom_end)
    {
        __data_start = .;
        *(.data)
        __data_end = .;
    }
    __data_load = LOADADDR(.data);
    . = ALIGN(2);
    .bss 0xFF0000 (NOLOAD):
    {
        __bss_start = .;
        *(.bss)
        *(COMMON)
        __bss_end = .;
    }
}
