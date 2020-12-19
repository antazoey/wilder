using Wilder.Common.Interfaces;

namespace Wilder.Common.Model
{
    public class PatternPlaylistItem : IPlaylistItem
    {
        public int Position { get; set; }
        public int Length { get; set; }
        public int StartOffset { get; set; }
        public int EndOffset { get; set; }
        public bool Muted { get; set; }
        public Pattern Pattern { get; set; }
    }
}
