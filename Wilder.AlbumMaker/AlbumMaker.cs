using Wilder.Common.Interfaces;
using Wilder.AlbumMaker.Repositories;

namespace Wilder.AlbumMaker
{
    public class AlbumMakerApi : IAlbumMaker
    {
        public IAlbumRepository Albums { get; }

        public AlbumMakerApi() : this(new AlbumRepository())
        {
        }

        public AlbumMakerApi(IAlbumRepository albums)
        {
            Albums = albums;
        }
    }
}