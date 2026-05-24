SECTIONS
{
    . = 0x000000;

    .text :
    {
        *(.text)
    }

    .bss (NOLOAD):
    {
        __bss_start = .;
        *(.bss)
        *(COMMON)
        __bss_end = .;
    }
}
