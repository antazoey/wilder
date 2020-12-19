using System;

namespace Wilder.Common.Enum
{
    [Flags]
    public enum InsertFlags
    {
        ReversePolarity = 1,
        SwapChannels = 1 << 1,
        Unknown3 = 1 << 2,
        Unmute = 1 << 3,
        DisableThreaded = 1 << 4,
        Unknown6 = 1 << 5,
        DockedMiddle = 1 << 6,
        DockedRight = 1 << 7,
        Unknown9 = 1 << 8,
        Unknown10 = 1 << 9,
        Separator = 1 << 10,
        Lock = 1 << 11,
        Solo = 1 << 12,
        Unknown14 = 1 << 13,
        Unknown15 = 1 << 14,
        Unknown16 = 1 << 15
    }
}
