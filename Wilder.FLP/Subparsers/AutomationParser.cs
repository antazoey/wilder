using System.IO;
using Wilder.Common.Model;

namespace Wilder.FLP.Subparsers
{
    internal static class AutomationParser
    {
        internal static void ParseAutomationChannels(Project project, BinaryReader reader, long dataEnd)
        {
            while (reader.BaseStream.Position < dataEnd)
            {
                _ = reader.ReadUInt16();
                var automationChannel = reader.ReadByte();
                _ = reader.ReadUInt32();
                _ = reader.ReadByte();
                var param = reader.ReadUInt16();
                var paramDestination = reader.ReadInt16();
                _ = reader.ReadUInt64();

                var channel = project.Channels[automationChannel];

                if ((paramDestination & 0x2000) == 0)  // Automation on channel
                    SetChannelData(project, channel, paramDestination, param);
                else
                    SetChannelSlotData(channel, paramDestination, param);
            }
        }

        internal static void ParseAutomationData(Project project, BinaryReader reader, AutomationData autData)
        {
            _ = reader.ReadUInt32(); // always 1?
            _ = reader.ReadUInt32(); // always 64?
            _ = reader.ReadByte();
            _ = reader.ReadUInt16();
            _ = reader.ReadUInt16(); // always 0?
            _ = reader.ReadUInt32();
            var keyCount = reader.ReadUInt32();

            if (autData == null)
                return;
            autData.Keyframes = new AutomationKeyframe[keyCount];

            for (var i = 0; i < keyCount; i++)
                ParseAutomationKeyFrame(project, reader, autData, i);

            // remaining data is unknown
        }

        private static void SetChannelData(Project project, Channel channel, short destination, ushort param)
        {
            channel.Data = new AutomationData
            {
                Channel = project.Channels[destination],
                Parameter = param & 0x7fff,
                // switch determines if automation is on channel or vst
                VstParameter = (param & 0x8000) > 0
            };
        }

        private static void SetChannelSlotData(Channel channel, short destination, ushort param)
        {
            channel.Data = new AutomationData // automation on insert slot
            {
                Parameter = param & 0x7fff,
                InsertId = (destination & 0x0FF0) >> 6,  // seems to be out by one
                SlotId = destination & 0x003F
            };
        }

        private static void ParseAutomationKeyFrame(Project project, BinaryReader reader, AutomationData autData, int index)
        {
            var startPos = reader.BaseStream.Position;

            var keyPos = reader.ReadDouble();
            var keyVal = reader.ReadDouble();
            var keyTension = reader.ReadSingle();
            _ = reader.ReadUInt32(); // seems linked to tension?

            var endPos = reader.BaseStream.Position;
            reader.BaseStream.Position = startPos;
            _ = reader.ReadBytes((int)(endPos - startPos));

            autData.Keyframes[index] = CreateAutomationKeyFrame(project, keyPos, keyTension, keyVal);
        }

        static AutomationKeyframe CreateAutomationKeyFrame(Project project, double keyPos, float keyTension, double keyVal)
        {
            return new AutomationKeyframe
            {
                Position = (int)(keyPos * project.Ppq),
                Tension = keyTension,
                Value = keyVal
            };
        }
    }
}
