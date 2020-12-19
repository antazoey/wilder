using System;
using System.IO;
using System.Text;
using Wilder.Common.Exceptions;

namespace Wilder.FLP
{
    internal class ProjectFactory
    {
        public Project CreateProject(BinaryReader flpReader)
        {
            var parser = new ProjectParser();
            ParseHeader(flpReader, parser);
            ParseFldt(flpReader);
            ParseEvents(flpReader, parser);
            return parser.Project;
        }

        void ParseHeader(BinaryReader reader, ProjectParser parser)
        {
            VerifyMagicNumber(reader);
            VerifyHeader(reader);
            VerifyType(reader);
            ParseChannels(reader, parser);
            ParsePpq(reader, parser);
        }

        void VerifyMagicNumber(BinaryReader reader)
        {
            if (Encoding.ASCII.GetString(reader.ReadBytes(4)) != "FLhd")
                throw new FlParseException("Invalid magic number", reader.BaseStream.Position);
        }

        void VerifyHeader(BinaryReader reader)
        {
            var headerLength = reader.ReadInt32();
            if (headerLength != 6)
                throw new FlParseException($"Expected header length 6, not {headerLength}", reader.BaseStream.Position);
        }

        void VerifyType(BinaryReader reader)
        {
            var type = reader.ReadInt16();
            if (type != 0)
                throw new FlParseException($"Type {type} is not supported", reader.BaseStream.Position);
        }

        void ParseChannels(BinaryReader reader, ProjectParser parser)
        {
            var channelCount = reader.ReadInt16();
            if (channelCount < 1 || channelCount > 1000)
                throw new FlParseException($"Invalid number of channels: {channelCount}", reader.BaseStream.Position);
            for (var i = 0; i < channelCount; i++)
                parser.AddChannelFromIndex(i);
        }

        void ParsePpq(BinaryReader reader, ProjectParser parser)
        {
            parser.Project.Ppq = reader.ReadInt16();
            if (parser.Project.Ppq < 0)
                throw new Exception($"Invalid PPQ: {parser.Project.Ppq}");
        }

        void ParseFldt(BinaryReader reader)
        {
            string id;
            var len = 0;
            do
            {
                reader.ReadBytes(len);
                id = Encoding.ASCII.GetString(reader.ReadBytes(4));
                len = reader.ReadInt32();
                if (len < 0 || len > 0x10000000)
                    throw new FlParseException($"Invalid chunk length: {len}", reader.BaseStream.Position);

            } while (id != "FLdt");
        }

        void ParseEvents(BinaryReader reader, ProjectParser parser)
        {
            var handler = new EventHandler(parser);
            while (reader.BaseStream.Position < reader.BaseStream.Length)
                handler.ParseEvent(reader);
        }
    }
}
