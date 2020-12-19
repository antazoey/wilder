using System.IO;
using Wilder.Common;
using Wilder.Common.Enum;
using Wilder.Common.Model;

namespace Wilder.FLP.Subparsers
{
    internal static class InsertParser
    {
        internal static void ParseInsertParameters(Project project, BinaryReader reader, long dataEnd)
        {
            while (reader.BaseStream.Position < dataEnd)
            {
                _ = reader.BaseStream.Position;
                _ = reader.ReadInt32();
                var messageId = (InsertParam)reader.ReadByte();
                _ = reader.ReadByte();
                var channelData = reader.ReadUInt16();
                var messageData = reader.ReadInt32();
                var slotId = channelData & 0x3F;
                var insertId = (channelData >> 6) & 0x7F;
                _ = channelData >> 13;
                var insert = project.Inserts[insertId];
                ParserInsertParameter(insert, messageId, messageData, slotId);
            }
        }

        internal static void ParseInsertRoutes(BinaryReader reader, Insert flInsert)
        {
            for (var i = 0; i < Constants.MaxInsertCount; i++)
                flInsert.Routes[i] = reader.ReadBoolean();
        }

        internal static void ParseInsertFlags(BinaryReader reader, Insert flInsert)
        {
            reader.ReadUInt32();
            var flags = (InsertFlags)reader.ReadUInt32();
            flInsert.Flags = flags;
        }

        private static void ParserInsertParameter(Insert insert, InsertParam messageId, int messageData, int slotId)
        {
            switch (messageId)
            {
                case InsertParam.SlotState:
                    insert.Slots[slotId].State = messageData;
                    break;
                case InsertParam.SlotVolume:
                    insert.Slots[slotId].Volume = messageData;
                    break;
                case InsertParam.Volume:
                    insert.Volume = messageData;
                    break;
                case InsertParam.Pan:
                    insert.Pan = messageData;
                    break;
                case InsertParam.StereoSep:
                    insert.StereoSep = messageData;
                    break;
                case InsertParam.LowLevel:
                    insert.LowLevel = messageData;
                    break;
                case InsertParam.BandLevel:
                    insert.BandLevel = messageData;
                    break;
                case InsertParam.HighLevel:
                    insert.HighLevel = messageData;
                    break;
                case InsertParam.LowFreq:
                    insert.LowFreq = messageData;
                    break;
                case InsertParam.BandFreq:
                    insert.BandFreq = messageData;
                    break;
                case InsertParam.HighFreq:
                    insert.HighFreq = messageData;
                    break;
                case InsertParam.LowWidth:
                    insert.LowWidth = messageData;
                    break;
                case InsertParam.BandWidth:
                    insert.BandWidth = messageData;
                    break;
                case InsertParam.HighWidth:
                    insert.HighWidth = messageData;
                    break;
                default:
                    // any value 64 or above appears to be the desination insert
                    if ((int)messageId >= 64 && (int)messageId <= 64 + 104)
                    {
                        var insertDest = (int)messageId - 64;
                        insert.RouteVolumes[insertDest] = messageData;
                    }
                    break;
            }
        }
    }
}
