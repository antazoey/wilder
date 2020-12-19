using System.ComponentModel.DataAnnotations.Schema;

namespace Wilder.Agency.Model
{
    public class Track
    {
        /// <summary>
        /// The title of the track.
        /// </summary>
        public string Title { get; set; }

        /// <summary>
        /// The number of the track on its album.
        /// </summary>
        public int TrackNumber { get; set; }

        /// <summary>
        /// The album the track is on.
        /// </summary>
        [ForeignKey("Name")]
        public Album Album { get; set; }
    }
}
