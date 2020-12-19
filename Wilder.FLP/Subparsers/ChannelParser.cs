using System.IO;
using Wilder.Common.Enum;
using Wilder.Common.Model;

namespace Wilder.FLP.Subparsers
{
    internal static class ChannelParser
    {
        internal static void ParseChannelParameters(GeneratorData genData, BinaryReader reader)
        {
            if (genData == null)
                return;
            _ = reader.ReadBytes(40);
            genData.ArpDir = (ArpDirection)reader.ReadInt32();
            genData.ArpRange = reader.ReadInt32();
            genData.ArpChord = reader.ReadInt32();
            genData.ArpTime = reader.ReadInt32() + 1;
            genData.ArpGate = reader.ReadInt32();
            genData.ArpSlide = reader.ReadBoolean();
            _ = reader.ReadBytes(31);
            genData.ArpRepeat = reader.ReadInt32();
            _ = reader.ReadBytes(29);
        }

        internal static void ParseBasicChannelParameters(GeneratorData genData, BinaryReader reader)
        {
            if (genData == null)
                return;
            genData.Panning = reader.ReadInt32();
            genData.Volume = reader.ReadInt32();
        }

        internal static void AddNewChannelFromIndex(Project project, int index)
        {
            project.Channels.Add(new Channel { Id = index, Data = new GeneratorData() });
        }
    }
}
