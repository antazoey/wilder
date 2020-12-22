namespace Wilder.Common.Model
{
    public class InsertSlot
    {
        public int Volume { get; set; } = 100;
        public int State { get; set; }
        public int DryWet { get; set; } = -1;
        public byte[] PluginSettings { get; set; }
        public Plugin Plugin { get; set; } = new Plugin();
    }
}
