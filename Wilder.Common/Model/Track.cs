using System.Collections.Generic;
using Wilder.Common.Interfaces;

namespace Wilder.Common.Model
{
    public class Track
    {
        public string Name { get; set; }
        public uint Color { get; set; }
        public List<IPlaylistItem> Items { get; set; } = new List<IPlaylistItem>();
    }
}
