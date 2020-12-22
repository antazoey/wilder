using Wilder.Common.Enum;

namespace Wilder.Common.Model
{
    public class Insert
    {
        public const int MaxSlotCount = 10;

        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public uint Color { get; set; }
        public ushort Icon { get; set; }
        public InsertFlags Flags { get; set; } = 0;
        public int Volume { get; set; } = 100;
        public int Pan { get; set; }
        public int StereoSep { get; set; }
        public int LowLevel { get; set; }
        public int BandLevel { get; set; }
        public int HighLevel { get; set; }
        public int LowFreq { get; set; }
        public int BandFreq { get; set; }
        public int HighFreq { get; set; }
        public int LowWidth { get; set; }
        public int BandWidth { get; set; }
        public int HighWidth { get; set; }
        public bool[] Routes { get; set; } = new bool[Constants.MaxInsertCount];
        public int[] RouteVolumes { get; set; } = new int[Constants.MaxInsertCount];
        public InsertSlot[] Slots { get; set; } = new InsertSlot[MaxSlotCount];

        public Insert()
        {
            for (var i = 0; i < MaxSlotCount; i++)
                Slots[i] = new InsertSlot();

            for (var i = 0; i < Constants.MaxInsertCount; i++)
                RouteVolumes[i] = 12800;
        }
    }
}
