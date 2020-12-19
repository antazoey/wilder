using Wilder.Common.Interfaces;

namespace Wilder.Common.Model
{
    public class Channel
    {
        public int Id { get; set; } = 0;
        public string Name { get; set; } = string.Empty;
        public uint Color { get; set; } = 0x4080FF;
        public IChannelData Data { get; set; } = null;
    }
}
