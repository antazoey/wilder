using System;
using System.IO;
using System.Text;
using Wilder.Common.Enum;
using Wilder.FLP.Subparsers;
// ReSharper disable SwitchStatementMissingSomeEnumCasesNoDefault
// ReSharper disable SwitchStatementHandlesSomeKnownEnumValuesWithDefault

namespace Wilder.FLP
{
    internal class EventHandler
    {
        readonly ProjectParser _projectParser;

        public EventHandler(ProjectParser projectParser)
        {
            _projectParser = projectParser;
        }

        public void ParseEvent(BinaryReader reader)
        {
            var eventId = (Event)reader.ReadByte();
            if (eventId < Event.Word)
                ParseByteEvent(eventId, reader);
            else if (eventId < Event.Int)
                ParseWordEvent(eventId, reader);
            else if (eventId < Event.Text)
                ParseDwordEvent(eventId, reader);
            else if (eventId < Event.Data)
                ParseTextEvent(eventId, reader);
            else
                ParseDataEvent(eventId, reader);
        }

        private void ParseByteEvent(Event eventId, BinaryReader reader)
        {
            var data = reader.ReadByte();
            var genData = _projectParser.GeneratorData;
            switch (eventId)
            {
                case Event.ByteMainVol:
                    _projectParser.Project.MainVolume = data;
                    break;
                case Event.ByteUseLoopPoints:
                    if (genData != null)
                        genData.SampleUseLoopPoints = true;
                    break;
                case Event.ByteMixSliceNum:
                    if (genData != null)
                        genData.Insert = data;
                    break;
                case Event.BytePlayTruncatedNotes:
                    _projectParser.Project.PlayTruncatedNotes = Convert.ToBoolean(data);
                    break;
            }
        }

        private void ParseWordEvent(Event eventId, BinaryReader reader)
        {
            var data = reader.ReadUInt16();
            var genData = _projectParser.GeneratorData;
            switch (eventId)
            {
                case Event.WordNewChan:
                    _projectParser.CurrentChannel = data;
                    break;
                case Event.WordNewPat:
                    while (_projectParser.PatternsCount < data)
                        _projectParser.AddPatternFromCount();
                    _projectParser.CurrentPattern = data;
                    break;
                case Event.WordTempo:
                    _projectParser.Project.Tempo = data;
                    break;
                case Event.WordFadeStereo:
                    if (genData == null)
                        break;
                    if ((data & 0x02) != 0)
                        genData.SampleReversed = true;
                    else if ((data & 0x100) != 0)
                        genData.SampleReverseStereo = true;
                    break;
                case Event.WordPreAmp:
                    if (genData == null)
                        break;
                    genData.SampleAmp = data;
                    break;
                case Event.WordMainPitch:
                    _projectParser.Project.MainPitch = data;
                    break;
                case Event.WordInsertIcon:
                    _projectParser.CurrentInsertIcon = data;
                    break;
                case Event.WordCurrentSlotNum:
                    _projectParser.CurrentSlot = data;
                    break;
            }
        }

        private void ParseDwordEvent(Event eventId, BinaryReader reader)
        {
            var data = reader.ReadUInt32();
            switch (eventId)
            {
                case Event.DWordColor:
                    _projectParser.CurrentChannelColor = data;
                    break;
                case Event.DWordMiddleNote:
                    _projectParser.CurrentChannelMiddleNote = data;
                    break;
                case Event.DWordInsertColor:
                    _projectParser.CurrentInsertColor = data;
                    break;
                case Event.DWordFineTempo:
                    _projectParser.Project.Tempo = data / 1000.0;
                    break;
            }
        }

        private static int GetBufferLen(BinaryReader reader)
        {
            var data = reader.ReadByte();
            var dataLen = data & 0x7F;
            var shift = 0;
            while ((data & 0x80) != 0)
            {
                data = reader.ReadByte();
                dataLen |= ((data & 0x7F) << (shift += 7));
            }
            return dataLen;
        }

        private void ParseTextEvent(Event eventId, BinaryReader reader)
        {
            var dataLen = GetBufferLen(reader);
            var dataBytes = reader.ReadBytes(dataLen);
            var unicodeString = Encoding.Unicode.GetString(dataBytes);
            if (unicodeString.EndsWith("\0"))
                unicodeString = unicodeString.Substring(0, unicodeString.Length - 1);

            var genData = _projectParser.GeneratorData;
            switch (eventId)
            {
                case Event.TextChanName:
                    _projectParser.CurrentChannelName = unicodeString;
                    break;
                case Event.TextPatName:
                    _projectParser.CurrentPatternName = unicodeString;
                    break;
                case Event.TextTitle:
                    _projectParser.Project.Title = unicodeString;
                    break;
                case Event.TextAuthor:
                    _projectParser.Project.Author = unicodeString;
                    break;
                case Event.TextComment:
                    _projectParser.Project.Comment = unicodeString;
                    break;
                case Event.TextGenre:
                    _projectParser.Project.Genre = unicodeString;
                    break;
                case Event.TextSampleFileName:
                    ProjectParser.ParseGeneratorName(genData, unicodeString);
                    break;
                case Event.TextVersion:
                    _projectParser.ParseVersion(dataBytes);
                    break;
                case Event.GeneratorName:
                    if (genData != null)
                        genData.GeneratorName = unicodeString;
                    break;
                case Event.TextInsertName:
                    _projectParser.CurrentInsertName = unicodeString;
                    break;
                default:
                    Console.WriteLine(eventId);
                    Console.WriteLine($"Unhandled text event: {unicodeString}");
                    break;
            }
        }

        private void ParseDataEvent(Event eventId, BinaryReader reader)
        {
            var dataLen = GetBufferLen(reader);
            var dataStart = reader.BaseStream.Position;
            var dataEnd = dataStart + dataLen;
            var genData = _projectParser.GeneratorData;
            var autData = _projectParser.AutomationData;
            switch (eventId)
            {
                case Event.DataPluginParams:
                    _projectParser.InitSlotPlugins(reader, genData, dataLen);
                    break;
                case Event.DataChanParams:
                    ChannelParser.ParseChannelParameters(genData, reader);
                    break;
                case Event.DataBasicChanParams:
                    ChannelParser.ParseBasicChannelParameters(genData, reader);
                    break;
                case Event.DataPatternNotes:
                    _projectParser.ParsePatternNotes(reader, dataEnd);
                    break;
                case Event.DataInsertParams:
                    _projectParser.ParseInsertParameters(reader, dataEnd);
                    break;
                case Event.DataAutomationChannels:
                    _projectParser.ParseAutomationChannels(reader, dataEnd);
                    break;
                case Event.DataPlayListItems:
                    _projectParser.ParsePlayListItems(reader, dataEnd);
                    break;
                case Event.DataAutomationData:
                    _projectParser.ParseAutomationData(reader, autData);
                    break;
                case Event.DataInsertRoutes:
                    _projectParser.ParseInsertRoutes(reader);
                    break;
                case Event.DataInsertFlags:
                    _projectParser.ParseInsertFlags(reader);
                    break;
            }

            // make sure cursor is at end of data
            reader.BaseStream.Position = dataEnd;
        }
    }
}
