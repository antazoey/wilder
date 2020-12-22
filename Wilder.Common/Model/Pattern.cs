using System.Collections.Generic;

namespace Wilder.Common.Model
{
    public class Pattern
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public Dictionary<Channel, List<Note>> Notes { get; set; } = new Dictionary<Channel, List<Note>>();
    }
}
