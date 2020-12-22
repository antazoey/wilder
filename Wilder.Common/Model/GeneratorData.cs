using System;
using Wilder.Common.Enum;
using Wilder.Common.Interfaces;

namespace Wilder.Common.Model
{
    public class GeneratorData : IChannelData
    {
        public byte[] PluginSettings { get; set; }
        public Plugin Plugin { get; set; } = new Plugin();
        public string GeneratorName { get; set; } = string.Empty;
        public double Volume { get; set; } = 100;
        public double Panning { get; set; } = 0;
        public uint BaseNote { get; set; } = 57;
        public int Insert { get; set; } = -1;
        public int LayerParent { get; set; } = -1;

        public string SampleFileName { get; set; } = string.Empty;
        public int SampleAmp { get; set; } = 100;
        public bool SampleReversed { get; set; }
        public bool SampleReverseStereo { get; set; }
        public bool SampleUseLoopPoints { get; set; }

        public ArpDirection ArpDir { get; set; } = ArpDirection.Off;
        public int ArpRange { get; set; }
        public int ArpChord { get; set; }
        public int ArpRepeat { get; set; }
        public double ArpTime { get; set; } = 100;
        public double ArpGate { get; set; } = 100;
        public bool ArpSlide { get; set; }
    }
}
