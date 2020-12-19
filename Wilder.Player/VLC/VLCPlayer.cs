using System;
using LibVLCSharp.Shared;

namespace Wilder.Player.VLC
{
    public class VLCPlayer
    {
        readonly  LibVLC _libvlc;

        public VLCPlayer()
        {
            Core.Initialize();
            _libvlc = new LibVLC(enableDebugLogs: true);
        }

        public void Play(string songPath)
        {
            using var media = new Media(_libvlc, new Uri(songPath));
            using var mediaplayer = new MediaPlayer(media);
            mediaplayer.Play();
        }
    }
}
