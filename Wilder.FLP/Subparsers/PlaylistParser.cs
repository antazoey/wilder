using System.IO;
using Wilder.Common.Model;

namespace Wilder.FLP.Subparsers
{
    internal static class PlaylistParser
    {

        internal static void ParsePlayListItems(Project project, BinaryReader reader, int versionMajor, long dataEnd)
        {
            while (reader.BaseStream.Position < dataEnd)
            {
                var startTime = reader.ReadInt32();
                var patternBase = reader.ReadUInt16();
                var patternId = reader.ReadUInt16();
                var length = reader.ReadInt32();
                var track = reader.ReadInt32();
                if (versionMajor == 20)
                    track = 501 - track;
                else
                    track = 198 - track;
                _ = reader.ReadUInt16();
                var itemFlags = reader.ReadUInt16();
                _ = reader.ReadUInt32();
                bool muted = (itemFlags & 0x2000) > 0;  // flag determines if item is muted

                // id of 0-patternBase is samples or automation, after is pattern
                if (patternId <= patternBase)
                    SetChannelPlaylistItem(project, reader, track, startTime, length, patternId, muted);
                else
                    SetPatternPlaylistItem(project, reader, track, startTime, length, patternId, muted, patternBase);
            }
        }

        static void SetChannelPlaylistItem(Project project, BinaryReader reader, int track, int startTime, int length, ushort patternId, bool muted)
        {
            var startOffset = (int)(reader.ReadSingle() * project.Ppq);
            var endOffset = (int)(reader.ReadSingle() * project.Ppq);

            project.Tracks[track].Items.Add(new ChannelPlaylistItem
            {
                Position = startTime,
                Length = length,
                StartOffset = startOffset,
                EndOffset = endOffset,
                Channel = project.Channels[patternId],
                Muted = muted
            });
        }

        static void SetPatternPlaylistItem(
            Project project,
            BinaryReader reader,
            int track,
            int startTime,
            int length,
            ushort patternId,
            bool muted,
            ushort patternBase)
        {
            var startOffset = reader.ReadInt32();
            var endOffset = reader.ReadInt32();

            project.Tracks[track].Items.Add(new PatternPlaylistItem
            {
                Position = startTime,
                Length = length,
                StartOffset = startOffset,
                EndOffset = endOffset,
                Pattern = project.Patterns[patternId - patternBase - 1],
                Muted = muted
            });
        }
    }
}
