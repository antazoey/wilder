using System.Collections.Generic;
using System.IO;
using Wilder.Common.Model;

namespace Wilder.FLP.Subparsers
{
    internal static class PatternNotesParser
    {
        internal static void ParsePatternNotes(Project project, BinaryReader reader, Pattern pattern, long dataEnd)
        {
            while (reader.BaseStream.Position < dataEnd)
            {
                var pos = reader.ReadInt32();
                _ = reader.ReadInt16();
                var ch = reader.ReadByte();
                _ = reader.ReadByte();
                var length = reader.ReadInt32();
                var key = reader.ReadByte();
                _ = reader.ReadInt16();
                _ = reader.ReadByte();
                var finePitch = reader.ReadUInt16();
                var release = reader.ReadUInt16();
                var pan = reader.ReadByte();
                var velocity = reader.ReadByte();
                _ = reader.ReadByte();
                _ = reader.ReadByte();

                var channel = project.Channels[ch];
                if (!pattern.Notes.ContainsKey(channel))
                    pattern.Notes.Add(channel, new List<Note>());
                pattern.Notes[channel].Add(new Note
                {
                    Position = pos,
                    Length = length,
                    Key = key,
                    FinePitch = finePitch,
                    Release = release,
                    Pan = pan,
                    Velocity = velocity
                });
            }
        }
    }
}
