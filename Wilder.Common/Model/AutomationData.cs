using Wilder.Common.Interfaces;

namespace Wilder.Common.Model
{
    public class AutomationData : IChannelData
    {
        public Channel Channel { get; set; }
        public int Parameter { get; set; }
        public int InsertId { get; set; } = -1;
        public int SlotId { get; set; } = -1;
        public bool VstParameter { get; set; } = true;
        public AutomationKeyframe[] Keyframes { get; set; } = new AutomationKeyframe[0];
    }
}
