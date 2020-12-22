using Wilder.Common.Interfaces;
using Wilder.AlbumMaker;
using Wilder.FLP;
using Wilder.Player.VLC;

namespace Wilder
{
    public class Core
    {
        public IAlbumMaker AlbumMaker { get; }
        
        public IPlayer Player { get; }
        
        public IProjectParser ProjectParser { get; }

        public Core(): this(new AlbumMakerApi(), new VLCPlayer(), new ProjectParser()) { }

        public Core(IAlbumMaker albumMaker, IPlayer player, IProjectParser projectParser)
        {
            AlbumMaker = albumMaker;
            Player = player;
            ProjectParser = projectParser;
        }
    }
}