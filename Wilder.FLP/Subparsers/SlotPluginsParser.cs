using System;
using System.IO;
using System.Text;
using Wilder.Common.Enum;
using Wilder.Common.Model;
// ReSharper disable SwitchStatementMissingSomeEnumCasesNoDefault

namespace Wilder.FLP.Subparsers
{
    internal static class SlotPluginsParser
    {
        internal static void InitSlotPlugins(BinaryReader reader, GeneratorData genData, InsertSlot slot, int bufferLength)
        {
            if (slot != null)
            {
                slot.PluginSettings = reader.ReadBytes(bufferLength);
                slot.Plugin = ParsePluginChunk(slot.PluginSettings);
            }
            else
            {
                if (genData == null)
                    return;
                if (genData.PluginSettings != null)
                    throw new Exception("Attempted to overwrite plugin");

                genData.PluginSettings = reader.ReadBytes(bufferLength);
                genData.Plugin = ParsePluginChunk(genData.PluginSettings);
            }
        }

        private static Plugin ParsePluginChunk(byte[] chunk)
        {
            var plugin = new Plugin();

            using var reader = new BinaryReader(new MemoryStream(chunk));
            var pluginType = (PluginType)reader.ReadInt32();

            if (pluginType != PluginType.Vst)
                return null;

            while (reader.BaseStream.Position < reader.BaseStream.Length)
            {
                var eventId = (PluginChunkId)reader.ReadInt32();
                var length = (int)reader.ReadInt64();

                switch (eventId)
                {
                    case PluginChunkId.VendorName:
                        plugin.VendorName = Encoding.ASCII.GetString(reader.ReadBytes(length));
                        break;
                    case PluginChunkId.Filename:
                        plugin.FileName = Encoding.ASCII.GetString(reader.ReadBytes(length));
                        break;
                    case PluginChunkId.Name:
                        plugin.Name = Encoding.ASCII.GetString(reader.ReadBytes(length));
                        break;
                    case PluginChunkId.State:
                        plugin.State = reader.ReadBytes(length);
                        break;
                }
            }
            return plugin;
        }
    }
}
